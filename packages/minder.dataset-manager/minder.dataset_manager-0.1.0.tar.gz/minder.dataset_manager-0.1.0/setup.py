# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minder',
 'minder.dataset_manager',
 'minder.dataset_manager._utils',
 'minder.dataset_manager.datasets']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['minder.research-portal-client>=0.1.3,<0.2.0',
 'numpy>=1.22.4,<2.0.0',
 'pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'minder.dataset-manager',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Dataset Manager\n\nLibrary to pre-process CSV files from Research Portal into usable datasets.\n\n## Installation\n\n```bash\npip install minder.dataset-manager\n```\n\n## Example\n```python\nimport logging\nimport asyncio\nimport sys\nfrom typing import Optional\nfrom minder.dataset_manager._utils import Dataset\nfrom minder.dataset_manager.datasets import LabelledUtiDataset\nfrom minder.research_portal_client import Configuration, JobManager\n\n\nlogging.basicConfig(level=logging.INFO)\n\nConfiguration.set_default(\n    Configuration(\n        access_token="---REDACTED---",\n    )\n)\n\n\nasync def example1():\n    job_ids = ["c25249e0-82ff-43d1-9676-f3cead0228b9"]\n    async with JobManager() as job_manager:\n        files = Dataset.download(job_ids, job_manager)\n        dataset = LabelledUtiDataset.create(job_ids, files)\n        dataset.save("./my-dataset.npz")\n\n\nasync def example2():\n    job_ids = ["c25249e0-82ff-43d1-9676-f3cead0228b9"]\n    existing_dataset = "./my-dataset.npz"\n    async with JobManager() as job_manager:\n        download_task = Dataset.download(job_ids, job_manager)\n        try:\n            previous_dataset: Optional[Dataset] = None\n            if existing_dataset.exists():\n                previous_dataset = LabelledUtiDataset.load(existing_dataset)\n        finally:\n            files = await download_task\n\n        new_dataset = LabelledUtiDataset.create(job_ids, files)\n\n        dataset = (\n            await previous_dataset.update(new_dataset, job_manager=job_manager)\n            if previous_dataset is not None\n            else new_dataset\n        )\n        dataset.save("./my-dataset.npz")\n\n\nasync def main():\n    await example1()\n    await example2()\n\n\nif sys.platform == "win32"::\n    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())\n\nasyncio.run(main())\n```\n\n# Development\n\n## Useful commands\n\n### Setup\n\n```bash\npoetry install\n```\n\n### Run tests\n  \n```bash\npoetry run pytest\n```\n\n### Code Coverage\n\nThis command consists of 2 parts:\n- running tests with coverage collection\n- formatting the report: `report` (text to stdout), `xml` (GitLab compatible: cobertura), `html` (visual)\n\n```bash\npoetry run coverage run -m pytest && poetry run coverage report -m\n```\n\n### Linting\n\n```bash\npoetry run flake8\n```\n\n### Formatting\n\n```bash\npoetry run black .\n```\n\n### Type Checking\n\n```bash\npoetry run mypy .\n```\n',
    'author': 'UK DRI Care Research & Technology centre',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
