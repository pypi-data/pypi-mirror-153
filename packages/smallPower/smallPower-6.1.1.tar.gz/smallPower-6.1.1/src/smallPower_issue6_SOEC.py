from smallpower.smallPower import SmallPowerComputer
import subprocess as sp
import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
# sp.run('scp sylfenGastonFibre:tests/df_courant.pkl .',shell=True)

class Issue6(SmallPowerComputer):
    def __init__(self,*args):
        SmallPowerComputer.__init__(self,*args)
def new_hover(fig):
    # name = 'name  : <b>%{marker.size:}</b><br><br>'
    x    = 'date  :  %{x|%d/%b/%Y %H:%M}<br>'
    y    = 'value :  %{y:.2f}<br>'
    fig.update_traces(hovertemplate=x+y)


new_tag_name = 'sumCourants'
cfg=SmallPowerComputer()
cfg.dftagColorCode.loc[new_tag_name]=['red','circle','solid','#0c677a','']
vals=cfg.dfplc.loc['SEH0.EPB_SYS_65A1_IT_01.HM05']
vals['DESCRIPTION']='somme des courants'
cfg.dfplc.loc[new_tag_name]=vals

# cfg.dfplc.loc[new_tag_name]=

df=pd.read_pickle('df_courant.pkl')
df1=df.sum(axis=1).resample('600s').ffill()
df1.columns=[new_tag_name]
df2=pd.DataFrame()
df2['courant SOEC']=df1.apply(lambda x:max(x,0)).abs()
df2['courant SOFC']=df1.apply(lambda x:min(x,0)).abs()

# df=df1.fillna(0)
# df1=df1.to_frame()
# fig=cfg.multiUnitGraphSP(df1.resample('3600s').ffill())
fig=px.scatter(df2)
fig.update_traces(mode='lines+markers',line_shape='hv')
new_hover(fig)
fig.show()
