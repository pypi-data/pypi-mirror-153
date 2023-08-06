"""Load the ytdl-server configuration from a config file and env-vars"""

from __future__ import annotations

__all__ = ('Config',)

import logging
import os
from typing import TYPE_CHECKING

import yaml

from .config_option import CELERY_OPTIONS, FLASK_OPTIONS, OPTIONS

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable
    from typing import Any, Final, Mapping, Optional

    from .config_option import FlaskCeleryOption, Option


# TODO: Add unit tests for Config
class Config:
    """Class that loads application config settings from env vars and
    from a config file"""

    __slots__ = (
        '_logger', 'database_uri', 'flask_config', 'celery_config',
        'download_dir', 'force_download_dir', 'ytdl_default_opts',
        'allow_user_opts', 'ytdl_enable_whitelist', 'ytdl_whitelist',
        'ytdl_whitelist_add', 'ytdl_whitelist_remove', 'ytdl_sensitive_opts',
        'custom_default_opts', 'custom_enable_whitelist', 'custom_whitelist',
        'ytdl_module', 'ytdl_class', 'daterange_module', 'daterange_class',
        'metadata_module', 'metadata_class'
    )

    database_uri: str
    """URI of the SQLAlchemy database"""
    flask_config: dict[str, Any]
    """Flask config options that are passed directly to Flask"""
    celery_config: dict[str, Any]
    """Celery config options that are passed directly to Celery"""
    download_dir: str
    """Dir that videos will be downloaded to by default"""
    force_download_dir: bool
    """Whether or not to force videos to be downloaded to `download_dir`"""
    allow_user_opts: bool
    """Whether or not to allow users to supply their own ytdl_opts and
    custom_opts"""
    ytdl_default_opts: dict[str, Any]
    """Default ytdl_opts"""
    ytdl_enable_whitelist: bool
    """Whether or not to use a whitelist for user-supplied ytdl_opts"""
    ytdl_whitelist: frozenset[str]
    """Set of whitelisted user ytdl_opts"""
    ytdl_whitelist_add: frozenset[str]
    """Additional ytdl_opts to add to `ytdl_whitelist`"""
    ytdl_whitelist_remove: frozenset[str]
    """Blacklisted ytdl_opts to remove from `ytdl_whitelist`"""
    ytdl_sensitive_opts: tuple[str, ...]
    """List of sensitive ytdl_opts whose values will be censored"""
    custom_default_opts: dict[str, Any]
    """Default custom_opts"""
    custom_enable_whitelist: bool
    """Whether or not to use a whitelist for custom_opts"""
    custom_whitelist: frozenset[str]
    """Set of whitelisted user custom_opts"""
    ytdl_module: str
    """The module that contains the YoutubeDL class"""
    ytdl_class: str
    """The YoutubeDL class to use"""
    daterange_module: str
    """The module that contains the DateRange class

    Defaults to the same value as `ytdl_module`
    """
    daterange_class: str
    """The DateRange class to use

    This is used for the 'datebefore' and 'dateafter' custom_opts
    """
    metadata_module: str
    """The module that contains the MetadataParser postprocessor class

    Defaults to the same value as `ytdl_module`
    """
    metadata_class: str
    """The MetadataParser postprocessor class to use

    This is used for the 'parse_metadata' and 'replace_in_metadata'
    custom_opts
    """

    _CONFIG_ENV_VAR: Final = 'YTDL_CONFIG'
    """Name of the env var that contains the filepath of the YAML config
    file that will be loaded (if it exists)"""

    _logger: Optional[logging.Logger]

    def __init__(
        self, *, logger: Optional[logging.Logger] = None,
        config_dict: Optional[Mapping[Any, Any]] = None,
        load_env_vars: bool = True
    ) -> None:
        """
        logger: Logger to log debug messages to. If `None`, no messages
            will be logged
        config_dict: Use this dict instead of loading the config file
        load_env_vars: Whether or not to load config values from their
            corresponding env vars

        `config_dict` and `load_env_vars` are intended to be used for
        testing
        """
        self._logger = logger
        if config_dict is None:
            config_dict = self._load_config_dict()

        for option in OPTIONS:
            value = self._get_value(option, config_dict, load_env_vars)
            setattr(self, option.name, value)

        if load_env_vars:
            self._load_flask_env_vars()
            self._load_celery_env_vars()

        self._run_manual_hacks()

    def _load_config_dict(self) -> dict[Any, Any]:
        """Load the YAML config file from the env var `_CONFIG_ENV_VAR`

        If the env var isn't set, returns an empty dict
        """
        if self._CONFIG_ENV_VAR in os.environ:
            config_path = os.environ[self._CONFIG_ENV_VAR]
            if config_path:
                self.log(
                    logging.INFO,
                    'Loading config file from env var: %s', config_path
                )
                with open(config_path, 'r') as file:
                    config_dict = yaml.safe_load(file)

                if not isinstance(config_dict, dict):
                    type_name = type(config_dict).__name__
                    raise ValueError(
                        'Invalid top-level type. '
                        f'Expected dict. Got {type_name}'
                    )
                return config_dict

        return {}

    def _get_value(
        self, option: Option, config_dict: Mapping[Any, Any],
        load_env_var: bool = True
    ) -> Any:
        """Get the value of the given option from the config dict or
        the corresponding env var

        Env vars have priority over the config dict

        If the option doesn't exist in the dict or as an env var, the
        default value for the option be set if it has one. Otherwise,
        an error will be raised

        If `load_env_var` is `False`, the env var won't be used
        """
        found_value = False
        is_default = False

        # Get the value from the env var if it exists
        if load_env_var and option.env_var is not None:
            if option.env_var in os.environ and os.environ[option.env_var]:
                value = option.get_env()
                found_value = True
                self.log(
                    logging.INFO, '%s: Found env var: %s. Value: %r',
                    option.name, option.env_var, value
                )

        if not found_value:
            if option.nested_in(config_dict, assert_type=True):
                # Get the value from the config file
                value = option.nested_get(config_dict)
                self._check_type(option, value)
                found_value = True

        if not found_value:
            if option.required:
                # Raise an error when the option is required, but wasn't
                # found
                raise KeyError(
                    f'Missing required config option: {option.name}'
                )
            else:
                value = option.get_default()
                is_default = True

        if not is_default:
            converted_value = option.convert_value(value)
            self.log(
                logging.INFO,
                '%s: Got value: %r', option.name, converted_value
            )
            return converted_value
        else:
            return value

    def _check_type(self, option: Option, value: Any) -> None:
        """Verify that the value of the option is the correct type"""
        if type(value) is not option.type:
            raise TypeError(
                f'The config option {option.name!r} has an invalid type. '
                f'Expected {option.type.__name__}. '
                f'Got {type(value).__name__}'
            )

        # Verify that all dicts only contain string keys
        #
        # Flask and Celery both only use string keys for their
        # configs
        if type(value) is dict:
            for key in value.keys():
                if type(key) is not str:
                    raise ValueError(
                        f"Invalid config option: '{option.name}.{key}'."
                        ' All keys must be strings'
                    )

    def _load_generic_env_vars(
        self, options: Iterable[FlaskCeleryOption], config_dict_name: str
    ) -> None:
        """Load all Flask and Celery env vars

        The env-var values are added to `flask_config` and
        `celery_config` respectively
        """
        config_dict: dict[str, Any] = getattr(self, config_dict_name)

        for option in options:
            if option.env_var in os.environ and os.environ[option.env_var]:
                value = option.get_env()
                self.log(
                    logging.INFO, '%s.%s: Found env var. Value: %r',
                    config_dict_name, option.name, value
                )
                config_dict[option.name] = value

    def _load_flask_env_vars(self) -> None:
        self._load_generic_env_vars(FLASK_OPTIONS, 'flask_config')

    def _load_celery_env_vars(self) -> None:
        self._load_generic_env_vars(CELERY_OPTIONS, 'celery_config')

    def _run_manual_hacks(self) -> None:
        """Option-specific hacks that can't be done automatically via
        `_Option`"""
        # Have Flask-SQLAlchemy use the database_uri
        self.flask_config['SQLALCHEMY_DATABASE_URI'] = self.database_uri

        # Have Celery use the SQL database as the result-backend by
        # default
        if 'result_backend' not in self.celery_config:
            result_backend = f'db+{self.database_uri}'
            self.log(
                logging.DEBUG,
                "Automatically setting `celery_config.result_backend` to %r",
                result_backend
            )
            self.celery_config['result_backend'] = result_backend

        # Have `daterange_module` and `metadata_module` use the same
        # module as `ytdl_module` by default
        for module in ('daterange_module', 'metadata_module'):
            if getattr(self, module) is None:
                self.log(
                    logging.DEBUG,
                    "Automatically setting `%s` to %r",
                    module, self.ytdl_module
                )
                setattr(self, module, self.ytdl_module)

    def items(self) -> Generator[tuple[str, Any], None, None]:
        """Return all config options as key-value pairs"""
        for option in OPTIONS:
            value = getattr(self, option.name)
            yield option.name, value

    def __repr__(self) -> str:
        options = []
        for option, value in self.items():
            options.append(f'{option}={value!r}')

        return f'Config({", ".join(options)})'

    def log(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        if self._logger is not None:
            self._logger.log(level, msg, *args, **kwargs)
