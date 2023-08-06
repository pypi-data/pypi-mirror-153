from smallpower.smallPower import SmallPowerComputer
import pandas as pd
import pickle
cfg=SmallPowerComputer()

# t1=pd.Timestamp.now(tz='CET')
t0=pd.Timestamp('2022-01-01',tz='CET')
t1=t0+pd.Timedelta(days=60)
tags=cfg.getUsefulTags('Courant alimentation stack')[:4]
df=cfg.loadtags_period(t0,t1,tags,rs='60s')
df.to_pickle('df_courant.pkl')
