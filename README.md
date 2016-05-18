# README #

Script for automatically pulling data from API and generating flatstore feeds.

### How to setup ###

Create a virtualenv and clone the repo into the new environment:

```
#!bash

virtualenv fsp_api_client
cd fsp_api_client
git clone git@bitbucket.org:peterhinson/fspflatstoreapiclient.git fsp_api_client


```

Activate the virtualenv and install package requirements using pip:

```
#!bash

source bin/activate
cd fsp_api_client
pip install -r requirements.txt

```

Use crontab to set a cron job running main.py daily (or more often if desired). Be sure to use the virtualenv python executable:


```
#!bash

crontab -e

PATH=/home/lnkd/fsp_api_client/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/home/phinson/bin
30	0	*	*	*	/home/lnkd/fsp_api_client/bin/python /home/lnkd/fsp_api_client/fsp_api_client/main.py >> /home/lnkd/fsp_api_client/fsp_api_client/logs/cronrun

```

Create config_local.py using the template provided in config_local.sample.py. Configure upload paths. Make sure that the target upload directory exists.

Note: output.sql will be generated in the output directory. This file contains queries to to link all Drupal feeds to the newly generated files csv files. You should only need to apply this SQL after the first run. Metadata is also updated for each dataset.

### Drupal Configuration ###

In Drupal's dataset content-type settings (/admin/content/node-type/dataset):

* Disable ' Pause automatic feed update' (under Feed API -> Default Setting)
* Set 'Supply feed as:' to URL (under Feed API)
* Disable revisions (under workflow)

Drupal settings:

* Clear caches
* Configure cron to run at least daily
* May need to manually disable 'pause update' for each dataset (manage content -> datasets)

Flatstore tables will be updated on cron run.