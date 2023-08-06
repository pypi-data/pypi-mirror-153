# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odd_collector_sdk', 'odd_collector_sdk.api', 'odd_collector_sdk.domain']

package_data = \
{'': ['*']}

install_requires = \
['APScheduler>=3.8.1,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'black==22.3.0',
 'odd-models>=2.0.0,<3.0.0',
 'pyaml-env>=1.1.5,<2.0.0',
 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'odd-collector-sdk',
    'version': '0.2.4',
    'description': 'ODD Collector',
    'long_description': '[![PyPI version](https://badge.fury.io/py/odd-collector-sdk.svg)](https://badge.fury.io/py/odd-collector-sdk)\n\n# ODD Collector SDK\nRoot project for ODD collectors\n\n### Domain\n* `CollectorConfig`\n\n    _Main config file for collector_\n    ``` python\n    class CollectorConfig(pydantic.BaseSettings):\n        default_pulling_interval: int # pulling interval in minutes\n        token: str                    # token for requests to odd-platform\n        plugins: Any\n        platform_host_url: str\n    ```\n\n* `Collector`\n\n    Args:\n\n    `config_path`: str - path to collector_config.yaml (i.e. `\'/collector_config.yaml\'`)\n\n    `root_package`: str - root package for adapters which will be loaded (i.e. `\'my_collector.adapters\'`)\n\n    `plugins_union_type` - Type variable for pydantic model.\n\n* `Plugin`\n\n  Is a config for adapter\n  ```python\n  class Plugin(pydantic.BaseSettings):\n    name: str\n    description: Optional[str] = None\n    namespace: Optional[str] = None\n  ```\n\n  Plugin class inherited from Pydantic\'s BaseSetting,it means it can take any field, which was skipped in `collector_config.yaml`, from env variables.\n\n  Field `type: Literal["custom_adapter"]`  is obligatory for each plugin, by convention literal **MUST** have same name with adapter package\n\n  Plugins example:\n  ```python\n    # plugins.py\n    class AwsPlugin(Plugin):\n        aws_secret_access_key: str\n        aws_access_key_id: str\n        aws_region: str\n    \n    class S3Plugin(AwsPlugin):\n        type: Literal["s3"]\n        buckets: Optional[List[str]] = []\n\n    class GluePlugin(AwsPlugin):\n        type: Literal["glue"]\n    \n    # For Collector\'s plugins_union_type argument\n    AvailablePlugin = Annotated[\n        Union[\n            GluePlugin,\n            S3Plugin,\n        ],\n        pydantic.Field(discriminator="type"),\n    ]\n  ```\n* AbstractAdapter\n    Abstract adapter which **MUST** be implemented by generic adapters\n\n## Collector example\n\n### Requirenments\nUse the package manager [poetry](https://python-poetry.org/) to install add odd-collector-sdk and asyncio.\n```bash\npoetry add odd-collector-sdk\n```\n\n### A typical top-level collector\'s directory layout (as an example we took poetry project)\n\n    .\n    ├── my_collector            \n    │   ├── adapters            # Adapters\n    │   │   ├── custom_adapter  # Some adapter package\n    │   │   │   ├── adapter.py  # Entry file for adapter\n    │   │   │   └── __init__.py\n    │   │   ├── other_custom_adapter\n    │   │   ├── ...             # Other adapters\n    │   │   └── __init__.py\n    │   ├── domain              # Domain models\n    │   │   ├── ...\n    │   │   ├── plugins.py      # Models for available plugins\n    │   │   └── __init__.py\n    │   ├── __init__.py         \n    │   └── __main__.py         # Entry file for collector\n    ├── ...\n    ├── collector_config.yaml\n    ├── pyproject.toml\n    ├── LICENSE\n    └── README.md\n\n\n\n### Adapters folder\nEach adapter inside adapters folder must have an `adapter.py` file with an `Adapter` class implementing `AbstractAdapter`\n```python\n    # custom_adapter/adapter.py example\n    from odd_collector_sdk.domain.adapter import AbstractAdapter\n    from odd_models.models import DataEntityList\n\n    # \n    class Adapter(AbstractAdapter):\n        def __init__(self, config: any) -> None:\n            super().__init__()\n\n        def get_data_entity_list(self) -> DataEntityList:\n            return DataEntityList(data_source_oddrn="test")\n\n        def get_data_source_oddrn(self) -> str:\n            return "oddrn"\n```\n\n### Plugins\nEach plugin must implement `Plugin` class from sdk\n```python\n    # domain/plugins.py\n    from typing import Literal, Union\n    from typing_extensions import Annotated\n\n    import pydantic\n    from odd_collector_sdk.domain.plugin import Plugin\n\n    class CustomPlugin(Plugin):\n        type: Literal["custom_adapter"]\n\n\n    class OtherCustomPlugin(Plugin):\n        type: Literal["other_custom_adapter"]\n\n    # Needs this type variable for Collector initialization\n    AvailablePlugins = Annotated[\n        Union[CustomPlugin, OtherCustomPlugin],\n        pydantic.Field(discriminator="type"),\n    ]\n```\n\n### collector_config.yaml\n\n```yaml\ndefault_pulling_interval: 10 \ntoken: "" \nplatform_host_url: "http://localhost:8080" \nplugins:\n  - type: custom_adapter\n    name: custom_adapter_name\n  - type: other_custom_adapter\n    name: other_custom_adapter_name\n\n```\n\n## Usage\n```python\n# __main__.py\n\nimport asyncio\nimport logging\nfrom os import path\n\n\nfrom odd_collector_sdk.collector import Collector\n\n# Union type of avalable plugins\nfrom my_collector.domain.plugins import AvailablePlugins\n\nlogging.basicConfig(\n    level=logging.INFO, format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"\n)\n\ntry:\n    cur_dirname = path.dirname(path.realpath(__file__))\n    config_path = path.join(cur_dirname, "../collector_config.yaml")\n    root_package = "my_collector.adapters"\n\n    loop = asyncio.get_event_loop()\n\n    collector = Collector(config_path, root_package, AvailablePlugin)\n\n    loop.run_until_complete(collector.register_data_sources())\n\n    collector.start_polling()\n    loop.run_forever()\nexcept Exception as e:\n    logging.error(e, exc_info=True)\n    loop.stop()\n```\n\nAnd run\n```bash\npoetry run python -m my_collector\n```\n\n\n',
    'author': 'Open Data Discovery',
    'author_email': 'pypi@opendatadiscovery.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/opendatadiscovery/odd-collector-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
