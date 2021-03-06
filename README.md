# omaha-server

[![Build Status](https://travis-ci.org/brave/omaha-server.svg?branch=master)](https://travis-ci.org/brave/omaha-server)
[![Coverage Status](https://coveralls.io/repos/brave/omaha-server/badge.png?branch=master)](https://coveralls.io/r/brave/omaha-server?branch=master)
[![Code Health](https://landscape.io/github/brave/omaha-server/master/landscape.svg?style=flat)](https://landscape.io/github/brave/omaha-server/master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/brave/omaha-server/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/brave/omaha-server/?branch=master)
[![Apache License, Version 2.0](https://img.shields.io/badge/license-Apache%202.0-red.svg)](https://github.com/brave/omaha-server/blob/master/LICENSE)
[![](https://badge.imagelayers.io/brave/omaha-server:master.svg)](https://imagelayers.io/?images=brave/omaha-server:master 'Get your own badge on imagelayers.io')

Google Omaha server implementation and Sparkle (mac) feed management.

Currently, our implementation is integrated into the updating processes of several organisations for products that require sophisticated update logic and advanced usage statistics. We provide additional support and further enhancement on a contract basis. For a case study and enquiries please refer [our website](https://www.crystalnix.com/case-study/google-omaha)

## Setting up a development server

**Requirements:**

- Ubuntu Trusty 14.04 (LTS) (64-bit)
- [pipenv](https://pipenv.readthedocs.io/en/latest/)
- [docker](docker.com) or [boot2docker](https://github.com/boot2docker/boot2docker) for OS X & Windows
- [docker-compose](https://docs.docker.com/compose/install/)

```shell
$ sudo apt-get update
$ sudo apt-get install docker.io
$ sudo apt-get install python python-pip
$ sudo pip install -U pipenv
$ sudo pip install -U docker-compose
$ git clone https://github.com/brave/omaha-server.git
$ cd omaha-server
# Up local environment
$ make up

# Stop server
$ make stop
```

Open `http://{DOCKER_HOST}:9090/admin/`

- username: `admin`
- password: `admin`

## Setting up a development environment

**Requirements:**

- python 3.7
- [pipenv](https://pipenv.readthedocs.io/en/latest/)
- PostgreSQL
- Redis

```shell
$ sudo pip install -U pipenv
$ make install-dev
```

## Activate virtual environment

```shell
$ pipenv shell
```

### Tests

```shell
$ make test
```

## Statistics

All statistics are stored in Redis. In order not to lose all data, we recommend to set up the backing up process. The proposed solution uses ElastiCache which supports [automatic backups](https://aws.amazon.com/en/blogs/aws/backup-and-restore-elasticache-redis-nodes/). In the case of a self-hosted solution do not forget to set up backups.

Required `userid`. [Including user id into request](https://github.com/Crystalnix/omaha/wiki/Omaha-Client-working-with-protocol#including-user-id-into-request)

## Utils

A command for generating fake data such as requests, events and statistics:

```shell
# Usage: ./manage.py generate_fake_data [options] <app_id>
# Options:
#     --count=COUNT         Total number of data values (default: 100)
$ ./manage.py generate_fake_data {F07B3878-CD6F-4B96-B52F-95C4D2} --count=20
```

A command for generating fake statistics:

```shell
# Usage: ./manage.py generate_fake_statistics [options]
# Options:
#     --count=COUNT         Total number of data values (default: 100)
$ ./manage.py generate_fake_statistics --count=3000
```

A command for generating fake live data:

```shell
# Usage: ./manage.py generate_fake_live_data <app_id>
#
$ ./manage.py generate_fake_live_data {c00b6344-038f-4e51-bcb1-33ffdd812d81}
```

A command for generating fake live data for Mac:

```shell
# Usage: ./manage.py generate_fake_mac_live_data <app_name> <channel>
#
$ ./manage.py generate_fake_mac_live_data Application alpha
```

## Deploying Omaha-Server to AWS

**Requirements:**

- [Sentry](https://github.com/getsentry/sentry)
		+ [SetUp Sentry as self-hosted solution](https://docs.sentry.io/server/installation/)
		+ [Sentry as SaaS solution](https://www.getsentry.com/)
- AWS RDS: [Creating a DB Instance Running the PostgreSQL Database Engine](http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreatePostgreSQLInstance.html)
- Redis instance in AWS ElasticCache: [Documentation](http://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/GettingStarted.CreateCluster.Redis.html)
- AWS S3: [Create a Bucket](http://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html)
- [AWS Access Key ID and Secret Access Key](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html)

#### Environment variables

| Environment variable name |    Description       |       Default value        |
|---------------------------|----------------------|----------------------------|
| APP_VERSION               | App version          | DEV                        |
| DJANGO_SETTINGS_MODULE    |                      | omaha_server.settings      |
| SECRET_KEY                | Django SECRET_KEY    |                            |
| HOST_NAME                 | App host name        |                            |
| DB_HOST                   | DB Host              | 127.0.0.1                  |
| DB_USER                   | DB User              | postgres                   |
| DB_NAME                   | DB Name              | postgres                   |
| DB_PASSWORD               | DB Password          | ''                         |
| DB_PORT                   | DB port              | 5432                       |
| AWS_ACCESS_KEY_ID         | AWS Access Key       |                            |
| AWS_SECRET_ACCESS_KEY     | AWS Secret Key       |                            |
| AWS_STORAGE_BUCKET_NAME   | S3 storage bucket    |                            |
| RAVEN_DSN                 | Sentry url           |                            |
| RAVEN_DSN_STACKTRACE      | Sentry url           | RAVEN_DSN                  |
| REDIS_HOST                | Redis host           | 127.0.0.1                  |
| REDIS_PORT                | Redis port           | 6379                       |
| REDIS_DB                  | Redis db             | 1                          |
| REDIS_STAT_PORT           | For statistics       | REDIS_PORT                 |
| REDIS_STAT_HOST           |                      | REDIS_HOST                 |
| REDIS_STAT_DB             |                      | 15                         |
| UWSGI_PROCESSES           |                      |                            |
| UWSGI_THREADS             |                      |                            |
| OMAHA_SERVER_PRIVATE      | Is private server    | False                      |
| DB_PUBLIC_USER            |                      |                            |
| DB_PUBLIC_PASSWORD        |                      |                            |
| AWS_ROLE                  |                      |                            |
| OMAHA_URL_PREFIX          | no trailing slash!   |                            |
| SENTRY_STACKTRACE_API_KEY | Auth API token       |                            |
| OMAHA_ONLY_HTTPS          | HTTPS-only           | False                      |
| CUP_REQUEST_VALIDATION    |                      | False                      |
| CRASH_TRACKER             | Sentry, ELK          | Sentry                     |
| LOGSTASH_HOST             | Logstash host        |                            |
| LOGSTASH_PORT             | Logstash TCP port    |                            |
| FILEBEAT_HOST             | Filebeat host        | 127.0.0.1                  |
| FILEBEAT_PORT             | Filebeat UDP port    | 9021                       |
| ELK_HOST                  | Logstash host        | ''                         |
| ELK_PORT                  | Logstash TCP port    | ''                         |
| FILEBEAT_DESTINATION      | filebeat output type | ''                         |
| LOG_NGINX_TO_FILEBEAT     | Send logs to filebeat| 'True'                     |
| EMAIL_SENDER              | Verified SES email   |                            |
| EMAIL_RECIPIENTS          | Feedback recepients  |                            |
| RSYSLOG_ENABLE            | Send logs to rsyslog | ''                         |



- [uWSGI Options](http://uwsgi-docs.readthedocs.org/en/latest/Options.html) & [Environment variables](http://uwsgi-docs.readthedocs.org/en/latest/Configuration.html#environment-variables)
- [Sentry](https://github.com/getsentry/sentry)
- Sentry API key is stored on the way Sentry Organization page -> API Keys

#### Enable Client Update Protocol v2

1. Use [Omaha eckeytool](https://github.com/google/omaha/tree/master/omaha/tools/eckeytool) to generate private.pem key and cup_ecdsa_pubkey.{KEYID}.h files.
2. Add cup_ecdsa_pubkey.{KEYID}.h to Omaha source directory /path/to/omaha/omaha/net/, set CupEcdsaRequestImpl::kCupProductionPublicKey in /path/to/omaha/omaha/net/cup_ecdsa_request.cc to new key and build Omaha client.
3. Add private.pem keyid and path to omaha CUP_PEM_KEYS dictionary.

## Links

- Presentation: [omaha-server High Fidelity, High Velocity Deployments in the Cloud](http://slides.com/andreylisin/omaha-server/#/)

## Contributors

Thanks to [Abiral Shrestha](https://twitter.com/proabiral) for the security reports and suggestions.

## Copyright and license

This software is licensed under the Apache 2 license, quoted below.

Copyright 2014 [Crystalnix Limited](http://crystalnix.com)

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License. You may obtain a copy of
the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
