"""Add shared s3 secret"""
import re
import sys

from yaspin.core import Yaspin

from mcli.config import MCLIConfig, MCLIConfigError
from mcli.models import MCLIPlatform, SecretType
from mcli.objects.secrets.platform_secret import PlatformSecret
from mcli.objects.secrets.s3_credentials import MCLIS3Secret
from mcli.utils.utils_kube import base64_encode, read_secret

ok_prefix = '✅ '
fail_prefix = '💥 '

DEFAULT_MOUNT_DIRECTORY = '/secrets/aws'
SHARED_SECRET_NAME = 'streaming-credentials-s3'
SHARED_NAMESPACE = 'internal-shared'


def is_rz(x: str) -> bool:
    return re.match(r'r\dz\d', x, re.IGNORECASE) is not None


def main() -> int:

    with Yaspin() as sp:
        sp.text = 'Importing stable s3 config...'
        sp.start()

        # Load mcli config
        try:
            conf: MCLIConfig = MCLIConfig.load_config()
        except MCLIConfigError:
            sp.write(f'{fail_prefix}Could not load mcli config. Please run `mcli init`.')
            sp.stop()
            return 1

        # Verify that the user has an r1z1 platform
        r1z1_platform = None
        for platform in conf.platforms:
            if platform.name == 'r1z1':
                r1z1_platform = platform
                break
        if not r1z1_platform:
            sp.write(f'{fail_prefix}Cannot fetch shared secret because you have not configured the R1Z1 platform. '
                     'If you should have access to this platform, try running `mcli create platform` to configure it.')
            sp.stop()
            return 1

        # Make sure r1z1 is index 0 platform
        new_platforms = [r1z1_platform] + [x for x in conf.platforms if x is not r1z1_platform]
        conf.platforms = new_platforms

        # Get the stable s3 secret from r1z1 shared namespace
        shared_secret = None
        with MCLIPlatform.use(r1z1_platform):
            try:
                shared_secret_data = read_secret(SHARED_SECRET_NAME, SHARED_NAMESPACE)
            except Exception:
                sp.write(f'{fail_prefix}Could not access shared secret')
                sp.stop()
                raise
            if shared_secret_data:
                assert isinstance(shared_secret_data['data'], dict)
                shared_secret = MCLIS3Secret(SHARED_SECRET_NAME, SecretType.s3_credentials)
                shared_secret_data['data'].setdefault('mount_directory', base64_encode(DEFAULT_MOUNT_DIRECTORY))
                shared_secret.unpack(shared_secret_data['data'])
            else:
                sp.write(f'{fail_prefix}Could not find shared secret')
                sp.stop()
                return 1
        assert shared_secret is not None
        sp.write(f'{ok_prefix}Got supplied secret from shared namespace')

        # Sync new s3 secret to r*z* platforms
        sp.text = 'Syncing new secret to R*Z* platforms...'
        platform_secret = PlatformSecret(shared_secret)
        for platform in conf.platforms:
            if is_rz(platform.name):
                with MCLIPlatform.use(platform):
                    platform_secret.create(platform.namespace)
                    sp.write(f'{ok_prefix}Synced secret to platform {platform.name}')

        # Save config
        conf.save_config()
        sp.write(f'{ok_prefix}Finished!')
        sp.stop()
        return 0


if __name__ == '__main__':
    sys.exit(main())
