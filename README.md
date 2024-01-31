# FastAPI Project Setup

This guide will walk you through the process of setting up the FastAPI project with a virtual environment or with docker.

## Prerequisites

Make sure you have Python 3.7 or higher installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

For use with docker make sure you have docker desktop installed on your system. You can download docker desktop from [docker.com](https://www.docker.com/products/docker-desktop/).

## 1. Clone the Repository

```bash
git clone https://github.com/joshuaunity/seicast-api.git

cd seicast-api

# Create & Activate venv On Unix or MacOS 
python3 -m venv venv

source venv/bin/activate

# Create & Activate venv  On Windows
python -m venv venv

.\venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

## For Use with Docker

```bash
git clone https://github.com/joshuaunity/seicast-api.git

cd seicast-api

docker-compose up
```

This will spin up the containerized project and you are ready to start hitting the APIs


## API Paths

1. then&now forecast - http://127.0.0.1:8000/forecast/
2. tomorrow forecast - http://127.0.0.1:8000/tomorrow/
