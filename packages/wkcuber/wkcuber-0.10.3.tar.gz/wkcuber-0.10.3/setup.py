# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wkcuber', 'wkcuber._internal', 'wkcuber.api', 'wkcuber.vendor']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.0.5,<4.0.0',
 'attrs>=21.1.0,<22.0.0',
 'cattrs==1.7.1',
 'cluster_tools==0.10.3',
 'czifile>=2019.7.2,<2020.0.0',
 'imagecodecs>=2020.5.30,<2021.0.0',
 'natsort>=6.2.0,<7.0.0',
 'nibabel>=2.5.1,<3.0.0',
 'numpy>=1.19.5,<2.0.0',
 'pillow>=6.2.1,<9.0.0',
 'requests>=2.22.0,<3.0.0',
 'scikit-image>=0.18.3,<0.19.0',
 'scikit-learn>=0.24.0,<0.25.0',
 'scipy>=1.6.0,<2.0.0',
 'tifffile>=2020.11.26,<2021.0.0',
 'universal-pathlib==0.0.18',
 'webknossos==0.10.3',
 'wkw==1.1.11',
 'zarr>=2.11.0,<3.0.0']

entry_points = \
{'console_scripts': ['wkcuber = wkcuber.__main__:main']}

setup_kwargs = {
    'name': 'wkcuber',
    'version': '0.10.3',
    'description': 'Python package to create, cube, and work with webKnossos WKW datasets',
    'long_description': '# webKnossos cuber (wkcuber)\n[![PyPI version](https://img.shields.io/pypi/v/wkcuber)](https://pypi.python.org/pypi/wkcuber)\n[![Supported Python Versions](https://img.shields.io/pypi/pyversions/wkcuber.svg)](https://pypi.python.org/pypi/wkcuber)\n[![Build Status](https://img.shields.io/github/workflow/status/scalableminds/webknossos-libs/CI/master)](https://github.com/scalableminds/webknossos-libs/actions?query=workflow%3A%22CI%22)\n[![Documentation](https://img.shields.io/badge/docs-passing-brightgreen.svg)](https://docs.webknossos.org/wkcuber/index.html)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPython library for creating and working with [webKnossos](https://webknossos.org) [WKW](https://github.com/scalableminds/webknossos-wrap) datasets. WKW is a container format for efficiently storing large, scale 3D image data as found in (electron) microscopy.\n\nThe tools are modular components to allow easy integration into existing pipelines and workflows.\n\n## Features\n\n* `wkcuber`: Convert supported input files to fully ready WKW datasets (includes type detection, downsampling, compressing and metadata generation)\n* `wkcuber.convert_image_stack_to_wkw`: Convert image stacks to fully ready WKW datasets (includes downsampling, compressing and metadata generation)\n* `wkcuber.export_wkw_as_tiff`: Convert WKW datasets to a tiff stack (writing as tiles to a `z/y/x.tiff` folder structure is also supported)\n* `wkcuber.cubing`: Convert image stacks (e.g., `tiff`, `jpg`, `png`, `bmp`, `dm3`, `dm4`) to WKW cubes\n* `wkcuber.tile_cubing`: Convert tiled image stacks (e.g. in `z/y/x.ext` folder structure) to WKW cubes\n* `wkcuber.convert_knossos`: Convert KNOSSOS cubes to WKW cubes\n* `wkcuber.convert_nifti`: Convert NIFTI files to WKW files (Currently without applying transformations).\n* `wkcuber.convert_raw`: Convert RAW binary data (.raw, .vol) files to WKW datasets\n* `wkcuber.downsampling`: Create downsampled magnifications (with `median`, `mode` and linear interpolation modes). Downsampling compresses the new magnifications by default (disable via `--no_compress`).\n* `wkcuber.compress`: Compress WKW cubes for efficient file storage (especially useful for segmentation data)\n* `wkcuber.metadata`: Create (or refresh) metadata (with guessing of most parameters)\n* `wkcuber.recubing`: Read existing WKW cubes in and write them again specifying the WKW file length. Useful when dataset was written e.g. with file length 1.\n* `wkcuber.check_equality`: Compare two WKW datasets to check whether they are equal (e.g., after compressing a dataset, this task can be useful to double-check that the compressed dataset contains the same data).\n* Most modules support multiprocessing\n\n## Supported input formats\n\n* Standard image formats, e.g. `tiff`, `jpg`, `png`, `bmp`\n* Proprietary image formats, e.g. `dm3`\n* Tiled image stacks (used for Catmaid)\n* KNOSSOS cubes\n* NIFTI files\n* Raw binary files\n\n## Installation\n### Python 3 with pip from PyPi\n- `wkcuber` requires at least Python 3.7+\n\n```bash\n# Make sure to have lz4 installed:\n# Mac: brew install lz4\n# Ubuntu/Debian: apt-get install liblz4-1\n# CentOS/RHEL: yum install lz4\n\npip install wkcuber\n```\n\n### Docker\nUse the CI-built image: [scalableminds/webknossos-cuber](https://hub.docker.com/r/scalableminds/webknossos-cuber/). Example usage `docker run -v <host path>:/data --rm scalableminds/webknossos-cuber wkcuber --layer_name color --scale 11.24,11.24,25 --name great_dataset /data/source/color /data/target`.\n\n\n## Usage\n\n```bash\n# Convert arbitrary, supported input files into wkw datasets. This sets reasonable defaults, but see other commands for customization.\npython -m wkcuber \\\n  --scale 11.24,11.24,25 \\\n  data/source data/target\n\n# Convert image stacks into wkw datasets\npython -m wkcuber.convert_image_stack_to_wkw \\\n  --layer_name color \\\n  --scale 11.24,11.24,25 \\\n  --name great_dataset \\\n  data/source/color data/target\n\n# Convert image files to wkw cubes\npython -m wkcuber.cubing --layer_name color data/source/color data/target\npython -m wkcuber.cubing --layer_name segmentation data/source/segmentation data/target\n\n# Convert tiled image files to wkw cubes\npython -m wkcuber.tile_cubing --layer_name color data/source data/target\n\n# Convert Knossos cubes to wkw cubes\npython -m wkcuber.convert_knossos --layer_name color data/source/mag1 data/target\n\n# Convert NIFTI file to wkw file\npython -m wkcuber.convert_nifti --layer_name color --scale 10,10,30 data/source/nifti_file data/target\n\n# Convert folder with NIFTI files to wkw files\npython -m wkcuber.convert_nifti --color_file one_nifti_file --segmentation_file --scale 10,10,30 another_nifti data/source/ data/target\n\n# Convert RAW file to wkw file\npython -m wkcuber.convert_raw --layer_name color --scale 10,10,30 --input_dtype uint8 --shape 2048,2048,1024 data/source/raw_file.raw data/target\n\n# Create downsampled magnifications\npython -m wkcuber.downsampling --layer_name color data/target\npython -m wkcuber.downsampling --layer_name segmentation --interpolation_mode mode data/target\n\n# Compress data in-place (mostly useful for segmentation)\npython -m wkcuber.compress --layer_name segmentation data/target\n\n# Compress data copy (mostly useful for segmentation)\npython -m wkcuber.compress --layer_name segmentation data/target data/target_compress\n\n# Create metadata\npython -m wkcuber.metadata --name great_dataset --scale 11.24,11.24,25 data/target\n\n# Refresh metadata so that new layers and/or magnifications are picked up\npython -m wkcuber.metadata --refresh data/target\n\n# Recubing an existing dataset\npython -m wkcuber.recubing --layer_name color --dtype uint8 /data/source/wkw /data/target\n\n# Check two datasets for equality\npython -m wkcuber.check_equality /data/source /data/target\n```\n\n### Parallelization\n\nMost tasks can be configured to be executed in a parallelized manner. Via `--distribution_strategy` you can pass `multiprocessing`, `slurm` or `kubernetes`. The first can be further configured with `--jobs` and the latter via `--job_resources=\'{"mem": "10M"}\'`. Use `--help` to get more information.\n\n### Zarr support\n\nMost conversion commands can be configured with `--data_format zarr`. This will produce a Zarr-based dataset instead of WKW. Zarr-based datasets can also be stored on remote storage (e.g. S3, GCS, HTTP). For that, storage-specific credentials and configurations need to be passed in as environment variables.\n\n```bash\nexport AWS_SECRET_ACCESS_KEY="..."\nexport AWS_ACCESS_KEY_ID="..."\nexport AWS_REGION="..."\n\npython -m wkcuber \\\n  --scale 11.24,11.24,25 \\\n  --data_format zarr \\\n  data/source s3://bucket/data/target\n```\n\n\n## Development\nMake sure to install all the required dependencies using Poetry:\n```bash\npip install poetry\npoetry install\n```\n\nPlease, format, lint, and unit test your code changes before merging them.\n```bash\npoetry run black .\npoetry run pylint -j4 wkcuber\npoetry run pytest tests\n```\n\nPlease, run the extended test suite:\n```bash\ntests/scripts/all_tests.sh\n```\n\nPyPi releases are automatically pushed when creating a new Git tag/Github release. \n\n## API documentation\nCheck out the [latest version of the API documentation](https://docs.webknossos.org/api/wkcuber.html).\n\n### Generate the API documentation\nRun `docs/generate.sh` to open a server displaying the API docs. `docs/generate.sh --persist` persists the html to `docs/api`.\n\n## Test Data Credits\nExcerpts for testing purposes have been sampled from:\n\n* Dow Jacobo Hossain Siletti Hudspeth (2018). **Connectomics of the zebrafish\'s lateral-line neuromast reveals wiring and miswiring in a simple microcircuit.** eLife. [DOI:10.7554/eLife.33988](https://elifesciences.org/articles/33988)\n* Zheng Lauritzen Perlman Robinson Nichols Milkie Torrens Price Fisher Sharifi Calle-Schuler Kmecova Ali Karsh Trautman Bogovic Hanslovsky Jefferis Kazhdan Khairy Saalfeld Fetter Bock (2018). **A Complete Electron Microscopy Volume of the Brain of Adult Drosophila melanogaster.** Cell. [DOI:10.1016/j.cell.2018.06.019](https://www.cell.com/cell/fulltext/S0092-8674(18)30787-6). License: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)\n\n## License\nAGPLv3\nCopyright scalable minds\n',
    'author': 'scalable minds',
    'author_email': 'hello@scalableminds.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://docs.webknossos.org/wkcuber',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
