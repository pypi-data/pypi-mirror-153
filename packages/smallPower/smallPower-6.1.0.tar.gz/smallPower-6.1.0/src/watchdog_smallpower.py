import pandas as pd,sys,os
import smallPowerDash.smallPower as smallPower
from dorianUtils.utilsD import EmailSmtp
import psycopg2
import subprocess as sp
import time
import traceback
import psutil
import logging
timenowstd = lambda :pd.Timestamp.now().strftime('%d %b %H:%M:%S =>')

dsp = smallPower.SmallPower_dumper()
logfile_name= os.path.dirname(os.path.realpath(__file__))+'/check.err'
logerror_file=open(logfile_name,'w+')

# --------------#
#   FUNCTIONS   #
# --------------#
debug=False

def sendMail(error):
    # locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    smtp = EmailSmtp()
    smtp.host = 'smtp.office365.com'
    smtp.port = 587
    smtp.user = "dorian.drevon@sylfen.com"
    smtp.password = "Alpha$02"
    smtp.isTls = True
    sender = "Dorian Drevon <dorian.drevon@sylfen.com>"
    destinataires = ["drevondorian@gmail.com"]
    # destinataires += ["marc.potron@sylfen.com"]
    content=error['msg'].upper()
    sub = "WARNING : dashboard smallPower ERROR :" + str(error['code'])
    smtp.sendMessage(fromAddr = sender,toAddrs = destinataires,subject = sub,content = content)

def notify_error(tb,error):
    logerror_file.write('-'*60 +'\n'+' '*20 + error['msg']+'\n')
    traceback.print_exception(*tb,file=logerror_file)
    logerror_file.write('-'*60+'\n')
    sendMail(error)

def warning(error):
    logerror_file.write('-'*60 +'\n'+ error['msg']+'\n')
    logerror_file.write('-'*60+'\n')
    sendMail(error)

def isProcessRunning(ps_name):
    ps_list=[k for k in sp.check_output('ps aux | grep '+ps_name,shell=True).decode().split('\n') if 'python' in k]
    if len(ps_list)==0:return 'process '+ps_name+' is not running'
    elif len(ps_list)>1:return 'several processes corresponding to'+ps_name+' are running simultaneously'
    else : return True

# -----------#
#   CHECKS   #
# -----------#
# make sure you can connect to database
try:
    conn=dsp.connect2db()
except Exception:
    error={'msg':'impossible to connect to database'+dsp.dbParameters['dbname'],'code':1}
    notify_error(sys.exc_info(),error)

# make sure you can read the data from database
try:
    start=time.time()
    df= pd.read_sql("select * from " + dsp.dbTable + " where tag~'GFC_01.*PT' order by timestampz asc;",conn)
    elapsed_time=(time.time()-start)
except:
    error={'msg':'impossible to read in database '+ dsp.dbParameters['dbname'] + 'for table ' + dbTable,'code':2}
    notify_error(sys.exc_info(),error)

# check that feeding the data base is still ok by requesting the database last values for a given tag
if df.empty or debug:
    error={'msg':timenowstd()+'database ' + dsp.dbParameters['dbname'] + ' is empty','code':3}
    warning(error)

# 2. make sure the time it takes to get the answer is less than 15 seconds.
if elapsed_time>15 or debug:
    error={'msg':timenowstd()+'it took :'+str(int(elapsed_time))+' seconds to read the data in '+dsp.dbParameters['dbname'],'code':4}
    warning(error)

# 3. make sure it is feeding looking at the last timestamp not being older than 20 minutes
if not df.empty or debug:
    max_ts=df['timestampz'].max().tz_convert(dsp.tz_record)
    if pd.Timestamp.now(dsp.tz_record)-max_ts>pd.Timedelta(minutes=20) or debug:
        error={'msg':timenowstd()+'==> database ' + dsp.dbParameters['dbname'] + ' most recent timestamp is '+max_ts.strftime('%d %b %H:%M:%S'),'code':5}
        warning(error)

# 3. check disk space is still ok < 80%
hdd = psutil.disk_usage('/').percent
if hdd>85 or debug:
    error={'msg':timenowstd()+'be careful disk usage is:'+str(hdd)+'%. There may be some problems flushing the database.','code':6}
    warning(error)
if hdd>95 or debug:
    error={'msg':timenowstd()+'Disk almost full.'+str(hdd)+'%. Just shutting down dumpers.','code':7}
    warning(error)
    # sp.check_output('pkill -f dumpSmallPower',shell=True)

# 4. check if dumper and server are still running
try:
    msg=isProcessRunning('dumpSmallPower')
    if not msg is True:
        raise Exception(msg)
except:
    error={'msg':'not running','code':8}
    notify_error(sys.exc_info(),error)

try:
    msg=isProcessRunning('appSmallPower')
    if not msg is True:
        raise Exception(msg)
except:
    error={'msg':'appSmallPower not runing.','code':8}
    notify_error(sys.exc_info(),error)


logerror_file.close()
sys.exit()
