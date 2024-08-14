## How to run

Install pyenv
Install python 3.12

Install pipenv
`pip install pipenv`

`pyenv local 3.12`

`pipenv shell`

`python main.py`

## Running Jupyter Lab from Ubuntu server

SSH into server, creating tunnel to local port
`ssh -L 8888:localhost:8888 oasis.local`

From there you can follow the link jupyter lab generates
`http://localhost:8888/lab?token=ABCDEFGHIJKLMNOP`

## ToDo

If spark isn't running, execute `sbin/start-all.sh`
can view server GUI on localhost:8080
server connection at localhost:7077 (see gui)
