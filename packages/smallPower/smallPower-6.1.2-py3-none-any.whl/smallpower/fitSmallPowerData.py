import sys,re,importlib,pandas as pd, numpy as np, time, datetime as dt
sys.path.append("/home/dorian/pythonDorianLibs/")
import configFiles
import smallPowerDash
import utilsD
import plotly.express as px
import matplotlib.colors as mtpcl
from pylab import cm
from dateutil import parser
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

importlib.reload(smallPowerDash)
importlib.reload(configFiles)
importlib.reload(utilsD)

folderData = '/home/dorian/data/sylfenData/smallPower_pkl/pkl_formatted/'
confFile    = "/home/dorian/sylfen/exploreSmallPower/PLC_confg/SmallPower-10002-001-ConfigurationPLC_v2.csv"
cfg = configFiles.ConfigFiles(folderData,confFile,'latin-1')
spd=smallPowerDash.SmallPowerDash(cfg)
utils = utilsD.Utils()

ll=utils.listWithNbs(cfg.listFilesPkl)
res = {}
dfFit=cfg.prepareDFforFit(7,ts=['18:02','19:59'],rs='3s')
res=cfg.fitDataframe(dfFit,func='expDown',plotYes=True)
# dfFit=cfg.prepareDFforFit(14,ts=['11:27','11:55'],rs='10s')
# res['t1']=cfg.fitDataframe(dfFit,func='poly2',plotYes=False)
# dfFit=cfg.prepareDFforFit(14,ts=['16:35','17:30'],rs='30s')
# res['t2']=cfg.fitDataframe(dfFit,func='poly2',plotYes=True)
