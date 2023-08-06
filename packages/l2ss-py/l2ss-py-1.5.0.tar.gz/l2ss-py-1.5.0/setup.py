# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['podaac', 'podaac.subsetter']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.7.1,<2.0.0',
 'cf-xarray>=0.7.0,<0.8.0',
 'geopandas==0.6.1',
 'h5py>=3.6.0,<4.0.0',
 'importlib-metadata>=4.8.1,<5.0.0',
 'julian>=0.14,<0.15',
 'netCDF4>=1.5,<2.0',
 'xarray[parallel]']

extras_require = \
{'harmony': ['harmony-service-lib>=1.0.15,<2.0.0', 'pystac>=0.5.3,<0.6.0']}

entry_points = \
{'console_scripts': ['l2ss-py = podaac.subsetter.run_subsetter:main',
                     'l2ss_harmony = podaac.subsetter.subset_harmony:main',
                     'run_worker = podaac.subsetter.subset_worker:main']}

setup_kwargs = {
    'name': 'l2ss-py',
    'version': '1.5.0',
    'description': 'L2 Subsetter Service',
    'long_description': '\n# l2ss-py\n\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=podaac_l2ss-py&metric=coverage)](https://sonarcloud.io/dashboard?id=podaac_l2ss-py)  \ndevelop: [![Develop Build](https://github.com/podaac/l2ss-py/actions/workflows/build-pipeline.yml/badge.svg?branch=develop&event=push)](https://github.com/podaac/l2ss-py/actions/workflows/build-pipeline.yml)  \nmain: [![Main Build](https://github.com/podaac/l2ss-py/actions/workflows/build-pipeline.yml/badge.svg?branch=main&event=push)](https://github.com/podaac/l2ss-py/actions/workflows/build-pipeline.yml)\n\nHarmony service for subsetting L2 data. l2ss-py supports:\n\n- Spatial subsetting\n    - Bounding box\n    - Shapefile subsetting\n    - GeoJSON subsetting\n- Temporal subsetting\n- Variable subsetting\n\nIf you would like to contribute to l2ss-py, refer to the [contribution document](CONTRIBUTING.md).\n\n\n## How to test l2ss-py locally\n\n### Unit tests\n\nThere are comprehensive unit tests for l2ss-py. The tests can be run as follows:\n\n```\npoetry run pytest -m "not aws and not integration" tests/\n```\n\nYou can generate coverage reports as follows:\n\n```\npoetry run pytest --junitxml=build/reports/pytest.xml --cov=podaac/ --cov-report=html -m "not aws and not integration" tests/\n```\n\n### l2ss-py script\n\nYou can run l2ss-py on a single granule without using Harmony. In order \nto run this, the l2ss-py package must be installed in your current \nPython interpreter\n\n```\n$ l2ss-py --help                                                                                                                    \nusage: run_subsetter.py [-h] [--bbox BBOX BBOX BBOX BBOX]\n                        [--variables VARIABLES [VARIABLES ...]]\n                        [--min-time MIN_TIME] [--max-time MAX_TIME] [--cut]\n                        input_file output_file\n\nRun l2ss-py\n\npositional arguments:\n  input_file            File to subset\n  output_file           Output file\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --bbox BBOX BBOX BBOX BBOX\n                        Bounding box in the form min_lon min_lat max_lon\n                        max_lat\n  --variables VARIABLES [VARIABLES ...]\n                        Variables, only include if variable subset is desired.\n                        Should be a space separated list of variable names\n                        e.g. sst wind_dir sst_error ...\n  --min-time MIN_TIME   Min time. Should be ISO-8601 format. Only include if\n                        temporal subset is desired.\n  --max-time MAX_TIME   Max time. Should be ISO-8601 format. Only include if\n                        temporal subset is desired.\n  --cut                 If provided, scanline will be cut\n  --shapefile SHAPEFILE\n                        Path to either shapefile or geojson file used to subset the provided input granule\n```\n\nFor example:\n\n```\nl2ss-py /path/to/input.nc /path/to/output.nc --bbox -50 -10 50 10 --variables wind_speed wind_dir ice_age time --min-time \'2015-07-02T09:00:00\' --max-time \'2015-07-02T10:00:00\' --cut\n```\n\nAn addition to providing a bounding box, spatial subsetting can be achieved by passing in a shapefile or a geojson file. \n\n```shell script\npoetry run l2ss-py /path/to/input.nc /path/to/output.nc --shapefile /path/to/test.shp\n```\n\nor \n\n```shell script\npoetry run l2ss-py /path/to/input.nc /path/to/output.nc --shapefile /path/to/test.geojson\n```\n\n### Running Harmony locally\n\nIn order to fully test l2ss-py with Harmony, you can run Harmony locally. This requires the data exists in UAT Earthdata Cloud.\n\n1. Set up local Harmony instance. Instructions [here](https://github.com/nasa/harmony#Quick-Start)\n2. Add concept ID for your data to [services.yml](https://github.com/nasa/harmony/blob/main/config/services.yml)\n3. Execute a local Harmony l2ss-py request. For example:\n    ```\n   localhost:3000/YOUR_COLLECTION_ID/ogc-api-coverages/1.0.0/collections/all/coverage/rangeset?format=application%2Fx-netcdf4&subset=lat(-10%3A10)&subset=lon(-10%3A10)&maxResults=2\n   ```\n',
    'author': 'podaac-tva',
    'author_email': 'podaac-tva@jpl.nasa.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/podaac/l2ss-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
