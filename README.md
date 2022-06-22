TorchServe server deployment

---

`run.sh` file contains the commands to convert pytorch models into `.mar` format and start the docker with all models in `model-storage`
`convert.sh` contains the command that converts Pytorch model, the Handler class code, and the tokenizer into a TorchServe artifact `model_name.mar`. The artifact is stored in the `model-store` directory and served by the TorchServe docker.

`config.properties` is the config file for the TorchServe server. The file is used as a parameter by the `docker run` command in `run.sh`

`requirements.txt` contains the dependency versions that allowed to successfully start a TS server.

`pytorch_model.bin` - these model files are just placeholders.



Outdated query example:
```shell
curl -v -X POST -H 'Content-Type: application/json' -d '{"text": "this is a test sentence", "from": "en", "to": "es"}' http://0.0.0.0:8080/predictions/t5smalltranslation/1.0
```
