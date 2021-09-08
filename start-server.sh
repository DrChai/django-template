#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
# Other commands e.g.:
# Sync Solr Index
# python manage.py build_solr_schema --filename=/solrdata/default/conf/schema.xml --using=default && curl 'http://solr:8983/solr/admin/cores?action=RELOAD&core=default&wt=json&indent=true'
echo Finished Sync.
exec "$@"