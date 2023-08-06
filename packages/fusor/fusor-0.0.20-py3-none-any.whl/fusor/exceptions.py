"""Exceptions for FUSOR models and helper functions."""


class IDTranslationException(Exception):
    """Indicate translation failure for provided ID value"""

    pass


class FUSORParametersException(Exception):
    """Signal incorrect or insufficient parameters for model constructor methods."""

    pass
