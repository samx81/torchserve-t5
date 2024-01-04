#!/bin/bash
mkdir -p model-store
MODEL_DIR=./model
MODEL_NAME=t5small
MODEL_FILE=pytorch_model.bin
# MODEL_FILE=model.safetensors

# https://stackoverflow.com/a/33826763
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -d|--dir) MODEL_DIR="$2"; shift ;;
        -n|--model-name) MODEL_NAME="$2"; shift ;;
        -f|--model-file) MODEL_FILE="$2"; shift ;;
        -u|--uglify) uglify=1 ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

fn_list=($(ls $MODEL_DIR | grep -v $MODEL_FILE))
fns=$(printf ",./${MODEL_DIR}/%s" "${fn_list[@]}")
fns=${fns:1}

torch-model-archiver --model-name $MODEL_NAME --version 1.0 \
    --model-file ./model.py --handler ./handler.py \
    --serialized-file ./$MODEL_DIR/$MODEL_FILE \
    --extra-files "${fns},./setup_config.json"