#!/bin/sh

gunicorn -w 4 envelope_builder:app -b 0.0.0.0:5000
