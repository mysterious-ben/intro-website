# intro-website
A very simple website powered by Flask and Dash


## Installation

1. Clone the project
```shell script
git clone https://github.com/mysterious-ben/intro-website
cd intro-website
```
2. Check the public config `src/config.py`
3. Create the private config `src/__config.py`


## Start Server

1. Option 1: run in an environment
```shell script
pip -r requirements.txt
python -m src.app
```
- To downgrade priority below -10 (soft CPU limit): `nice -n 0 python -m src.app`
- To limit RAM to 500MB: `ulimit -v 500000 && python -m src.app`

2. Option 2: Run in a docker container
```shell script
docker-compose up
```
