import importlib,time,sys,os
start=time.time()
import pandas as pd,numpy as np
import smallpower.smallPower as smallPower
from smallpower import conf
import dorianUtils.comUtils as com
from dorianUtils.comUtils import html_table
from dorianUtils.comUtils import print_file
importlib.reload(smallPower)
importlib.reload(com)

def download_data(t0,t1,tags):
    import subprocess as sp,os
    listDays=[cfg.streamer.to_folderday(k) for k in pd.date_range(t0,t1,freq='D')]
    for d in listDays:
        for t in tags:
            sp.run('scp sylfenGaston:data_ext/smallPower_daily/'+d+t+'.pkl'+ ' ' + cfg.folderPkl+'/'+d,shell=True)

folder_figures='/home/dorian/sylfen/programmerBible/doc/pictur/'
cfg=smallPower.SmallPowerComputer()
# t0 = pd.Timestamp('2022-02-13 08:00',tz='CET')
t0 = pd.Timestamp('2022-02-13 08:00',tz='CET')
t1 = pd.Timestamp('2022-02-22 22:00',tz='CET')

# t0 = pd.Timestamp('2022-06-01 14:00',tz='CET')
# t1 = pd.Timestamp('2022-06-02 01:00',tz='CET')
#
tags = cfg.getTagsTU('O2.*[FP]T.*hm05')
tags += cfg.getTagsTU('GF[CD]_02.*PT')

##### look at periods where we have the 4 stacks working
tags = cfg.getTagsTU('alim.*it.*hm05$')
# download_data(t0,t1,tags)
start=time.time()
df = cfg.loadtags_period(t0,t1,tags,rs='3600s',rsMethod="mean",closed='right')

# df.to_pickle('df_issue38.pkl')
# print(time.time()-start)

# sys.exit()
fig = cfg.multiUnitGraphSP(df.astype(float))
colors=cfg.utils.colors_mostdistincs
for k,trace in enumerate(fig.data):
    trace.marker.color=colors[k]
    trace.marker.symbol='circle'
    trace.line.color=colors[k]
    trace.line.dash='solid'
# fig = cfg.update_lineshape_fig(fig)
# fig = cfg.utils.multiUnitGraph(df.astype(float))
fig.show()
