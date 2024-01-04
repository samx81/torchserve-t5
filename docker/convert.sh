#!/bin/bash
mkdir -p model-store
MODEL_DIR=$1
MODEL_NAME=$2
docker run -itd --name mar -v $(pwd):/home/model-server/src/ pytorch/torchserve:latest-gpu
docker exec -it mar torch-model-archiver --model-name $MODEL_NAME --version 1.0 --model-file ./src/$MODEL_DIR/model.py --serialized-file ./src/$MODEL_DIR/pytorch_model.bin --handler ./src/$MODEL_DIR/handler.py --extra-files "./src/$MODEL_DIR/config.json,./src/$MODEL_DIR/spiece.model,./src/$MODEL_DIR/tokenizer.json,./src/setup_config.json" --runtime python3 --export-path ./src/model-store/ -r ./src/requirements.txt -f
docker rm -f mar
