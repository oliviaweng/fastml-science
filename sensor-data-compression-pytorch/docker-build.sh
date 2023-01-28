#!/bin/bash 
docker build . --tag autoencoder
docker-compose up -d
