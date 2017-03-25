#!/bin/bash
service ssh start
celery worker -A tasks -c $workernum --loglevel info