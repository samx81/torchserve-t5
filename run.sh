#!/bin/bash
#docker build -t torchserve:latest-gpu .
#git lfs init
#git clone https://huggingface.co/t5-small
./convert.sh t5_model t5_model


docker run -it --gpus '"device=0"' --restart=always --name torchserve --shm-size=3g   --ulimit memlock=-1     --ulimit stack=67108864     -p 83:8080     -p 8081:8081     -p 8082:8082     -p 7070:7070     -p 7071:7071 -v $(pwd):/home/model-server/src/ pytorch/torchserve:latest-gpu torchserve --ts-config=<FULL_PATH>/config.properties
