#!/bin/bash

MODEL_NAME=t5small
ENDPOINT=t5small
# https://stackoverflow.com/a/33826763
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -n|--model-name) MODEL_NAME="$2"; shift ;;
        -e|--endpoint) ENDPOINT="$2"; shift ;;
        -u|--uglify) uglify=1 ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done
torchserve --start --model-store ./model-store --models $ENDPOINT=$MODEL_NAME.mar --ncs