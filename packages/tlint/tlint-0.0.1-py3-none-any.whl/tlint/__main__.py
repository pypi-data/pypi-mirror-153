import shutil
import sys
from tlint import TLint

__doc__ = """usage: tlint [init | -h]

Python linter with very few options.
All linting config goes in yaml config file.

- Lint project according to tlint.yaml
    tlint

- Generate default linting config
    tlint init

- Show tlint CLI help
    tlint help
    tlint -h
"""

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init':
            shutil.copy("tlint/conf/example.tlint.yaml", "tlint.yaml")
        elif sys.argv[1] in ('-h', 'help'):
            print(__doc__)
    else:
        TLint().lint()

if __name__ == "__main__":
    main()
