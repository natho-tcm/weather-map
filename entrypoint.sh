#!/bin/bash

echo "Waiting for postgres"
sleep 2

sanic app.web.server:app --host=0.0.0.0 --port=8080