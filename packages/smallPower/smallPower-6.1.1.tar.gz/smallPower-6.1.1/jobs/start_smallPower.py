import subprocess as sp,sys
# simulator = sys.argv[1]
#usage : -d:start also the dumper
#        -s:start also the simulator
#        -w:start the watchdog
#        -a:start the app.py web service
#        -f:start all

# if no flag was used only the conf is imported
simulator=True
python_env='python'
if 'sylfen' in os.getenv('HOME'):
    baseFolder   = '/home/sylfen/data_ext/'
else:
    baseFolder   = '/home/dorian/data/sylfenData/'

db_name      = "jules"
dbtable_name = "realtime_data"
folderpkl    = baseFolder+'smallpower_daily/'

## should be the simulator started ?
if simulator:
    db_name      = "juleslocal"
    dbtable_name = "realtime_data"
    folderpkl    = baseFolder+'smallpower_test/'
    sp.Popen(python_env + " src/simulator_smallpower.py")

## start dumper
sp.Popen(python_env + " src/dumper_smallpower.py")
## start app
sp.Popen(python_env + " smallPower_js/app.py")
## start watchdog
sp.Popen(python_env + " src/watchdog_smallpower.py")
