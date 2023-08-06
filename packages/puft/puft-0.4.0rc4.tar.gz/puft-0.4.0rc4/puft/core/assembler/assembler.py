from __future__ import annotations
import os
from typing import Dict, TYPE_CHECKING, Any

from warepy import (
    join_paths, format_message, load_yaml, get_enum_values, Singleton
)
from flask_socketio import SocketIO

from puft.core.sock.socket import Socket
from puft.tools.hints import CLIModeEnumUnion
from puft.tools.log import log
from puft.core.app.app_mode_enum import AppModeEnum
from puft.core.cli.cli_run_enum import CLIRunEnum
from puft.core.error.error import Error
from puft.tools.error_handlers import handle_wildcard_error
from puft.core.cell.named_cell import NamedCell
from puft.core.cell.config_cell import ConfigCell
from puft.core.app.puft_sv_cell import PuftSvCell
from puft.core.db.db_sv_cell import DbSvCell
from puft.core.sock.sock_sv_cell import SocketSvCell
from puft.core.sv.sv_cell import SvCell
from puft.core.view.view_cell import ViewCell
from puft.core.emt.emt_cell import EmtCell
from puft.core.error.error_cell import ErrorCell

from puft.core.db.db import Db
from puft.core.app.puft import Puft
from puft.tools.hints import CLIModeEnumUnion
from .config_extension_enum import ConfigExtensionEnum

if TYPE_CHECKING:
    from .build import Build


class Assembler(Singleton):
    """Assembles all project instances from given `Builder` type's class and
    initializes it.
    
    Acts automatically and shouldn't be inherited directly by project in any
    form.
    """
    DEFAULT_LOG_PARAMS = {
        "path": "./var/logs/system.log",
        "level": "DEBUG",
        "format":
            "{time:%Y.%m.%d at %H:%M:%S:%f%z} | {level} | {extra} >> {message}",
        "rotation": "10 MB",
        "serialize": False
    }

    def __init__(
        self, 
        mode_enum: CLIModeEnumUnion, host: str, port: int,
        build: Build,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        # Define attributes for getter methods to be used at builder.
        # Do not set extra_configs_by_name to None at initialization, because
        # `get()` method called from this dictionary.
        self.extra_configs_by_name = {}
        self.root_path = build.root_path
        self.sv_cells = build.sv_cells
        self.view_cells = build.view_cells
        self.error_cells: list[ErrorCell] = build.error_cells
        self.emt_cells = build.emt_cells
        self.mode_enum = mode_enum
        self.shell_processors = build.shell_processors
        self.cli_cmds = build.cli_cmds
        self.ctx_processor_func = build.ctx_processor_func
        self.each_request_func = build.each_request_func
        self.first_request_func = build.first_request_func
        self.default_wildcard_error_handler_func = handle_wildcard_error
        self.sock_cells = build.sock_cells
        self.default_sock_error_handler = build.default_sock_error_handler

        self.socket_enabled: bool = False

        self._assign_config_cells(build.config_dir)

        # Traverse given configs and assign enabled builtin cells.
        self._assign_builtin_sv_cells(mode_enum, host, port)

    @log.catch
    def get_puft(self) -> Puft:
        return self.puft

    @log.catch
    def get_db(self) -> Db:
        return self.db

    @log.catch
    def get_root_path(self) -> str:
        return self.root_path

    @log.catch
    def get_mode_enum(self) -> CLIModeEnumUnion:
        return self.mode_enum

    @log.catch
    def _assign_config_cells(self, config_dir: str) -> None:
        """Traverse through config files under given config_dir and create 
        ConfigCells from them.

        Name taken from filename of config and should be the same as specified 
        at config's target sv_cell.name.

        Names can contain additional extension like `name.prod.yaml` according
        to appropriate Puft modes. These configs launched per each mode. Config
        without this extra extension, considered `prod` moded.
        """
        self.config_cells: list[ConfigCell] = []

        config_path: str = join_paths(self.root_path, config_dir)
        source_map_by_name: dict[str, dict[AppModeEnum, str]] = \
            self._find_config_files(config_path)

        for name, source_map in source_map_by_name.items():
            self.config_cells.append(ConfigCell(
                name=name,
                source_by_app_mode=source_map))

    def _find_config_files(
            self, config_path: str) -> dict[str, dict[AppModeEnum, str]]:
        """Accept path to config dir and return dict describing all paths to
        configs for all app modes per sv name.
        
        Return example:
        ```python
        {
            "custom_sv_name": {
                AppModeEnum.PROD: "./some/path",
                AppModeEnum.DEV: "./some/path",
                AppModeEnum.TEST: "./some/path"
            }
        }
        ```
        """
        source_map_by_name = {} 
        for filename in os.listdir(config_path):
            # Pick files only under config_dir.
            if os.path.isfile(join_paths(config_path, filename)):
                parts = filename.split(".")
                file_path = join_paths(config_path, filename)

                if len(parts) == 1:
                    # Skip files without extension.
                    continue
                # Check if file has supported extension.
                elif len(parts) == 2:
                    # Config name shouldn't contain dots and thus we can grab
                    # it right here.
                    config_name = parts[0]
                    if parts[1] in get_enum_values(ConfigExtensionEnum):
                        # Add file without app mode automatically to
                        # `prod`.
                        if config_name not in source_map_by_name:
                            source_map_by_name[config_name] = dict()
                        source_map_by_name[config_name][
                            AppModeEnum.PROD] = file_path
                    else:
                        # Skip files with unsupported extension.
                        continue
                elif len(parts) == 3:
                    # Config name shouldn't contain dots and thus we can grab
                    # it right here.
                    config_name = parts[0]
                    if parts[1] in get_enum_values(AppModeEnum) \
                            and parts[2] in get_enum_values(
                                ConfigExtensionEnum):
                        # File has both normal extension and defined
                        # app mode.
                        if config_name not in source_map_by_name:
                            source_map_by_name[config_name] = dict()
                        source_map_by_name[config_name][
                            AppModeEnum(parts[1])] = file_path
                    else:
                        # Unrecognized app mode or extension,
                        # maybe raise warning?
                        continue
                else:
                    # Skip files with names containing dots, e.g.
                    # "dummy.new.prod.yaml".
                    continue
        return source_map_by_name

    @log.catch
    def _assign_builtin_sv_cells(
            self, mode_enum: CLIModeEnumUnion, host: str, port: int) -> None:
        """Assign builting sv cells if configuration file for its sv
        exists.
        """
        self.builtin_sv_cells: list[Any] = [PuftSvCell(
            name="puft",
            sv_class=Puft,
            mode_enum=mode_enum,
            host=host,
            port=port
        )]
        log_layers: list[str] = []

        # Enable only modules with specified configs.
        if self.config_cells:
            try:
                NamedCell.find_by_name("db", self.config_cells)
            except ValueError:
                pass
            else:
                self.builtin_sv_cells.append(DbSvCell(
                    name="db",
                    sv_class=Db
                ))
                log_layers.append('db')

            try:
                NamedCell.find_by_name('socket', self.config_cells)
            except ValueError:
                pass
            else:
                self.builtin_sv_cells.append(SocketSvCell(
                    name='socket',
                    sv_class=Socket))
                self.socket_enabled = True
                log_layers.append('socket')
            
            if log_layers:
                log.info(f'Enabled layers: {", ".join(log_layers)}')

    @staticmethod
    @log.catch
    def build(
            configs_by_name: Dict[str, dict] | None = None,
            root_path: str | None = None) -> None:
        """Initialize all given to Assembler instances in their dependencies.
        
        Reassign assembler's attributes to given ones and run it's setup
        operations to assemble app and other project's instances.

        Args:
            configs_by_name (optional):
                Configs to be appended to appropriate ones described in Build
                class. Defaults to None.
                Contain config name as key (which is compared to ConfigCell
                name field) and configuration mapping as value, e.g.:
        ```python
        configs_by_name = {
            "app": {"TESTING": True},
            "db": {"db_uri": "sqlite3:///:memory:"}
        }
        ```
            root_path (optional):
                Root path to execute project from. Defaults to `os.getcwd()`.
                Required in cases of calling this function not from actual
                project root (e.g. from tests) to set root path explicitly.
        """
        # Get Assembler instance without args, because it should be initialized before (in root create_app function).
        assembler = Assembler.instance()

        if root_path:
            assembler.root_path = root_path
        if configs_by_name:
            assembler.extra_configs_by_name = configs_by_name

        assembler._build_all()
        
    @log.catch
    def _build_all(self) -> None:
        """Send commands to build all given instances."""
        self._build_log()
        self._build_svs()
        self._build_views()
        self._build_errors()
        self._build_emts()
        self._build_shell_processors()
        self._build_cli_cmds()
        self._build_socks()

        # Call postponed build from created App.
        try:
            self.puft.postbuild()
        except NotImplementedError:
            pass

    @log.catch
    def _build_log(self) -> None:
        """Call chain to build log."""
        # Try to find log config cell and build log class from it
        if self.config_cells:
            try:
                log_config_cell = NamedCell.find_by_name("log", self.config_cells)
            except ValueError:
                log_config = None
            else:
                # Parse config mapping from cell and append extra configs,
                # if they are given
                app_mode_enum: AppModeEnum
                if type(self.mode_enum) is CLIRunEnum:
                    app_mode_enum = AppModeEnum(self.mode_enum.value) 
                else:
                    # Assign dev app mode for all other app modes
                    app_mode_enum = AppModeEnum.DEV
                log_config = log_config_cell.parse(
                    app_mode_enum=app_mode_enum,
                    root_path=self.root_path, 
                    update_with=self.extra_configs_by_name.get("log", None)
                )
            self._init_log_class(config=log_config)

    @log.catch
    def _init_log_class(self, config: dict | None = None) -> None:
        """Build log with given config.
        
        If config is None, build with default parameters."""
        # Use full or partially (with replacing missing keys from default) given config.
        log_kwargs = self.DEFAULT_LOG_PARAMS
        if config:
            for k, v in config.items():
                log_kwargs[k] = v
        log.configure(**log_kwargs)

    @log.catch
    def _build_svs(self) -> None:
        self._run_builtin_sv_cells()
        self._run_custom_sv_cells()

    @log.catch
    def _build_socks(self) -> None:
        if self.sock_cells and self.socket_enabled:
            for cell in self.sock_cells:
                socketio: SocketIO = self.socket.get_socketio()

                # Register class for socketio namespace
                # https://flask-socketio.readthedocs.io/en/latest/getting_started.html#class-based-namespaces
                socketio.on_namespace(cell.handler_class(cell.namespace))
                # Also register error handler for the same namespace
                socketio.on_error(cell.namespace)(cell.error_handler) 

    @log.catch
    def _perform_db_postponed_setup(self) -> None:
        """Postponed setup is required, because Db uses Flask app to init
        native SQLAlchemy db inside, so it's possible only after App
        initialization.

        The setup_db requires native flask app to work with.
        """
        self.db.setup(flask_app=self.puft.get_native_app())
    
    @log.catch
    def _run_builtin_sv_cells(self) -> None:
        for cell in self.builtin_sv_cells:
            # Check for domain's config in given cells by comparing names and
            # apply to sv config if it exists
            config = self._assemble_sv_config(name=cell.name) 

            # Each builtin sv should receive essential fields for their
            # configs, such as root_path, because they cannot import Assembler
            # due to circular import issue and get this fields by themselves
            config["root_path"] = self.root_path

            # Initialize sv.
            if type(cell) is PuftSvCell:
                # Run special initialization with mode, host and port for Puft
                # sv
                self.puft: Puft = cell.sv_class(
                    mode_enum=cell.mode_enum, host=cell.host, port=cell.port, 
                    config=config,
                    ctx_processor_func=self.ctx_processor_func,
                    each_request_func=self.each_request_func,
                    first_request_func=self.first_request_func)
            elif type(cell) is DbSvCell:
                self.db: Db = cell.sv_class(config=config)
                # Perform Db postponed setup
                self._perform_db_postponed_setup()
            elif type(cell) is SocketSvCell:
                self.socket = cell.sv_class(config=config, app=self.puft)
            else:
                cell.sv_class(config=config)

    @log.catch
    def _run_custom_sv_cells(self) -> None:
        if self.sv_cells:
            for cell in self.sv_cells:
                if self.config_cells:
                    sv_config = self._assemble_sv_config(name=cell.name) 
                else:
                    sv_config = {}

                cell.sv_class(config=sv_config)

    @log.catch
    def _assemble_sv_config(
            self,
            name: str, is_errors_enabled: bool = False) -> dict[str, Any]:
        """Check for sv's config in config cells by comparing its given
        name and return it as dict.

        If appropriate config hasn't been found, raise ValueError if
        `is_errors_enabled = True` or return empty dict otherwise.
        """
        try:
            config_cell_with_target_name: ConfigCell = NamedCell.find_by_name(
                name, self.config_cells)
        except ValueError:
            # If config not found and errors enabled, raise error.
            if is_errors_enabled:
                message = format_message(
                    "Appropriate config for given name {} hasn't been found.",
                    name)
                raise ValueError(message)
            else:
                config: dict[str, Any] = {}
        else:
            if type(config_cell_with_target_name) is not ConfigCell:
                raise TypeError(format_message(
                    "Type of cell should be ConfigCell, but {} received",
                    type(config_cell_with_target_name)))
            else:
                app_mode_enum: AppModeEnum
                if type(self.mode_enum) is CLIRunEnum:
                    app_mode_enum = AppModeEnum(self.mode_enum.value) 
                else:
                    # Assign dev app mode for all other app modes.
                    app_mode_enum = AppModeEnum.DEV
                config = config_cell_with_target_name.parse(
                    root_path=self.root_path, 
                    update_with=self.extra_configs_by_name.get(name, None),
                    app_mode_enum=app_mode_enum)
        return config

    @log.catch
    def _fetch_yaml_project_version(self) -> str:
        """Fetch project version from info.yaml from the root path and return it. 

        TODO:
            Replace this logic with senseful one. Better use configuration's
            version? Or __init__.py or main.py specified.
        """
        info_data = load_yaml(join_paths(self.root_path, "./info.yaml"))
        project_version = info_data["version"]
        return project_version

    @log.catch
    def _build_views(self) -> None:
        """Build all views by registering them to app."""
        if self.view_cells:
            for view_cell in self.view_cells:
                self.puft.register_view(view_cell)

    @log.catch
    def _build_emts(self) -> None:
        """Build emts from given cells and inject Puft application controllers to each."""
        if self.emt_cells:
            for cell in self.emt_cells:
                cell.emt_class(puft=self.puft)

    @log.catch
    def _build_shell_processors(self) -> None:
        if self.shell_processors:
            self.puft.register_shell_processor(*self.shell_processors)

    @log.catch
    def _build_cli_cmds(self) -> None:
        if self.cli_cmds:
            self.puft.register_cli_cmd(*self.cli_cmds)

    def _build_errors(self) -> None:
        # TODO: Test case when user same error class registered twice (e.g. in
        # duplicate cells)
        is_wildcard_specified = False
        for error_cell in self.error_cells:
            if type(error_cell.error_class) is Error:
                is_wildcard_specified = True
            self.puft.register_error(
                error_cell.error_class, error_cell.handler_function)
        # If wildcard handler is not specified, apply the default one
        if not is_wildcard_specified:
            self.puft.register_error(
                Error, self.default_wildcard_error_handler_func)
