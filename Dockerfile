# Image for pychubby-api
FROM centos/python-36-centos7
USER root

## Install libXrender dependency
RUN yum install cmake -y && yum install libXrender -y  && rm -rf /var/cache/yum

# copy gunicorn hello world app
WORKDIR /opt/app-root/src
COPY . /opt/app-root/src

# Install gunicorn server from pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Fetch pychubby pretrained data
RUN python -c "from pychubby import data; import urllib.request as urllib; data.get_pretrained_68('/opt/app-root/src/.pychubby/')"

# Run gunicorn on port 8080
EXPOSE 8080
ENTRYPOINT ["/opt/app-root/bin/gunicorn", "--workers=2", "--threads=4", "--worker-class=gthread", "app:app",  "--bind", "0.0.0.0:8080", "--access-logfile=-"]

# Test healthcheck url
HEALTHCHECK CMD curl --fail http://localhost:8080/healthz || exit 1

