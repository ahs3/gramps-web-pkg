#!/bin/bash
CFG="config.cfg"
LANGUAGE=en python3 -O -m gramps_webapi --config $CFG run --port 5555
