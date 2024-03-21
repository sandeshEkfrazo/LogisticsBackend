#!/bin/bash


NAME="logistics_project" 
DJANGODIR=/logistics/django/logistics_project
DJANGOENVDIR=/logistics/logi
SOCKFILE=/logistics/logi/run/gunicorn.sock 
USER=root  
GROUP=root   
NUM_WORKERS=3 
DJANGO_SETTINGS_MODULE=logistics_project.settings
DJANGO_WSGI_MODULE=logistics_project.wsgi  

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /logistics/logi/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ${DJANGOENVDIR}/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
