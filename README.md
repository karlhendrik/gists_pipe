# Gists Pipe

[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=round)](https://github.com/karlhendrik/gists_pipe/issues)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![build-status](https://api.travis-ci.com/karlhendrik/gists_pipe.svg?branch=main)](https://www.travis-ci.com)


Gists Pipe is a simple application to fetch user Gists from GitHub and push each Gist to PipeDrive as deal. Application also features a live gists watching. 

## Installation

First you need to copy `.env.example` as `.env`. Then you'll need GitHub and PipeDrive API keys. Also don't forget to update COMPANY_NAME (this is neccesary to make requests to a your company PipeDrive), APP_URL & PROJECT_ROOT values.

Everything is tied together with [Docker](https://docs.docker.com/get-docker/) so you dont need any additional software to run this project. 

```bash
git clone https://github.com/karlhendrik/gists_pipe.git
cd gists_pipe/
cp .env.example .env
bash ./scripts/build.sh
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit)

