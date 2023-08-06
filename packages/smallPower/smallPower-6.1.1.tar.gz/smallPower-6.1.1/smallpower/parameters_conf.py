PARKING_TIME  = 60*10 #### in seconds
ENDPOINTURL   = 'opc.tcp://10.10.38.100'
PORT_BECKHOFF = 4840
NAMESPACE_BECKHOFF = "ns=4;s=GVL."
DB_PARAMETERS = {
    'host'     : "localhost",
    'port'     : "5432",
    'dbname'   : "jules",
    'user'     : "postgres",
    'password' : "sylfenbdd"
}
DB_TABLE  = 'realtimedata'
TZ_RECORD = 'CET'
SIMULATOR = False
FOLDERPKL = '/home/dorian/data/sylfenData/smallPower_daily/'

ALL = {k:eval(k) for k in ['PARKING_TIME','DB_PARAMETERS','DB_TABLE','TZ_RECORD','SIMULATOR','FOLDERPKL']}

## working with the simulator ?
if SIMULATOR:
    PORT_BECKHOFF=4860
    DB_PARAMETERS['dbname'] = "juleslocal"
    DB_TABLE = 'test_realtimedata'
    ENDPOINTURL  = 'opc.tcp://127.0.0.1'
    FOLDERPKL = FOLDERPKL.replace('smallPower_daily','smallpower_test/')
