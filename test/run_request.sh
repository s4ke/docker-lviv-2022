#!/bin/bash

set -e -u -x -o pipefail

curl -F image=@$1 127.0.0.1:4000/classify
