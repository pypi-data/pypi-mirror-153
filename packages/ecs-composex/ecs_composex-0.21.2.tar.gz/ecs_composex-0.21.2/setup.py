# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecs_composex',
 'ecs_composex.acm',
 'ecs_composex.alarms',
 'ecs_composex.appmesh',
 'ecs_composex.cloudmap',
 'ecs_composex.codeguru_profiler',
 'ecs_composex.cognito_userpool',
 'ecs_composex.common',
 'ecs_composex.common.stacks',
 'ecs_composex.compose',
 'ecs_composex.compose.compose_secrets',
 'ecs_composex.compose.compose_services',
 'ecs_composex.compose.compose_services.service_image',
 'ecs_composex.compose.compose_services.service_logging',
 'ecs_composex.compose.compose_volumes',
 'ecs_composex.compose.x_resources',
 'ecs_composex.dashboards',
 'ecs_composex.docdb',
 'ecs_composex.dynamodb',
 'ecs_composex.ecs',
 'ecs_composex.ecs.ecs_family',
 'ecs_composex.ecs.ecs_family.family_logging',
 'ecs_composex.ecs.ecs_firelens',
 'ecs_composex.ecs.ecs_firelens.ecs_firelens_advanced',
 'ecs_composex.ecs.ecs_firelens.helpers',
 'ecs_composex.ecs.ecs_prometheus',
 'ecs_composex.ecs.ecs_service',
 'ecs_composex.ecs.helpers',
 'ecs_composex.ecs.managed_sidecars',
 'ecs_composex.ecs.service_alarms',
 'ecs_composex.ecs.service_compute',
 'ecs_composex.ecs.service_networking',
 'ecs_composex.ecs.service_scaling',
 'ecs_composex.ecs.task_compute',
 'ecs_composex.ecs.task_iam',
 'ecs_composex.ecs_cluster',
 'ecs_composex.efs',
 'ecs_composex.elasticache',
 'ecs_composex.elbv2',
 'ecs_composex.elbv2.elbv2_stack',
 'ecs_composex.events',
 'ecs_composex.iam',
 'ecs_composex.kinesis',
 'ecs_composex.kinesis_firehose',
 'ecs_composex.kms',
 'ecs_composex.neptune',
 'ecs_composex.opensearch',
 'ecs_composex.rds',
 'ecs_composex.route53',
 'ecs_composex.s3',
 'ecs_composex.secrets',
 'ecs_composex.sns',
 'ecs_composex.specs',
 'ecs_composex.sqs',
 'ecs_composex.ssm_parameter',
 'ecs_composex.utils',
 'ecs_composex.vpc']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'boto3>=1.20',
 'compose-x-common>=1.0.1,<2.0.0',
 'compose-x-render>=0.5,<0.6',
 'importlib-resources>=5.4.0,<6.0.0',
 'jsonschema>=4.4.0,<5.0.0',
 'requests>=2.27.1,<3.0.0',
 'retry2>=0.9.3,<0.10.0',
 'tabulate>=0.8.9,<0.9.0',
 'troposphere>=4.0.0,<5.0.0',
 'urllib3>=1.26.8,<2.0.0']

extras_require = \
{'ecrscan': ['ecr-scan-reporter>=0.4,<0.5']}

entry_points = \
{'console_scripts': ['compose-x = ecs_composex.cli:main',
                     'ecs-compose-x = ecs_composex.cli:main',
                     'ecs_compose_x = ecs_composex.cli:main']}

setup_kwargs = {
    'name': 'ecs-composex',
    'version': '0.21.2',
    'description': 'Manage, Configure and Deploy your services and AWS services and applications from your docker-compose definition',
    'long_description': '.. meta::\n    :description: ECS Compose-X\n    :keywords: AWS, ECS, Fargate, Docker, Containers, Compose, docker-compose\n\n============\nECS ComposeX\n============\n\n|PYPI_VERSION| |PYPI_LICENSE| |PY_DLS|\n\n|CODE_STYLE| |TDD| |BDD|\n\n|QUALITY|\n\n|BUILD|\n\n-----------------------------------------------\nThe no-code CDK for docker-compose & AWS ECS\n-----------------------------------------------\n\nDeploy your services to AWS ECS from your docker-compose files in 3 steps\n\n* Step 1. Install ECS Compose-x\n* Step 2. Use your existing docker-compose files. Optionally, add Compose-X extensions.\n* Step 3. Deploy to AWS via CloudFormation.\n\n\nWhat does it do?\n========================\n\n* Help developers/SRE/Cloud engineers to deploy applications to AWS using docker-compose syntax\n    * Generates CloudFormation templates out of the Compose Files\n    * Links services and AWS Resources together via IAM / Networking / Configuration\n    * Detects mis-configurations and autocorrects wherever possible\n\n* Use/Re-use existing docker-compose files and compose specifications\n    * Supports docker-compose specification 3.7+\n    * Performs JSON validation of input to improve reliability\n    * Enable/disable features to run in AWS Fargate automatically\n\n* Expand the definitions with AWS CloudFormation resources\n    * For supported resources, supports full CloudFormation properties\n    * For existing resources, will detect them and allow to use the ``Return Values`` with other components\n\n* Allows to use existing resources in your AWS Account\n* Can be extended with custom modules/hooks\n\n\nUseful Links\n===============\n\n* `Documentation`_\n* `Labs <https://labs.compose-x.io/>`_\n* `Feature requests`_\n* `Issues`_\n* `Compatibility Matrix`_\n\n\nInstallation\n=====================\n\n.. code-block:: bash\n\n    # Inside a python virtual environment\n    python3 -m venv venv\n    source venv/bin/activate\n    pip install pip -U\n    pip install ecs-composex\n\n    # For your user only\n    pip install ecs-composex --user\n\nUsage\n======\n\n.. code-block:: bash\n\n    # Get all the options\n    ecs-compose-x -h\n\n    # Simple example using docker-compose file and an extension with your AWS Settings\n    ecs-compose-x render -d templates -n my-new-stack -f docker-compose.yaml -f aws-settings.yaml\n\n\n.. _`Mark Peek`: https://github.com/markpeek\n.. _`AWS ECS CLI`: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI.html\n.. _Troposphere: https://github.com/cloudtools/troposphere\n.. _Blog: https://blog.compose-x.io/\n.. _Docker Compose: https://docs.docker.com/compose/\n.. _ECS ComposeX: https://docs.compose-x.io\n.. _YAML Specifications: https://yaml.org/spec/\n.. _Extensions fields:  https://docs.docker.com/compose/compose-file/#extension-fields\n.. _ECS ComposeX Project: https://github.com/orgs/lambda-my-aws/projects/3\n.. _CICD Pipeline for multiple services on AWS ECS with ECS ComposeX: https://blog.compose-x.io/posts/cicd-pipeline-for-multiple-services-on-aws-ecs-with-ecs-composex/\n.. _Feature requests: https://github.com/compose-x/ecs_composex/issues/new?assignees=JohnPreston&labels=enhancement&template=feature_request.md&title=%5BFR%5D+%3Caws+service%7Cdocker+compose%3E+\n.. _Issues: https://github.com/compose-x/ecs_composex/issues/new?assignees=JohnPreston&labels=bug&template=bug_report.md&title=%5BBUG%5D\n\n\n.. _AWS ECS:            https://nightly.docs.compose-x.io/syntax/composex/ecs.html\n.. _AWS VPC:            https://nightly.docs.compose-x.io/syntax/composex/vpc.html\n.. _AWS RDS:            https://nightly.docs.compose-x.io/syntax/composex/rds.html\n.. _AWS DynamoDB:       https://nightly.docs.compose-x.io/syntax/composex/dynamodb.html\n.. _AWS DocumentDB:     https://nightly.docs.compose-x.io/syntax/composex/docdb.html\n.. _AWS ACM:            https://nightly.docs.compose-x.io/syntax/composex/acm.html\n.. _AWS ELBv2:          https://nightly.docs.compose-x.io/syntax/composex/elbv2.html\n.. _AWS S3:             https://nightly.docs.compose-x.io/syntax/composex/s3.html\n.. _AWS IAM:            https://nightly.docs.compose-x.io/syntax/composex/ecs.details/iam.html\n.. _AWS Kinesis:        https://nightly.docs.compose-x.io/syntax/composex/kinesis.html\n.. _AWS SQS:            https://nightly.docs.compose-x.io/syntax/composex/sqs.html\n.. _AWS SNS:            https://nightly.docs.compose-x.io/syntax/composex/sns.html\n.. _AWS KMS:            https://nightly.docs.compose-x.io/syntax/composex/kms.html\n.. _AWS ElastiCache:    https://nightly.docs.compose-x.io/syntax/composex/elasticache.html\n.. _AWS EC2:            https://nightly.docs.compose-x.io/features.html#ec2-resources-for-ecs-cluster\n.. _AWS AppMesh:        https://nightly.docs.compose-x.io/readme/appmesh.html\n.. _AWS CloudWatch:     https://nightly.docs.compose-x.io/syntax/compose_x/alarms.html\n.. _Lookup:             https://nightly.docs.compose-x.io/syntax/compose_x/common.html#lookup\n.. _the compatibilty matrix: https://nightly.docs.compose-x.io/compatibility/docker_compose.html\n.. _Compatibility Matrix: https://nightly.docs.compose-x.io/compatibility/docker_compose.html\n.. _Find out how to use ECS Compose-X in AWS here: https://blog.compose-x.io/posts/use-your-docker-compose-files-as-a-cloudformation-template/index.html\n.. _Documentation: https://docs.compose-x.io\n\n.. |BUILD| image:: https://codebuild.eu-west-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiWjIrbSsvdC9jZzVDZ3N5dVNiMlJCOUZ4M0FQNFZQeXRtVmtQbWIybUZ1ZmV4NVJEdG9yZURXMk5SVVFYUjEwYXpxUWV1Y0ZaOEcwWS80M0pBSkVYQjg0PSIsIml2UGFyYW1ldGVyU3BlYyI6Ik1rT0NaR05yZHpTMklCT0MiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main\n\n.. |PYPI_VERSION| image:: https://img.shields.io/pypi/v/ecs_composex.svg\n        :target: https://pypi.python.org/pypi/ecs_composex\n\n.. |PYPI_DL| image:: https://img.shields.io/pypi/dm/ecs_composex\n    :alt: PyPI - Downloads\n    :target: https://pypi.python.org/pypi/ecs_composex\n\n.. |PYPI_LICENSE| image:: https://img.shields.io/pypi/l/ecs_composex\n    :alt: PyPI - License\n    :target: https://github.com/compose-x/ecs_composex/blob/master/LICENSE\n\n.. |PYPI_PYVERS| image:: https://img.shields.io/pypi/pyversions/ecs_composex\n    :alt: PyPI - Python Version\n    :target: https://pypi.python.org/pypi/ecs_composex\n\n.. |PYPI_WHEEL| image:: https://img.shields.io/pypi/wheel/ecs_composex\n    :alt: PyPI - Wheel\n    :target: https://pypi.python.org/pypi/ecs_composex\n\n.. |CODE_STYLE| image:: https://img.shields.io/badge/codestyle-black-black\n    :alt: CodeStyle\n    :target: https://pypi.org/project/black/\n\n.. |TDD| image:: https://img.shields.io/badge/tdd-pytest-black\n    :alt: TDD with pytest\n    :target: https://docs.pytest.org/en/latest/contents.html\n\n.. |BDD| image:: https://img.shields.io/badge/bdd-behave-black\n    :alt: BDD with Behave\n    :target: https://behave.readthedocs.io/en/latest/\n\n.. |QUALITY| image:: https://sonarcloud.io/api/project_badges/measure?project=compose-x_ecs_composex&metric=alert_status\n    :alt: Code scan with SonarCloud\n    :target: https://sonarcloud.io/dashboard?id=compose-x_ecs_composex\n\n.. |PY_DLS| image:: https://img.shields.io/pypi/dm/ecs-composex\n    :target: https://pypi.org/project/ecs-composex/\n',
    'author': 'John Preston',
    'author_email': 'john@compose-x.io',
    'maintainer': 'John Preston',
    'maintainer_email': 'john@compose-x.io',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
