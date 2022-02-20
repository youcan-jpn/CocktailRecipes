# backend

## Setup

1. create a docker volume
``` docker
docker volume create --name cocktail_db
```

2. build docker image(s)
``` bash
cd backend
docker-compose build
```

3. up docker containers
``` bash
docker-compose up -d
```