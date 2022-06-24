#!/bin/bash

set -e -u -x -o pipefail

curl -F image=@$1 localhost:4000/classify