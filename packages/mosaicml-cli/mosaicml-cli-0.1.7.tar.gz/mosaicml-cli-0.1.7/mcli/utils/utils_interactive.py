"""Util Functions for Interactive User Prompting"""
import logging
from typing import Any, Callable, List, Optional, TypeVar, Union, overload

from typing_extensions import Literal

T_Option = TypeVar('T_Option')  # pylint: disable=invalid-name
T_Option_Str = Union[T_Option, str]  # pylint: disable=invalid-name

logger = logging.getLogger(__name__)


def validate_true(_: Any) -> bool:
    return True


class DoesNotExistValidator():
    """Returns ``False`` if the choice is not in the provided list
    """

    def __init__(self, existing: List[str]):
        self.existing = existing

    def __call__(self, choice: str) -> bool:
        return choice in self.existing


class AlreadyExistsValidator():
    """Returns ``False`` if the choice duplicates a value in the provided list
    """

    def __init__(self, existing: List[str]):
        self.existing = existing

    def __call__(self, choice: str) -> bool:
        return choice not in self.existing


_INPUT_DISABLED: bool = False
_INPUT_DISABLED_MESSAGE: str = 'Interactivity requested when input was disabled'


class ValidationError(Exception):
    """Base class for interactive validation errors
    """


def get_validation_callback(validation_fun, *args, **kwargs) -> Callable[[T_Option], bool]:  # type: ignore

    def validator(option: T_Option) -> bool:
        try:
            return validation_fun(option, *args, **kwargs)
        except ValidationError:
            return False

    return validator


class InputDisabledError(Exception):
    """Error thrown when interactivity is requested but input has been disabled.
    """


class input_disabled():
    """Context manager for enabling or disabling input

    If interactive prompts are requested while input has been disabled, an `InputDisabledError` will be thrown.

    Args:
        disabled (bool, optional): If True, disable input within the context. Defaults to True.
    """

    def __init__(self, disabled: bool = True):
        self.disabled = disabled
        self.prev: Optional[bool] = None

    @staticmethod
    def set_disabled(disabled: bool):
        globals()['_INPUT_DISABLED'] = disabled

    def __enter__(self):
        self.prev = _INPUT_DISABLED
        self.set_disabled(self.disabled)
        return self

    def __exit__(self, exc_type, value, traceback):
        assert self.prev is not None
        self.set_disabled(self.prev)
        return False


@overload
def list_options(
    input_text: str,
    options: List[T_Option],
    *,
    allow_custom_response: Literal[False] = False,
    multiple_ok: Literal[False] = False,
    default_response: Optional[T_Option] = None,
    pre_helptext: Optional[str] = 'Interactive selection...',
    helptext: str = 'put a number or enter your own option',
    validate: Callable[[T_Option], bool] = validate_true,
    print_option: Callable[[T_Option], str] = str,
    print_response: bool = True,
) -> T_Option:
    ...


@overload
def list_options(
    input_text: str,
    options: List[T_Option],
    *,
    allow_custom_response: Literal[True],
    multiple_ok: Literal[False] = False,
    default_response: Optional[T_Option] = None,
    pre_helptext: Optional[str] = 'Interactive selection...',
    helptext: str = 'put a number or enter your own option',
    validate: Callable[[T_Option], bool] = validate_true,
    print_option: Callable[[T_Option], str] = str,
    print_response: bool = True,
) -> T_Option_Str[T_Option]:
    ...


@overload
def list_options(
    input_text: str,
    options: List[T_Option],
    *,
    multiple_ok: Literal[True],
    allow_custom_response: Literal[False] = False,
    default_response: Optional[T_Option] = None,
    pre_helptext: Optional[str] = 'Interactive selection...',
    helptext: str = 'put a number or enter your own option',
    validate: Callable[[T_Option], bool] = validate_true,
    print_option: Callable[[T_Option], str] = str,
    print_response: bool = True,
) -> List[T_Option]:
    ...


@overload
def list_options(
    input_text: str,
    options: List[T_Option],
    *,
    allow_custom_response: Literal[True],
    multiple_ok: Literal[True],
    default_response: Optional[T_Option] = None,
    pre_helptext: Optional[str] = 'Interactive selection...',
    helptext: str = 'put a number or enter your own option',
    validate: Callable[[T_Option], bool] = validate_true,
    print_option: Callable[[T_Option], str] = str,
    print_response: bool = True,
) -> List[T_Option_Str[T_Option]]:
    ...


def _list_options_single_response(
    input_text: str,
    options: List[T_Option],
    *,
    allow_custom_response: bool = False,
    multiple_ok: bool = False,
    default_response: Optional[T_Option] = None,
    helptext: str = 'put a number or enter your own option',
    validate: Callable[[Union[str, T_Option]], bool] = validate_true,
    print_option: Callable[[Union[str, T_Option]], str] = str,
    print_response: bool = True,
) -> Union[T_Option, str, List[T_Option], List[str]]:

    if _INPUT_DISABLED:
        raise InputDisabledError(_INPUT_DISABLED_MESSAGE)

    response: Union[List[T_Option], List[str]] = []
    if len(options) == 1 and default_response is None:
        default_response = options[0]
    full_helptext = print_option(default_response) if default_response else helptext
    while not response:
        response_input = input(f'{input_text} ({full_helptext}): ')
        if response_input == '' and default_response:
            response = [default_response]
        if allow_custom_response and response_input != '':
            response = [response_input]
        if not all((validate(x) for x in response)):
            response = []

        if not multiple_ok and len(response) > 1:
            response = []
            print('Only one response allowed')
        if not response:
            print(response_input, 'received. Please input a response: ')
    if print_response:
        response_choices = ', '.join([print_option(x) for x in response])
        print(f'Selected: {response_choices}')

    if not multiple_ok and isinstance(response, list) and len(response) == 1:
        return response[0]
    return response


def list_options(
    input_text: str,
    options: List[T_Option],
    *,
    allow_custom_response: bool = False,
    multiple_ok: bool = False,
    default_response: Optional[T_Option] = None,
    pre_helptext: Optional[str] = 'Interactive selection...',
    helptext: str = 'put a number or enter your own option',
    validate: Callable[[Union[str, T_Option]], bool] = validate_true,
    print_option: Callable[[Union[str, T_Option]], str] = str,
    print_response: bool = True,
) -> Union[T_Option, str, List[T_Option], List[str], List[T_Option_Str[T_Option]]]:
    """Produces an interactive list of options or a single confirmation with
    many parameters

    Multiple Options Printout format:

    {pre_helptext}
    1) Option 1
    2) Option 2
    3) Option 3
    {input_text} ({helptext}): <USER INPUT HERE>

    Single Option Printout format:

    {pre_helptext}
    {input_text} ({default_response if default_response else helptext}): <USER INPUT HERE>

    Args:
        input_text: The pre-text to put on the confirmation line where the user
            types. Default parameters are added after the input_text
        options: A list of options that are allowed. Behavior switches from a
            numbered picker to a prompt if <=1 options are provided
        default_response: The default choice for the user if they hit enter
            without typing anything. It must be included in options to be
            selected unless custom responses are allowed
        allow_custom_response: A flag to allow the user to type in their own
            option and use it. Allows users to type any custom response even if
            it is not included in options.  note: Only set if True
        multiple_ok: Allows a user to pick a comma separated list of options.
            Returns a list of responses if selected.  Can only be used if multiple
            options are given. note: Only set if True
        pre_helptext: Additional helptext to print before a prompt is asked
        helptext: The helptext that goes in the input line surrounded by parens.
            Helptext should display the default_response if provided.
        validate: An optional lambda that is run on any returned response.
            Validate must return true for all selected options to allow for
            selections.  Default: allows Any
        print_option: An optional callable to provide if your T_Option type may
            require a special formatting to printout.  Can be used to write a custom
            print function for any objects. note: it will not be applied to
            any helptext
        print_response: Print the selected response after selection. default: true

    Returns:
        Returns a list of selected options as provided in the options parameter
    """
    if _INPUT_DISABLED:
        raise InputDisabledError(_INPUT_DISABLED_MESSAGE)

    options = [x for x in options if x is not None]

    def print_helptext():
        if pre_helptext:
            print(f'{ pre_helptext }')

    if len(options) <= 1:
        # Only one option available, print one option alternative format
        print_helptext()
        return _list_options_single_response(
            input_text=input_text,
            options=options,
            allow_custom_response=allow_custom_response,
            multiple_ok=multiple_ok,
            default_response=default_response,
            helptext=helptext,
            validate=validate,
            print_option=print_option,
            print_response=print_response,
        )

    # Multiple Options detected
    response: Union[List[T_Option], List[str]] = []
    while not response:
        print_helptext()
        for count, option in enumerate(options):
            print(f'{count + 1}): {print_option(option)}')
        response_input = input(f'{input_text} ({helptext}): ').strip()
        if response_input == '' and default_response:
            response = [default_response]

        if not response:
            try:
                response_nums = [int(x.strip()) for x in response_input.split(',')]
                response = [options[x - 1] for x in response_nums]
            except Exception as _:  # type: ignore pylint: disable=broad-except
                pass
        if not response and allow_custom_response:
            response = [response_input]
        elif not all((x in options for x in response)):
            response = []

        if not all((validate(x) for x in response)):
            response = []

        if not multiple_ok and len(response) > 1:
            response = []

        if not response:
            print(response, 'received. Please input a response: ')
            continue

    if print_response:
        response_choices = ', '.join([print_option(x) for x in response])
        print(f'Selected: {response_choices}')
    if not multiple_ok and isinstance(response, list) and len(response) == 1:
        return response[0]
    return response


def query_yes_no(
    question: str,
    default: Optional[bool] = True,
):
    """A simple yes or no question input response generator

    Args:
        question: The question to ask
        default: The default awnser to provide if the users puts no response in

    Returns:
        Returns a true or false answer
    """
    if _INPUT_DISABLED:
        raise InputDisabledError(_INPUT_DISABLED_MESSAGE)

    if default is None:
        question_prompt = ' [y/n] '
    elif default:
        question_prompt = ' [Y/n] '
    else:
        question_prompt = ' [y/N] '
    while True:
        choice = input(question + question_prompt).lower()
        if default is not None and choice == '':
            return default
        elif 'yes'.startswith(choice.lower()):
            return True
        elif 'no'.startswith(choice.lower()):
            return False
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")


def prompt(question: str, default: Optional[str] = None) -> str:
    """Prompt a user for a response

    Args:
        question (str): Question to pose to the user
        default (Optional[str]): Default value for no response. Defaults to None.

    Returns:
        str: User response
    """
    if _INPUT_DISABLED:
        raise InputDisabledError(_INPUT_DISABLED_MESSAGE)

    if default is not None:
        question_prompt = f' [{default}] '
    else:
        question_prompt = ' '
    while True:
        response = input(question + question_prompt)
        if response == '':
            if default is not None:
                return default
            else:
                print('Please provide an answer.')
        else:
            return response
