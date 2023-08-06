SCRIPT_FILE=$0
SCRIPT_DIR=`(cd \`dirname ${SCRIPT_FILE}\`; pwd)`
NAMEAPP=${SCRIPT_DIR%/*}/src/dumpSmallPower.py
# echo $NAMEAPP
. ${SCRIPT_DIR}/start_smallpowerJob.sh $NAMEAPP
