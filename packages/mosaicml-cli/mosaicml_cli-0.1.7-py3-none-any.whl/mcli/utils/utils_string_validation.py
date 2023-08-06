""" Utils for string validation for user input """
import re
import string
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


def validate_alphanumeric_dash_characters(text: str) -> bool:
    """ Validates lowercase alphanumeric with a dash """
    return re.match(r'[a-z\-]+', text) is not None  # type: ignore


@dataclass
class StringVerificationResult():
    """ Used to return the result of a string verification

    Overrides __len__ to be truthy based on validity
    Overrides __eq__ to cast when being compared to bools
    """
    valid: bool
    message: Optional[str]

    def __bool__(self) -> bool:
        return self.valid

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, bool):
            return bool(self) == __o
        return super().__eq__(__o)


def rfc_verification(
    text: str,
    length: int,
    special_characters: str,
    start_alnum_verification: bool = True,
    end_alnum_verification: bool = True,
    allow_uppercase: bool = False,
) -> StringVerificationResult:
    """Does General RFC Verification with Parameters

    Args:
        text: The text to verify
        length: The maximum length allowed for the string
        special_characters: Regex Escaped Special Characters to
        start_alnum_verification: The first character must be an alnum
        end_alnum_verification: The last character must be an alnum
        allow_uppercase: Allow uppercase characters

    Returns:
        Returns a truthy StringVerificationResult with possible error messages
    """
    if len(text) > length or len(text) == 0:
        return StringVerificationResult(
            False,
            f'Name must be less than {length} characters',
        )
    if allow_uppercase:
        alnum = 'a-zA-Z0-9'
    else:
        alnum = 'a-z0-9'
    valid_characters = f'^[{alnum}{special_characters}]*'

    if re.fullmatch(valid_characters, text) is None:
        return StringVerificationResult(
            False,
            f'Valid characters are only regex [{string.ascii_lowercase}{string.digits}{special_characters}]',
        )

    if start_alnum_verification and not text[0].isalnum():
        return StringVerificationResult(
            False,
            'The first character must be alphanumeric',
        )
    if end_alnum_verification and not text[-1].isalnum():
        return StringVerificationResult(
            False,
            'The last character must be alphanumeric',
        )

    return StringVerificationResult(True, None)


def ensure_rfc_compatibility(
    text: str,
    length: int,
    special_characters: str,
    start_alnum_verification: bool = True,
    end_alnum_verification: bool = True,
    alnum_pad: str = '1',
    special_replacement: str = '-',
) -> str:

    invalid_characters = f'[^a-z0-9{special_characters}]'
    repl = re.subn(invalid_characters, special_replacement, text.lower())[0]
    repl = repl[:length]
    if repl == '':
        return repl

    if start_alnum_verification and not repl[0].isalnum():
        repl = alnum_pad + repl[:-len(alnum_pad)]

    if end_alnum_verification and not repl[-1].isalnum():
        repl = repl[:-len(alnum_pad)] + alnum_pad

    return repl


def validate_rfc1123_name(text: str) -> StringVerificationResult:
    """
    A check on text validity based on k8s rfc1123 spec

        contain at most 63 characters
        contain only lowercase alphanumeric characters or '-'
        start with an alphanumeric character
        end with an alphanumeric character
    """
    return rfc_verification(text=text, length=63, special_characters=r'\-')


def ensure_rfc1123_compatibility(text: str) -> str:
    """
    Ensures that names are valid based on k8s rfc1123 spec
    """
    return ensure_rfc_compatibility(
        text=text,
        length=63,
        special_characters=r'\-',
    )


def validate_dns_subdomain_name(text: str) -> StringVerificationResult:
    """
    Ensures that secret names are valid based on k8s rfc1123 spec


        contain no more than 253 characters
        contain only lowercase alphanumeric characters, '-' or '.'
        start with an alphanumeric character
        end with an alphanumeric character
    """
    return rfc_verification(text=text, length=253, special_characters=r'\-\.')


def validate_secret_name(secret_name: str) -> StringVerificationResult:
    """
    Ensures that secret names are valid based on k8s spec

        contain no more than 253 characters
        contain only lowercase alphanumeric characters, '-' or '.'
        start with an alphanumeric character
        end with an alphanumeric character
    """

    return validate_dns_subdomain_name(text=secret_name)


def validate_secret_key(secret_key: str) -> StringVerificationResult:
    """
    Ensures that secret keys are valid based on k8s spec

        contain no more than 253 characters
        contain only alphanumeric characters, '-' or '.' or '_'
    """
    verification_result = rfc_verification(
        text=secret_key,
        length=253,
        special_characters=r'\-\._A-Z',
        start_alnum_verification=False,
        end_alnum_verification=False,
    )
    return verification_result


def validate_absolute_path(path: str) -> bool:
    """Ensures that the given path is an absolute path

    Args:
        path: File path

    Returns:
        True if path is absolute
    """

    return Path(path).is_absolute()


def validate_existing_filename(filename: str) -> bool:
    """Ensures that the given filename exists

    Args:
        filename: File path

    Returns:
        True if file exists and is a file
    """
    path = Path(filename).expanduser().absolute()
    return path.exists() and path.is_file()


def validate_existing_directory(directory: str) -> bool:
    """Ensures that the given filename exists

    Args:
        directory: Directory path

    Returns:
        True if directory exists and is a directory
    """
    path = Path(directory).expanduser().absolute()
    return path.exists() and path.is_dir()


def validate_url(url: str) -> bool:
    """Validate that `url` is a valid URL

    Args:
        url: URL

    Returns:
        True if url is valid
    """

    return urlparse(url) is not None


def validate_email_address(email: str) -> bool:
    """Validate that `email` is a valid email address

    Args:
        email: Email address

    Returns:
        True if the email address is valid
    """

    pattern = r'^[^@]*@.*\..*$'
    return re.fullmatch(pattern, email) is not None


KEY_VALUE_PATTERN = r'^([a-zA-Z_][a-zA-Z0-9_]*)=(.*)'


def validate_key_value_pair(key_value_str: str) -> bool:
    """Validate the a string is of the form KEY=VALUE

    Args:
        key_value_str: String of the form KEY=VALUE

    Returns:
        True if string is valid
    """
    return re.fullmatch(KEY_VALUE_PATTERN, key_value_str) is not None
