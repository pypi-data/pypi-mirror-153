# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hao']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML',
 'chardet',
 'decorator',
 'regex',
 'requests',
 'tqdm',
 'urllib3>=1.26.5']

entry_points = \
{'console_scripts': ['h-oss-download = hao.oss:download',
                     'h-oss-init = hao.oss:init',
                     'h-oss-upload = hao.oss:upload',
                     'h-run = hao.cli:run']}

setup_kwargs = {
    'name': 'hao',
    'version': '3.6.8',
    'description': 'conf, logs, namespace, etc',
    'long_description': '# hao\n\nconfigurations, logs and others.\n\n## install\n\n```bash\npip install hao\n```\n\n## precondition\n\nThe folder contained any of the following files (searched in this very order) will be treated as **project root path**.\n\n- requirements.txt\n- VERSION\n- conf\n- setup.py\n- .idea\n- .git\n\n**If your project structure does NOT conform to this, it will not work as expected.**\n\n## features\n\n### config\n\nIt will try to load YAML config file from `conf` folder\n```\n.                               # project root\n├── conf\n│\xa0\xa0 ├── config-{env}.yml        # if `export env=abc`, will raise error if not found\n│\xa0\xa0 ├── config-{hhostname}.yml  # try to load this file, then the default `config.yml`\n│\xa0\xa0 └── config.yml              # the default config file that should always exist\n├── requirements.txt            # every project should have this file\n├── VERSION                     # hao.versions.get_version() will try to read this file\n├── .git\n```\n\nIn following order:\n\n```python\nif os.environ.get("env") is not None:\n    try_to_load(f\'config-{env}.yml\', fallback=\'config.yml\')                   # echo $env\nelse:\n    try_to_load(f\'config-{socket.gethostname()}.yml\', fallback=\'config.yml\')  # echo hostname\n```\n\nSay you have the following content in your config file:\n```yaml\n# config.yml\nes:\n  default:\n    host: 172.23.3.3\n    port: 9200\n    indices:\n      - news\n      - papers\n```\n\nThe get the configured values in your code:\n```python\nimport hao\nes_host = hao.config.get(\'es.default.host\')          # str\nes_port = hao.config.get(\'es.default.port\')          # int\nindices = hao.config.get(\'es.default.indices\')       # list\n...\n```\n\n### logs\n\nSet the logger levels to filter logs\n\ne.g.\n```yaml\n# config.yml\nlogging:\n  __main__: DEBUG\n  transformers: WARNING\n  lightning: INFO\n  pytorch_lightning: INFO\n  elasticsearch: WARNING\n  tests: DEBUG\n  root: INFO                        # root level\n```\n\nSettings for logger:\n```yaml\n# config.yml\nlogger:\n  format: "%(asctime)s %(levelname)-7s %(name)s:%(lineno)-4d - %(message)s"   # overwrite to change to other format\n  handlers:\n    TimedRotatingFileHandler:    # any Handlers in `logging` and `logging.handlers` with it\'s config\n      when: d\n      backupCount: 3\n```\n\nDeclare and user the logger\n\n```python\nimport hao\nLOGGER = hao.logs.get_logger(__name__)\n\nLOGGER.debug(\'message\')\nLOGGER.info(\'message\')\nLOGGER.warnning(\'message\')\nLOGGER.error(\'message\')\nLOGGER.exception(err)\n```\n\n### namespaces\n\n```python\nimport hao\nfrom hao.namespaces import from_args, attr\n\n@from_args\nclass ProcessConf(object):\n    file_in = attr(str, required=True, help="file path to process")\n    file_out = attr(str, required=True, help="file path to save")\n    tokenizer = attr(str, required=True, choice=(\'wordpiece\', \'bpe\'))\n\n\nfrom argparse import Namespace\nfrom pytorch_lightning import Trainer\n@from_args(adds=Trainer.add_argparse_args)\nclass TrainConf(Namespace):\n    root_path_checkpoints = attr(str, default=hao.paths.get_path(\'data/checkpoints/\'))\n    dataset_train = attr(str, default=\'train.txt\')\n    dataset_val = attr(str, default=\'val.txt\')\n    dataset_test = attr(str, default=\'test.txt\')\n    batch_size = attr(int, default=128, key=\'train.batch_size\')                          # key means try to load from config.yml by the key\n    task = attr(str, choices=(\'ner\', \'nmt\'), default=\'ner\')\n    seed = attr(int)\n    epochs = attr(int, default=5)\n```\n\nWhere `attr` is a wrapper for `argpars.add_argument()`\n\nUsage 1: overwrite the default value from command line\n\n```shell\npython -m your_module --task=nmt\n```\n\nUsage 2: overwrite the default value from constructor\n```python\ntrain_conf = TrainConf(task=\'nmt\')\n```\n\nValue lookup order:\n\n- command line\n- constructor\n- config yml if `key` specified in `attr`\n- `default` if specified in `attr`\n\n',
    'author': 'orctom',
    'author_email': 'orctom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/orctom/hao',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
