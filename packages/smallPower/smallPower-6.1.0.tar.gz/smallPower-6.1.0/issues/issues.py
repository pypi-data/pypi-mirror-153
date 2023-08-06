import importlib,time,sys,os
start=time.time()
import pandas as pd,numpy as np
import smallpower.smallPower as smallPower
from smallpower import conf
from dorianUtils.comUtils import html_table
from dorianUtils.utilsD import Utils
import subprocess as sp,os
import plotly.express as px


folder_figures='/home/dorian/sylfen/programmerBible/doc/pictur/'
cfg = smallPower.SmallPowerComputer()

def download_data(t0,t1,tags):
    listDays=[cfg.streamer.to_folderday(k)[:-1] for k in pd.date_range(t0,t1,freq='D')]
    for d in listDays:
        for t in tags:
            filename='data_ext/smallPower_daily/'+d+t+'.pkl'
            folder_final=cfg.folderPkl+d[:-1]
            if not os.path.exists(folder_final):os.mkdir(folder_final)
            # print(filename,folder_final)
            sp.run('scp sylfenGaston:'+filename + ' ' + folder_final,shell=True)

def replot_colors(fig):
    colors=Utils().colors_mostdistincs
    for k,trace in enumerate(fig.data):
        trace.marker.color=colors[k]
        trace.marker.symbol='circle'
        trace.line.color=colors[k]
        trace.line.dash='solid'
    return fig

def show_file_from_gaston(filename='df_issue38.pkl',dl=True):
    folder_data=os.dirname(__file__)+'/data/'
    fullpath=folder_data+filename
    if dl:sp.run('scp sylfenGaston:tests/'+filename+ ' ' + fullpath,shell=True)
    df=pd.read_pickle(fullpath)
    fig = cfg.multiUnitGraphSP(df.astype(float))
    fig = cfg.update_lineshape_fig(fig)
    fig.show()

def push_toFolderGaston(df,filename,folderGaston,private=True,fig_generate=True,cfg=None):
    if cfg is None :cfg=cfg
    df.to_pickle('data/'+filename+'.pkl')
    df.to_csv('data/'+filename+'.csv')
    if fig_generate:
        fig=cfg.multiUnitGraphSP(df.resample('1H',closed='right',label='right').mean());
        # fig=cfg.multiUnitGraphSP(df.resample('1H').nearest());
        fig=replot_colors(fig)
        a4_size=[210,297]
        std_screenSize=[1920,1080]
        a_ratioA4=a4_size[0]/a4_size[1]
        h=1080/2 ### it should take half the page of an A4 on a std 19/9 screen display
        w=h*a_ratioA4
        more=4
        h,w=h*more,w*more ## increase the size to improve resolution of picture when downsizing it on A4.
        fig.write_html(folder_figures +filename +'.html')
        fig.update_layout(font_size=12*more/1.5)
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.04,
            xanchor="left",
            x=0.01
        ))
        fig.write_image(folder_figures +filename +'.png',height=h,width=w)

    if private:
        host='sylfenGaston'
    else:
        host='sylfenGastonFibre'

    sp.run('scp data/' + filename + '* ' + host +':'+folderGaston,shell=True)

class VersionsManager():
    def __init__(self,folderpkl):
        self.folderpkl=folderpkl

    def presence_tags(self,tags,show_res=True,recompute=True):
        listDays=os.listdir(self.folderpkl)
        df=pd.DataFrame()
        for t in tags:
            df[t] = [True if t+'.pkl' in os.listdir(self.folderpkl+d) else False for d in listDays]
        df.index=listDays
        df=df.sort_index()
        if show_res:
            html_table(df)
            px.line(df).show()
        return df
