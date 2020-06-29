# intro-website
A very simple website powered by Flask and Dash


## Installation

(in a separate environment)
```shell script
git clone https://github.com/mysterious-ben/intro-website
pip -r requirements.txt
```


## Start Server

1. Check/update `config.py`
2. Add `__config.py`
3. From the project folder, run `python -m src.app`
    - To downgrade priority below -10 (soft CPU limit): `nice -n 0 python -m src.app`
    - To limit RAM to 500MB: `ulimit -v 500000 && python -m src.app`
