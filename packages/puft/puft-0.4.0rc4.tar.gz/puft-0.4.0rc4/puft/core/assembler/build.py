import os
from typing import Callable
from puft.core.sock.default_sock_error_handler import default_sock_error_handler
from puft.core.sock.sock_cell import SockCell

from puft.core.sv.sv_cell import SvCell
from puft.core.view.view_cell import ViewCell
from puft.core.emt.emt_cell import EmtCell
from puft.core.error.error_cell import ErrorCell


class Build:
    """Proxy mapping class with collection of initial project instances to be
    builded by assembler.
    
    Should be inherited by build class in root folder.
    """
    def __init__(
        self,
        version: str = "",
        config_dir: str = "./src/configs",
        sv_cells: list[SvCell] = [],
        view_cells: list[ViewCell] = [],
        emt_cells: list[EmtCell] = [],
        error_cells: list[ErrorCell] = [],
        shell_processors: list[Callable] = [],
        cli_cmds: list[Callable] = [],
        sock_cells: list[SockCell] = [],
        default_sock_error_handler: Callable = default_sock_error_handler,
        ctx_processor_func: Callable | None = None,
        each_request_func: Callable | None = None,
        first_request_func: Callable | None = None,
    ) -> None:
        # Use native root module path.
        # Because this class imported from root directory, root_path below will be assigned from there during class's
        # initialization.
        # NOTE: This path can be overrided by assembler in order of getting arguments on it's own initialization.
        self.root_path = os.getcwd()

        self.version = version
        self.config_dir = config_dir
        self.sv_cells = sv_cells
        self.view_cells = view_cells
        self.emt_cells = emt_cells
        self.error_cells = error_cells
        self.shell_processors = shell_processors
        self.cli_cmds = cli_cmds
        self.ctx_processor_func = ctx_processor_func
        self.each_request_func = each_request_func
        self.first_request_func = first_request_func
        self.sock_cells = sock_cells
        self.default_sock_error_handler = default_sock_error_handler
