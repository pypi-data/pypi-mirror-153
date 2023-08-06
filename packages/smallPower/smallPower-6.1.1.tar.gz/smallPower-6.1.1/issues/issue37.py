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
import issues
importlib.reload(issues)

cfg=smallPower.SmallPowerComputer()
vm=issues.VersionsManager(cfg.folderPkl)

folderCEA='/data2/CEA_data/'
t0 = pd.Timestamp('2021-11-01 00:00',tz='CET')
t1 = pd.Timestamp('2022-02-28 00:00',tz='CET')
rs,rsMethod='60s','mean'
infos=pd.read_excel('data/liste_exportALPHA_versCEA_issue37.xlsx',skiprows=7)
tags=[t for t in infos.TAG if t in list(cfg.dfplc.index)]

##### easy tags in plc
def easy_tags():
    # tags=tags[:14]
    easy_tags=tags[:4]
    # p=vm.presence_tags(tags,True)
    # issues.download_data(t0,t1,tags)
    start=time.time()
    df = cfg.loadtags_period(t0,t1,easy_tags,pool='auto',rs=rs,rsMethod=rsMethod,closed='right',verbose=True)
    issues.push_toFolderGaston(df,'issue37_easy_tags',folderCEA)
    print(time.time()-start)
    sys.exit()

#### courants HC13
def courant_HC13():
    tag_courant_hc13=[t for k,t in enumerate(infos.TAG.fillna('unassigned')) if 'HC13' in t]
    tags_needed=[t.strip('.HC13') for t in tag_courant_hc13]
    # t1 = pd.Timestamp('2022-02-01 00:00',tz='CET')
    # issues.download_data(t0,t1,tags_needed)
    # p=vm.presence_tags(tags_needed,True)
    # issues.download_data(t0,t1,tags_needed)
    courants_HC13 = -cfg.loadtags_period(t0,t1,tags_needed,pool='auto',rs=rs,rsMethod=rsMethod,closed='right',verbose=True)
    issues.push_toFolderGaston(courants_HC13,'issue37_courants_HC13',folderCEA)
    sys.exit()

##### other tags
idx_rows_no_tag=[k for k,t in enumerate(infos.TAG) if t not in list(cfg.dfplc.index)]
infos_otherTags=infos.loc[idx_rows_no_tag]

### debit h2O
def debitH2O():
    tags_needed=['SEH1.L213_H2OPa_FT_01.HM05','SEH1.L213_H2OPb_FT_01.HM05']
    # p=vm.presence_tags(tags_needed,True)
    # issues.download_data(t0,t1,tags_needed)
    start=time.time()
    # df_H2O_debit = cfg.loadtags_period(t0,t1,tags_needed,pool='auto',rs=rs,rsMethod=rsMethod,closed='right',verbose=True)
    # df_H2O_debit['debit H2O'] = df_H2O_debit.sum(axis=1)
    df_H2O_debit = pd.read_pickle('data/issue37_debitH2O.pkl')
    print(time.time()-start)

    l=cfg.dfplc.loc[df_H2O_debit.columns[0]]
    l.name=df_H2O_debit.columns[2]
    l.DESCRIPTION='debit H2O entrant'
    cfg.dfplc.loc[l.name]=l
    cfg.dftagColorCode.loc[l.name]=cfg.dftagColorCode.loc[df_H2O_debit.columns[0]]

    issues.push_toFolderGaston(df_H2O_debit,'issue37_debitH2O',folderCEA,cfg=cfg)
    sys.exit()

###Débit Fuel entrant =Débit H2 neuf + Débit H2O+ Débit de recirculation

tags_needed=['SEH1.L041_H2_FT_01.HM05']
sys.exit()

# p=vm.presence_tags(tags_needed,True)
# issues.download_data(t0,t1,tags_needed)
start=time.time()

#### FU/SU

df = cfg.loadtags_period(t0,t1,tags,rs=rs,rsMethod=rsMethod,closed='right')

# df.to_pickle('df_issue38.pkl')
# print(time.time()-start)
