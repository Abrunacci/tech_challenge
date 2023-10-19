# Tech challenge
FastAPI offline challenge


### System Requirements
* [Docker](https://docs.docker.com/engine/install/)
* [Docker-compose](https://docs.docker.com/compose/install/)

### Run application
```shell
git pull https://github.com/Abrunacci/tech_challenge.git
cd tech_challenge
docker-compose build
docker-compose up
```

### Run tests
```shell
docker-compose up -d
docker-compose exec api pytest . -v
```


