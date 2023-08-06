import io
from os import PathLike
from pathlib import Path
from typing import Union, IO, Optional

import yamale


class SyntaxValidationResult:
    """Checks a yml file against a provided yml-schema

    The SyntaxValidationResult class is used to validate
    experiment runs and returns an ErrorDescription object
    that provides detailed information on why the check failed.

    The class currently functions as a yamale wrapper.

    Parameters
    ----------
    is_valid: (bool) boolean flag whether the experiment is valid or not.
    error_message: (str) detailed error description on why the validation failed.
                   NONE if no error occurred.
    """

    def __init__(self, is_valid: bool, error_message: Optional[str]):
        self.is_valid = is_valid
        self.error_message = error_message

    def __bool__(self):
        return self.is_valid

    @staticmethod
    def validate_syntax(
        experiment_config: Union[str, IO[str], PathLike],
        experiment_schema: Path,
    ):
        try:
            yamale_schema = yamale.make_schema(
                experiment_schema, parser="ruamel"
            )
            if isinstance(experiment_config, io.TextIOBase):
                yamale_data = yamale.make_data(
                    content=experiment_config.read(),
                    parser="ruamel",
                )
            else:
                if (
                    isinstance(experiment_config, Path)
                    and experiment_config.is_dir()
                ):
                    raise RuntimeError(
                        "Cannot validate directories, only files."
                    )
                try:
                    yamale_data = yamale.make_data(
                        path=experiment_config, parser="ruamel"
                    )
                except ValueError as e:
                    return SyntaxValidationResult(
                        is_valid=False, error_message=str(e)
                    )
            yamale.validate(yamale_schema, yamale_data, strict=True)
            return SyntaxValidationResult(
                is_valid=True,
                error_message=None,
            )
        except ValueError as e:
            return SyntaxValidationResult(
                is_valid=False,
                error_message=str(e),
            )


class SyntaxValidationError(Exception):
    def __init__(self, validation_result: SyntaxValidationResult):
        super().__init__(validation_result.error_message)
        self.validation_result = validation_result

    def __str__(self):
        return self.validation_result.error_message
