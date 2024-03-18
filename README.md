

### install the following packages
```shell

pip install langchain
pip install openai
pip install -U langchain-community
pip install -U langchain-openai
pip install -U slack_bolt
pip install -U tabulate
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

### How to run
```python
python3 chat_netobserv.py
```

### How to run after setting up slack
Note: need to add set slack environment variables in `slack_key.py`
```python
python3 netobserv_slack.py
```