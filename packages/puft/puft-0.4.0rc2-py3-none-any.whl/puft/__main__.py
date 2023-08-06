"""
Invoke cli interface when puft executed as a script:
```py
python -m puft
```
"""
try:
    from .core.cli import cli
except ImportError:
    from puft.core.cli import cli


if __name__ == "__main__":
    cli.main()