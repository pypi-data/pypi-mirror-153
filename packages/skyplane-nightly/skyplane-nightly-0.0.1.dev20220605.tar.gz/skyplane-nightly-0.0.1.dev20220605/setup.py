# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skyplane',
 'skyplane.cli',
 'skyplane.cli.cli_impl',
 'skyplane.cli.experiments',
 'skyplane.compute',
 'skyplane.compute.aws',
 'skyplane.compute.azure',
 'skyplane.compute.gcp',
 'skyplane.gateway',
 'skyplane.obj_store',
 'skyplane.replicate',
 'skyplane.utils']

package_data = \
{'': ['*']}

install_requires = \
['azure-identity>=1,<2',
 'azure-mgmt-authorization>=1.0.0',
 'azure-mgmt-compute>=24.0.0',
 'azure-mgmt-network>=10.0.0',
 'azure-mgmt-resource>=11.0.0',
 'azure-mgmt-storage>=11.0.0',
 'azure-storage-blob>=12.0.0',
 'boto3>=1.16.0',
 'cachetools>=4.1.0',
 'click>=8.0.0',
 'google-api-python-client>=2.0.2',
 'google-auth>=2.0.0',
 'google-cloud-compute>=1.0.0',
 'google-cloud-storage>=1.30.0',
 'pandas>=1.0.0',
 'paramiko>=2.7.2',
 'questionary>=1.5.2',
 'rich>=9.0.0',
 'sshtunnel>=0.3.0',
 'termcolor>=1.1.0',
 'typer>=0.4.0']

extras_require = \
{'gateway': ['lz4>=4.0.0,<5.0.0',
             'flask>=2.1.2,<3.0.0',
             'pyopenssl>=22.0.0,<23.0.0',
             'werkzeug>=2.1.2,<3.0.0'],
 'solver': ['cvxpy[cvxopt]>=1.1.0',
            'graphviz>=0.15',
            'matplotlib>=3.0.0',
            'numpy>=1.19.0']}

entry_points = \
{'console_scripts': ['skylark = skyplane.cli.cli:app',
                     'skyplane = skyplane.cli.cli:app']}

setup_kwargs = {
    'name': 'skyplane-nightly',
    'version': '0.0.1.dev20220605',
    'description': 'Skyplane efficiently transports data between cloud regions and providers.',
    'long_description': "# Skyplane\n\n[![poetry](https://github.com/skyplane-project/skyplane/actions/workflows/poetry.yml/badge.svg)](https://github.com/skyplane-project/skyplane/actions/workflows/poetry.yml)\n[![docker](https://github.com/skyplane-project/skyplane/actions/workflows/docker-publish.yml/badge.svg?branch=main)](https://github.com/skyplane-project/skyplane/actions/workflows/docker-publish.yml)\n[![sphinx](https://github.com/skyplane-project/skyplane/actions/workflows/sphinx.yml/badge.svg)](https://github.com/skyplane-project/skyplane/actions/workflows/sphinx.yml)\n[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n\n**🔥 Blazing fast bulk data transfers between any cloud 🔥**\n\nSkyplane is a tool for blazingly fast bulk data transfers in the cloud. Skyplane manages parallelism, data partitioning, and network paths to optimize data transfers, and can also spin up VM instances to increase transfer throughput. \n\nYou can use skyplane to transfer data: \n* Between buckets within a cloud provider\n* Between object stores across multiple cloud providers\n* To/from local storage to a cloud object store\n\n# Getting started\n\n## Installation\n\nWe recommend installation from PyPi: `pip install skyplane-nightly`\n\nTo install Skyplane from source:\n```bash\n$ git clone https://github.com/skyplane-project/skyplane\n$ cd skyplane\n$ pip install -e .\n```\n\n## Authenticating with cloud providers\n\nTo transfer files from cloud A to cloud B, Skyplane will start VMs (called gateways) in both A and B. The CLI therefore requires authentication with each cloud provider. Skyplane will infer credentials from each cloud providers CLI. Therefore, log into each cloud.\n\n<details open>\n<summary>⤵️&nbsp;&nbsp;Setting up AWS credentials</summary>\n<br>\n\nTo set up AWS credentials on your local machine, first [install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).\n\nAfter installing the AWS CLI, configure your AWS IAM access ID and secret with `aws configure`:\n```bash\n$ aws configure\nAWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE\nAWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY\nDefault region name [None]: us-west-2\nDefault output format [None]: json\n```\n\nSee AWS documentation for further [instructions on how to configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html#getting-started-quickstart-new).\n\n</details>\n\n<details open>\n<summary>⤵️&nbsp;&nbsp;Setting up GCP credentials</summary>\n<br>\n\nTo set up GCP credentials on your local machine, first [install the gcloud CLI](https://cloud.google.com/sdk/docs/install-sdk).\n\nAfter installing the gcloud CLI, configure your GCP CLI credentials with `gcloud auth` as follows:\n```bash\n$ gcloud auth login\n$ gcloud auth application-default login\n```\n\n⚠️ If you already had GCP credentials configured, make sure to run `gcloud auth application-default login` which generates application credentials for Skyplane.\n</details>\n\n<details open>\n<summary>⤵️&nbsp;&nbsp;Setting up Azure credentials</summary>\n<br>\n\nTo set up Azure credentials on your local machine, first [install the Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest).\n\nAfter installing the Azure CLI, configure your Azure CLI credentials with `az login` as follows:\n```bash\n$ az login\n```\n\nSkyplane should now be able to authenticate with Azure although you may need to pass your subscription ID to `skyplane init` later.\n</details>\n\n### Importing cloud credentials into Skyplane\n\nAfter authenticating with each cloud provider, you can run `skyplane init` to create a configuration file for Skyplane.\n\n```bash\n$ skyplane init\n```\n<details>\n<summary>skyplane init output</summary>\n<br>\n\n```\n$ skyplane init\n\n====================================================\n _____ _   ____   _______ _       ___   _   _  _____\n/  ___| | / /\\ \\ / / ___ \\ |     / _ \\ | \\ | ||  ___|\n\\ `--.| |/ /  \\ V /| |_/ / |    / /_\\ \\|  \\| || |__\n `--. \\    \\   \\ / |  __/| |    |  _  || . ` ||  __|\n/\\__/ / |\\  \\  | | | |   | |____| | | || |\\  || |___\n\\____/\\_| \\_/  \\_/ \\_|   \\_____/\\_| |_/\\_| \\_/\\____/\n====================================================\n\n\n(1) Configuring AWS:\n    Loaded AWS credentials from the AWS CLI [IAM access key ID: ...XXXXXX]\n    AWS region config file saved to /home/ubuntu/.skyplane/aws_config\n\n(2) Configuring Azure:\n    Azure credentials found in Azure CLI\n    Azure credentials found, do you want to enable Azure support in Skyplane? [Y/n]: Y\n    Enter the Azure subscription ID: [XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX]:\n    Azure region config file saved to /home/ubuntu/.skyplane/azure_config\n    Querying for SKU availbility in regions\n    Azure SKU availability cached in /home/ubuntu/.skyplane/azure_sku_mapping\n\n(3) Configuring GCP:\n    GCP credentials found in GCP CLI\n    GCP credentials found, do you want to enable GCP support in Skyplane? [Y/n]: Y\n    Enter the GCP project ID [XXXXXXX]:\n    GCP region config file saved to /home/ubuntu/.skyplane/gcp_config\n\nConfig file saved to /home/ubuntu/.skyplane/config\n```\n\n</details>\n\n# Using Skyplane\n\nThe easiest way to use Skyplane is to use the CLI. `skyplane cp` supports any local path or cloud object store destination as an argument.\n\n```bash\n# copy files between two AWS S3 buckets\n$ skyplane cp s3://... s3://...\n\n# copy files from an AWS S3 bucket to a GCP GCS bucket\n$ skyplane cp s3://... gs://...\n\n# copy files from a local directory to/from a cloud object store\n$ skyplane cp /path/to/local/files gs://...\n```\n\nSkyplane also supports incremental copies via `skyplane sync`:    \n```bash\n# copy changed files from S3 to GCS\n$ skyplane sync s3://... gcs://...\n```\n\n`skyplane sync` will diff the contents of the source and destination and only copy the files that are different or have changed. It will not delete files that are no longer present in the source so it's always safe to run `skyplane sync`.\n\n## Accelerating transfers\n### Use multiple VMs\n\nWith default arguments, Skyplane sets up a one VM (called gateway) in the source and destination regions. We can further accelerate the transfer by using more VMs.\n\nTo double the transfer speeds by using two VMs in each region, run:\n```bash\n$ skyplane cp s3://... s3://... -n 2\n```\n\n⚠️ If you do not have enough vCPU capacity in each region, you may get a InsufficientVCPUException. Either request more vCPUs or reduce the number of parallel VMs.\n\n### Stripe large objects across multiple VMs\nSkyplane can transfer a single large object across multiple VMs to accelerate transfers. Internally, Skyplane will stripe the large object into many small chunks which can be transferred in parallel.\n\nTo stripe large objects into multiple chunks, run:\n```bash\n$ skyplane cp s3://... s3://... --max_chunk_size_mb 16\n```\n\n⚠️ Large object transfers are only supported for transfers between AWS S3 buckets at the moment.\n",
    'author': 'Skyplane authors',
    'author_email': 'skyplaneproject@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/skyplane-project/skyplane',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
