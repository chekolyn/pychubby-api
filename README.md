# Pychubby-api

Small Api for [PyChubby](https://github.com/jankrepl/pychubby).


### Prerequisites

Easiest way is to have working docker daemon for install instruction go [here](https://docs.docker.com/install/)

## Docker Image Build

docker build -t pychubby-api:latest .


## Running docker image

Run docker image and expose port 8080
```
docker run  -d -p 8080:8080 pychubby-api:latest
```
Give an example

## Test running daemon
```
curl localhost:8080/healthz
```

## Access Swagger UI
[http://localhost:8080/api/ui/](http://localhost:8080/api/ui)

## Built With

* [connexion](https://github.com/zalando/connexion). - The api framework used

## Authors

* **Sergio Aguilar** - *Initial work* - [@chekolyn](https://github.com/chekolyn)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Shout out to [jankrepl](https://github.com/jankrepl) for creating PyChubby
