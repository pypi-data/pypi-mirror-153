"""Leveraged Multi Family Real Estate Analysis.

Usage:
------

python -m lmfa 'multifamily_2.yaml', 'multifamily_4.yaml'


Contact:
--------

More information is available at:

- https://pypi.org/project/leveraged-multi-family-analysis/
- https://github.com/vamseeachanta/leveraged-multi-family-analysis


Version:
--------

- leveraged-multi-family-analysis v0.1.1
"""
from lmfa import multifamily


def main() -> None:
    multifamily.run_analysis()


if __name__ == "__main__":
    main()
