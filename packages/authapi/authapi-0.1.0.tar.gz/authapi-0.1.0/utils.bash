#!/usr/bin/env bash
SERVICE_NAME="authapi"
PORT=3000

function docker_build(){
    echo "Building docker image"
    docker image build -t ${SERVICE_NAME} .
}

function docker_run(){
    docker_build
    echo "Running docker image"
    docker run -p ${PORT}:${PORT} --name ${SERVICE_NAME} -t ${SERVICE_NAME}
    docker rm -f ${SERVICE_NAME}
}
