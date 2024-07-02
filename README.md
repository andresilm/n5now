# Traffic Violations application
 N5  Code Challenge


## Run in local virtual environment


### Create virtual environment and install dependencies
```
make install
```

### Activate virtual environment

```
source venv/bin/activate
```

### Run application

```
uvicorn main:app --host 127.0.0.1 --port 8080
```


## Run in docker container

### Create docker image
```
make docker-build
```

### Launch container and start application

```
make docker-run
```
