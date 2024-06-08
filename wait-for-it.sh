#!/bin/sh
sleep 10
celery --broker=redis://cache:6379 flower