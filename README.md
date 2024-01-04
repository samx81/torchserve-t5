TorchServe server deployment

This is an adaptation from https://github.com/chiragjn/torchserve-t5-translation, with some changes. 
- The prefix part has been removed, since this deployment was for a fine-tuned t5-model for a specific seq2seq task
- The handler code was changed in order to support batching on the server side. However, the batching works only with single-datapoint queries which increases the network load.
- During the inference tests, the GPU memory was the bottleneck for increasing the performance through larger batch size or increasing the number of processes on the server side (see `config.properties`)

## Quick Start
Install dependency following 

https://github.com/pytorch/serve/tree/master?tab=readme-ov-file#-quick-start-with-torchserve

then
`pip install -r requirements.txt`

---
## Original repo readme

`run.sh` file contains the commands to convert pytorch models into `.mar` format and start the docker with all models in `model-storage`

`convert.sh` contains the command that converts Pytorch model, the Handler class code, and the tokenizer into a TorchServe artifact `model_name.mar`. The artifact is stored in the `model-store` directory and served by the TorchServe docker.

`config.properties` is the config file for the TorchServe server. The file is used as a parameter by the `docker run` command in `run.sh`

`requirements.txt` contains the dependency versions that allowed to successfully start a TS server.

`pytorch_model.bin` - these model files are just placeholders.


Outdated query example:
```shell
curl -v -X POST -H 'Content-Type: application/json' -d '{"text": "this is a test sentence", "from": "en", "to": "es"}' http://0.0.0.0:8080/predictions/t5smalltranslation/1.0
```
