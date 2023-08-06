HOST='sylfenGastonFibre'
# HOST='sylfenGaston'
VENV="/home/sylfen/.venv/venv_smallpower"
APP_PATH=$1

PATH_STARTJOB="/home/dorian/sylfen/toPushGaston/startjob.sh"
. $PATH_STARTJOB $HOST $VENV $APP_PATH
