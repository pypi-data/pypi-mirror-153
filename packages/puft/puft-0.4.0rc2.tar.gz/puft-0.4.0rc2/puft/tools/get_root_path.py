from puft.core.assembler.assembler import Assembler

def get_root_path() -> str:
    """Return app project root path."""
    return Assembler.instance().get_root_path()