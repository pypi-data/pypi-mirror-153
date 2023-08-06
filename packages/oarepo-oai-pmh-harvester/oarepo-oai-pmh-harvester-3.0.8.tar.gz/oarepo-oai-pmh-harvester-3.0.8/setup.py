# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oarepo_oaipmh_harvester',
 'oarepo_oaipmh_harvester.alembic',
 'oarepo_oaipmh_harvester.oaipmh_batch',
 'oarepo_oaipmh_harvester.oaipmh_batch.alembic',
 'oarepo_oaipmh_harvester.oaipmh_batch.records',
 'oarepo_oaipmh_harvester.oaipmh_batch.records.jsonschemas',
 'oarepo_oaipmh_harvester.oaipmh_batch.records.mappings',
 'oarepo_oaipmh_harvester.oaipmh_batch.records.mappings.v7',
 'oarepo_oaipmh_harvester.oaipmh_batch.records.mappings.v7.oaipmh_batch',
 'oarepo_oaipmh_harvester.oaipmh_batch.resources',
 'oarepo_oaipmh_harvester.oaipmh_batch.services',
 'oarepo_oaipmh_harvester.oaipmh_config',
 'oarepo_oaipmh_harvester.oaipmh_config.alembic',
 'oarepo_oaipmh_harvester.oaipmh_config.records',
 'oarepo_oaipmh_harvester.oaipmh_config.records.jsonschemas',
 'oarepo_oaipmh_harvester.oaipmh_config.records.mappings',
 'oarepo_oaipmh_harvester.oaipmh_config.records.mappings.v7',
 'oarepo_oaipmh_harvester.oaipmh_config.records.mappings.v7.oaipmh_config',
 'oarepo_oaipmh_harvester.oaipmh_config.resources',
 'oarepo_oaipmh_harvester.oaipmh_config.services',
 'oarepo_oaipmh_harvester.oaipmh_record',
 'oarepo_oaipmh_harvester.oaipmh_record.alembic',
 'oarepo_oaipmh_harvester.oaipmh_record.records',
 'oarepo_oaipmh_harvester.oaipmh_record.records.jsonschemas',
 'oarepo_oaipmh_harvester.oaipmh_record.records.mappings',
 'oarepo_oaipmh_harvester.oaipmh_record.records.mappings.v7',
 'oarepo_oaipmh_harvester.oaipmh_record.records.mappings.v7.oaipmh_record',
 'oarepo_oaipmh_harvester.oaipmh_record.resources',
 'oarepo_oaipmh_harvester.oaipmh_record.services',
 'oarepo_oaipmh_harvester.oaipmh_run',
 'oarepo_oaipmh_harvester.oaipmh_run.alembic',
 'oarepo_oaipmh_harvester.oaipmh_run.records',
 'oarepo_oaipmh_harvester.oaipmh_run.records.jsonschemas',
 'oarepo_oaipmh_harvester.oaipmh_run.records.mappings',
 'oarepo_oaipmh_harvester.oaipmh_run.records.mappings.v7',
 'oarepo_oaipmh_harvester.oaipmh_run.records.mappings.v7.oaipmh_run',
 'oarepo_oaipmh_harvester.oaipmh_run.resources',
 'oarepo_oaipmh_harvester.oaipmh_run.services']

package_data = \
{'': ['*']}

install_requires = \
['Sickle>=0.7.0,<0.8.0',
 'dojson>=1.4.0,<2.0.0',
 'elasticsearch==7.17.3',
 'invenio-records-resources>=0.19.0',
 'invenio-search>=1.4.2,<2.0.0',
 'invenio>=3.4.1,<4.0.0',
 'tqdm>=4.63.0,<5.0.0']

entry_points = \
{'invenio_base.api_apps': ['oarepo_oaipmh_harvester = '
                           'oarepo_oaipmh_harvester.ext:OARepoOAIHarvesterExt',
                           'oarepo_oaipmh_harvester_batch = '
                           'oarepo_oaipmh_harvester.oaipmh_batch.ext:OaipmhBatchExt',
                           'oarepo_oaipmh_harvester_config = '
                           'oarepo_oaipmh_harvester.oaipmh_config.ext:OaipmhConfigExt',
                           'oarepo_oaipmh_harvester_record = '
                           'oarepo_oaipmh_harvester.oaipmh_record.ext:OaipmhRecordExt',
                           'oarepo_oaipmh_harvester_run = '
                           'oarepo_oaipmh_harvester.oaipmh_run.ext:OaipmhRunExt'],
 'invenio_base.apps': ['oarepo_oaipmh_harvester = '
                       'oarepo_oaipmh_harvester.ext:OARepoOAIHarvesterExt',
                       'oarepo_oaipmh_harvester_batch = '
                       'oarepo_oaipmh_harvester.oaipmh_batch.ext:OaipmhBatchExt',
                       'oarepo_oaipmh_harvester_config = '
                       'oarepo_oaipmh_harvester.oaipmh_config.ext:OaipmhConfigExt',
                       'oarepo_oaipmh_harvester_record = '
                       'oarepo_oaipmh_harvester.oaipmh_record.ext:OaipmhRecordExt',
                       'oarepo_oaipmh_harvester_run = '
                       'oarepo_oaipmh_harvester.oaipmh_run.ext:OaipmhRunExt'],
 'invenio_celery.tasks': ['oarepo_oaipmh_harvester = '
                          'oarepo_oaipmh_harvester.harvester'],
 'invenio_db.alembic': ['oaipmh_config = '
                        'oarepo_oaipmh_harvester.oaipmh_config:alembic',
                        'oarepo_oaipmh_harvester = '
                        'oarepo_oaipmh_harvester:alembic'],
 'invenio_db.models': ['oaipmh_config = '
                       'oarepo_oaipmh_harvester.oaipmh_config.records.models',
                       'oarepo_oaipmh_harvester = '
                       'oarepo_oaipmh_harvester.models'],
 'invenio_jsonschemas.schemas': ['oaipmh_batch = '
                                 'oarepo_oaipmh_harvester.oaipmh_batch.records.jsonschemas',
                                 'oaipmh_config = '
                                 'oarepo_oaipmh_harvester.oaipmh_config.records.jsonschemas',
                                 'oaipmh_record = '
                                 'oarepo_oaipmh_harvester.oaipmh_record.records.jsonschemas',
                                 'oaipmh_run = '
                                 'oarepo_oaipmh_harvester.oaipmh_run.records.jsonschemas'],
 'invenio_search.mappings': ['oaipmh_batch = '
                             'oarepo_oaipmh_harvester.oaipmh_batch.records.mappings',
                             'oaipmh_config = '
                             'oarepo_oaipmh_harvester.oaipmh_config.records.mappings',
                             'oaipmh_record = '
                             'oarepo_oaipmh_harvester.oaipmh_record.records.mappings',
                             'oaipmh_run = '
                             'oarepo_oaipmh_harvester.oaipmh_run.records.mappings'],
 'oarepo_oaipmh_harvester.parsers': ['marcxml = '
                                     'oarepo_oaipmh_harvester.parsers:MarcxmlParser']}

setup_kwargs = {
    'name': 'oarepo-oai-pmh-harvester',
    'version': '3.0.8',
    'description': 'OAIPMH harvester library for Invenio. Development only, not for production.',
    'long_description': '# OARepo OAI-PMH harvester\n\nAn OAI-PMH harvesing library for Invenio 3.5+. The library provides initial transformation of OAI-PMH payload to an\nintermediary json representation which is later on transformed by a specific transformer to invenio records.\n\nDue to their generic nature, these transformers are not part of this library but have to be provided by an application.\n\nThe progress and transformation errors are captured within the database.\n\nFor now, the library does not provide error notifications, but these will be added. A sentry might be used for the\nlogging & reporting.\n\n## Installation\n\n```bash\npoetry add oarepo-oaipmh-harvester\n```\n\n## Configuration\n\nAll configuration is inside the database model `OAIHarvesterConfig`.\nThere is a command-line tool to add a new config:\n\n```bash\ninvenio oaiharvester add \\\n  --code nusl \\\n  --name NUŠL \\\n  --url "http://invenio.nusl.cz/oai2d/" \\\n  --set global \\\n  --prefix marcxml \n  --transformer nusl_oai.transformer.NuslTransformer\n```\n\nThis will register an oai-pmh harvester with code "nusl",\nits url, oai set and metadata prefix. Records from this\nharvester will be transformed by the NuslTransformer before\nthey are written to the repository.\n\nOptions:\n\n```bash\nUsage: invenio oaiharvester add [OPTIONS]\n\nOptions:\n  --code TEXT         OAI server code  [required]\n  --name TEXT         OAI server name  [required]\n  --url TEXT          OAI base url  [required]\n  --set TEXT          OAI set  [required]\n  --prefix TEXT       OAI metadata prefix  [required]\n  --parser TEXT       OAI metadata parser. If not passed, a prefix-based default is used\n  --transformer TEXT  Transformer class  [required]\n```\n\n## Usage\n\n### Command-line\n\nOn command line, invoke\n\n```bash\noaiharvester harvest nusl <optional list of oai identifiers to harvest>\n```\n\nOptions:\n\n```text\n  -a, --all-records  Re-harvest all records, not from the last timestamp\n  --background       Start Harvest on background (via celery task), return immediately\n  --dump-to TEXT     Do not import records, just dump (cache) them to this\n                     directory (mostly for debugging)\n  --load-from TEXT   Do not contact oai-pmh server but load the records from\n                     this directory (created by dump-to option)\n```\n\n### Celery task\n\n```python3\n@shared_task\ndef oai_harvest(\n        harvester_id: str, \n        start_from: str, \n        load_from: str = None, \n        dump_to: str = None,\n        on_background=False, \n        identifiers=None):\n    """\n    @param harvester_id: id of the harvester configuration (OAIHarvesterConfig) object\n    @param start_from: datestamp (either YYYY-MM-DD or YYYY-MM-DDThh:mm:ss, \n           depends on the OAI endpoint), inclusive\n    @param load_from: if set, a path to the directory on the filesystem where \n           the OAI-PMH data are present (in *.json.gz files)\n    @param dump_to: if set, harvested metadata will be parsed from xml to json \n           and stored into this directory, not to the repository\n    @param on_background: if True, transformation and storage will be started in celery tasks and can run in parallel.\n           If false, they will run sequentially inside this task\n    @param identifiers: if load_from is set, it is a list of file names within the directory. \n           If load_from is not set, these are oai identifiers for GetRecord. If not set at all, all records from \n           start_from are harvested \n    """\n```\n\n## Harvest status\n\nEach harvest creates a row in `OAIHarvestRun` database\ntable containing first and last datestamps and harvest\nstatus (running, completed, errored, ...)\n\nA run is split into a chunk of records and each chunk\nis represented in `OAIHarvestRunBatch` database table.\nIt contains a chunk status (running, completed, warning,\nfailed, ...) and a list of identifiers harvested and \ntheir status (ok, warning during harvesting the identifier,\nharvesting the identifier failed). The table also contains\ndetails of the warnings/errors.\n\n## Custom parsers and transformers\n\nThe input OAI xml is at first parsed via parsers into\na json format.\n\nMARC-XML and DC parsers are supported out of the box.\nSee the section below if you need a different parser\n\nThe JSON is then transformed into an invenio record\nvia a transformer class. As different repositories\nuse different semantic of fields (even in MARC),\nthis step can not be generic and implementor is required\nto provide his/her own transformer class.\n\n### Transformer\n\nA simple transformer, that transforms just the title from MARC-XML\ninput might look like:\n\n```python3\nfrom typing import List\nfrom oarepo_oaipmh_harvester import OAITransformer, OAIRecord, OAIHarvestRunBatch\n\nfrom my_record.proxies import current_service\nfrom my_record.records.api import MyRecord\n\nclass NuslTransformer(OAITransformer):\n    oaiidentifier_search_property = \'metadata_systemIdentifiers_identifier\'\n    # the name of service filter that accesses the record\'s OAI identifier\n    oaiidentifier_search_path = (\'metadata\', \'systemIdentifiers\', \'identifier\')\n    # path to the oai record identifier inside the record\n\n    # invenio service that will be used to create/update the record\n    record_service = current_service\n    # invenio record for this record\n    record_model = MyRecord \n    \n\n    def transform_single(self, rec: OAIRecord):\n        # add all your transformations here\n        rec.transformed.update({\n            \'metadata\': {\n                \'title\': rec[\'24500a\']\n            }\n        })\n```\n\n### Parser\n\nA parser is responsible for transforming the XML document\ninto an intermediary JSON.\n\nFor implementation details see [MarcxmlParser](./oarepo_oaipmh_harvester/parsers.py).',
    'author': 'Mirek Simek',
    'author_email': 'miroslav.simek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
