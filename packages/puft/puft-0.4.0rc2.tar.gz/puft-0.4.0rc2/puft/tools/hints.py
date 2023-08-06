from puft.core.cli.cli_db_enum import CLIDbEnum
from puft.core.cli.cli_run_enum import CLIRunEnum
from puft.core.cli.cli_helper_enum import CLIHelperEnum

CLIModeEnumUnion = CLIDbEnum | CLIRunEnum | CLIHelperEnum
