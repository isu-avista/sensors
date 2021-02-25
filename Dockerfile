# get base image
FROM python:3

# Arguments
ARG dbtype
ARG dbname
ARG dbip
ARG dbport
ARG dbuser
ARG dbpass
ARG hostname
ARG hostport

# create working directory
WORKDIR ./

# install dependencies
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y apt-utils
RUN apt-get install -y python3 python3-pip python3-dev python3-wheel python3-venv gunicorn3 python3-setuptools python3-smbus git ssh libatlas-base-dev libpq-dev gpiod libgpiod-dev

# copy requirements
COPY ./requirements.txt ./requirements.txt

# install python dependencies
RUN pip3 install -r requirements.txt

# copy application files
COPY ./ ./

# Generate the config files
RUN python3 generate_configs.py -t $dbtype -n $dbname -i $dbip -o $dbport -p $dbpass -u $dbuser -s $hostname -r $hostport
