

### install the following packages
```shell

pip install langchain
pip install openai
pip install -U langchain-community
pip install -U langchain-openai
```

### create OpenAI API key
https://platform.openai.com/api-keys
then add it to `secret_key.py`

### How to generate flows data bases
- bring up an OpenShift cluster
- clone https://github.com/msherif1234/network-observability-cli/tree/cli-intg
- `make build`
- then run `./build/oc-netobserv-flows-db`
that will generate flows.db locally then copy to ai repo or create symlink
