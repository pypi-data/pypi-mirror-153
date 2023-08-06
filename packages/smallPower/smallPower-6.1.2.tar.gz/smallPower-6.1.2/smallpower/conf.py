import os,glob,pandas as pd, pickle,sys
from dorianUtils.utilsD import Utils
from dorianUtils.comUtils import FileSystem
import time

__fs=FileSystem()

def load_material_dfConstants():
    dfConstants = pd.read_excel(FILECONF_SMALLPOWER,sheet_name='physical_constants',index_col=1)
    cst = {}
    for k in dfConstants.index:
        # setattr(cst,k,dfConstants.loc[k].value)
        cst[k]=dfConstants.loc[k].value
    return cst,dfConstants

def __loadcolorPalettes():
    colPalettes = Utils().colorPalettes
    colPalettes['reds']     = colPalettes['reds'].drop(['Misty rose',])
    colPalettes['greens']   = colPalettes['greens'].drop(['Honeydew',])
    colPalettes['blues']    = colPalettes['blues'].drop(['Blue (Munsell)','Powder Blue','Duck Blue','Teal blue'])
    colPalettes['magentas'] = colPalettes['magentas'].drop(['Pale Purple','English Violet'])
    colPalettes['cyans']    = colPalettes['cyans'].drop(['Azure (web)',])
    colPalettes['yellows']  = colPalettes['yellows'].drop(['Light Yellow',])
    ### manual add colors
    colPalettes['blues'].loc['Indigo']='#4B0082'
    #### shuffle them so that colors attribution is random
    for c in colPalettes.keys():
        colPalettes[c]=colPalettes[c].sample(frac=1)
    return colPalettes

def _buildColorCode(colorPalettes,dfplc,unitDefaultColors):
    dftagColorCode = pd.read_excel(FILECONF_SMALLPOWER,sheet_name='tags_color_code',index_col=0,keep_default_na=False)
    from plotly.validators.scatter.marker import SymbolValidator
    raw_symbols = pd.Series(SymbolValidator().values[2::3])
    listLines = pd.Series(["solid", "dot", "dash", "longdash", "dashdot", "longdashdot"])
    allHEXColors=pd.concat([k['hex'] for k in colorPalettes.values()])
    ### remove dupplicates index (same colors having different names)
    allHEXColors=allHEXColors[~allHEXColors.index.duplicated()]

    dfplc
    alltags = list(dfplc.index)
    dfplc.UNITE=dfplc.UNITE.fillna('u.a.')
    def assignRandomColor2Tag(tag):
        unitTag  = dfplc.loc[tag,'UNITE'].strip()
        shadeTag = unitDefaultColors.loc[unitTag].squeeze()
        color = colorPalettes[shadeTag]['hex'].sample(n=1)
        return color.index[0]

    # generate random color/symbol/line for tags who are not in color_codeTags
    listTags_wo_color=[k for k in alltags if k not in list(dftagColorCode.index)]
    d = {tag:assignRandomColor2Tag(tag) for tag in listTags_wo_color}
    dfRandomColorsTag = pd.DataFrame.from_dict(d,orient='index',columns=['colorName'])
    dfRandomColorsTag['symbol'] = pd.DataFrame(raw_symbols.sample(n=len(dfRandomColorsTag),replace=True)).set_index(dfRandomColorsTag.index)
    dfRandomColorsTag['line'] = pd.DataFrame(listLines.sample(n=len(dfRandomColorsTag),replace=True)).set_index(dfRandomColorsTag.index)
    # concatenate permanent color_coded tags with color-random-assinged tags
    dftagColorCode = pd.concat([dfRandomColorsTag,dftagColorCode],axis=0)
    # assign HEX color to colorname
    dftagColorCode['colorHEX'] = dftagColorCode.apply(lambda x: allHEXColors.loc[x['colorName']],axis=1)
    dftagColorCode['color_appearance']=''
    return dftagColorCode

def _load_enum_hubmodes():
    enumModeHUB = pd.read_excel(FILE_PLC_XLSM,sheet_name='Enumérations',skiprows=1).iloc[:,1:3].dropna()
    enumModeHUB=enumModeHUB.set_index(enumModeHUB.columns[0]).iloc[:,0]
    enumModeHUB.index=[int(k) for k in enumModeHUB.index]
    for k in range(100):
        if k not in enumModeHUB.index:
            enumModeHUB.loc[k]='undefined'
    enumModeHUB = enumModeHUB.sort_index()
    enumModeHUB = enumModeHUB.to_dict()
    return enumModeHUB

def get_tags_allpowers(dfplc):
    return {
        'power_stk_her':['SEH1.STB_STK_00_HER_00_JTW_00_HC01'],
        'power_enceinte':['SEH1.STB_HER_00_JTW_00_HC01'],
        'power_gv1a':__fs.getTagsTU('STG_01a.*JTW',dfplc),
        'power_gv1b':__fs.getTagsTU('STG_01b.*JTW',dfplc),
        'alim_stacks':__fs.getTagsTU('STK_ALIM.*JTW',dfplc),
        'power_pumps':__fs.getTagsTU('PMP.*JTW',dfplc),
        'power_blowers':__fs.getTagsTU('BLR.*JTW',dfplc),
    }

def get_tags_gv_rendement(gv,dfplc):
    tags={}
    power_gv = __fs.getTagsTU('stg.*'+gv+'.*JTW',dfplc)
    for k,tag in enumerate(power_gv):
        tags['power_gv_'+gv+'_'+str(k+1)] = tag
    tags['ft_in_gv_'+gv] = __fs.getTagsTU('l213.*'+gv+'.*FT',dfplc)[0]
    tags['tt_in_gv'] = __fs.getTagsTU('GWPBH_TT',dfplc)[0]
    tags['tt_out_gv'] = __fs.getTagsTU('L036.*TT',dfplc)[0]
    return tags

def get_tags_for_indicators(dfplc):
    tags_for_indicators={
        'vanneBF'     : 'l300.*ECV',
        'air_in_ft'   : 'l138.*FT',
        'air_out_ft'  : 'l118.*FT',
        'air_out_pt'  : 'GFD_02.*PT',
        'air_in_tt'   : 'HTBA.*HEX_02.*TT.*01',
        'air_stack_tt': 'GFC_02.*TT',
        'air_balayage_tt' : 'HPB.*HEX_02.*TT.*02',
        'n2_in_air'       : 'l301.*FT',
        'fuel_in_ft'      : 'l041.*FT.*HM05',
        'h2_in_ft'        : 'l041.*FT.*HM05',
        'fuel_out_ft'     : 'l025.*FT.*HM05',
        'fuel_out_pt'     : 'GFD_01.*PT',
        'fuel_in_tt'      : 'HTBF.*HEX_01.*TT.*01',
        'fuel_stack_tt'   : 'GFC_01.*TT',
        'n2_in_fuel'      : 'l303.*FT.*HM05',
        # 'water_in_ft' : 'l213.*FT.*HM05',
        'power_total' :'SEH0.JT_01.JTW_HC20',
        'T_stacks'    :'SEH1.STB_TT_02.HM05',
        # 'L032' : 'l032.*FT',#NO
        # 'L303' : 'l303.*FT',#NO
        # 'L025' : 'l025.*FT',#NF
        'h2_cold_loop_ft'   : 'l032.*FT',
        'power_chauffant_1' : 'STK_HER.*01.*JTW',
        'power_chauffant_2' : 'STK_HER.*02.*JTW',
        'power_chauffant_3' : 'STK_HER.*03.*JTW',
        }
    tags_for_indicators={k:__fs.getTagsTU(v,dfplc)[0] for k,v in tags_for_indicators.items()}
    ### complete dictionnaries for stack currents
    for k in range(1,5):
        basetag='SEH1.STK_ALIM_0'+str(k)+'.IT'
        tag_hm05,tag_hr29 = basetag+'_HM05',basetag+'_HR29'
        tags_for_indicators['current_stack_measure'+ str(k)] = tag_hm05
        tags_for_indicators['current_stack_command'+ str(k)] = tag_hr29
    ### complete dictionnaries for rendement_gv tags
    tags_gv = pd.concat([pd.Series(get_tags_gv_rendement(k,dfplc)) for k in ['a','b']]).drop_duplicates()
    tags_for_indicators = pd.concat([pd.Series(tags_for_indicators),tags_gv]).sort_index()
    return tags_for_indicators

def generate_conf_small_power():
    print('generating configuration files and store in :'+_FILECONF_SMALLPOWER_PKL)
    start=time.time()
    f = open(_FILECONF_SMALLPOWER_PKL,'wb')
    beckhoff_plc = pd.read_excel(FILE_PLC_XLSM,sheet_name='FichierConf_Jules',index_col=0)
    beckhoff_plc = beckhoff_plc[beckhoff_plc.DATASCIENTISM]

    pickle.dump(beckhoff_plc,f)

    palettes = __loadcolorPalettes()
    pickle.dump(palettes,f)

    cst,dfConstants = load_material_dfConstants()

    pickle.dump(dfConstants,f)

    pickle.dump(cst,f)

    enum_modes = _load_enum_hubmodes()
    pickle.dump(enum_modes,f)

    unitDefaultColors = pd.read_excel(FILECONF_SMALLPOWER,sheet_name='units_colorCode',index_col=0)
    pickle.dump(unitDefaultColors,f)

    plc_indicator_tags = pd.read_excel(FILECONF_SMALLPOWER,sheet_name='indicator_tags',index_col=0)
    pickle.dump(plc_indicator_tags,f)

    dftagColorCode = _buildColorCode(palettes,pd.concat([beckhoff_plc,plc_indicator_tags]),unitDefaultColors)
    pickle.dump(dftagColorCode,f)

    useful_tags = pd.read_excel(FILECONF_SMALLPOWER,sheet_name='useful_tags',index_col=0)
    pickle.dump(useful_tags,f)

    tags_for_indicators = get_tags_for_indicators(beckhoff_plc)
    pickle.dump(tags_for_indicators,f)
    f.close()
    print('configuration files all generated in  : '+ str(time.time()-start)+' seconds.')
    return [beckhoff_plc,palettes,dfConstants,cst,enum_modes,
            unitDefaultColors,plc_indicator_tags,dftagColorCode,
            useful_tags,tags_for_indicators]

# ====================
# PARAMETERS SETTINGS
# ====================
FOLDERUSER=os.getenv('HOME')+'/smallpower_user'
_DEFAULT_PARAMETERS_FILE=os.path.dirname(__file__) + '/parameters_conf.default.py'
PARAMETERS_FILE=FOLDERUSER + '/parameters_conf.py'
if not os.path.exists(PARAMETERS_FILE):
    if not os.path.exists(FOLDERUSER):os.mkdir(FOLDERUSER)
    ### copy the default parameters file as the parameters File into the user folder
    os.popen('cp ' + _DEFAULT_PARAMETERS_FILE + ' ' + PARAMETERS_FILE)

### create symbolic link of parameters file into conf folder
os.popen('ln -f -s ' + PARAMETERS_FILE + ' ' + _DEFAULT_PARAMETERS_FILE.replace('default.',''))
from .parameters_conf import *
#
ALL = {k:eval(k) for k in ['PARKING_TIME','DB_PARAMETERS','DB_TABLE','TZ_RECORD','SIMULATOR','FOLDERPKL']}
_appdir     = os.path.dirname(os.path.realpath(__file__))
CONFFOLDER = _appdir + '/confFiles/'
FILECONF_SMALLPOWER = CONFFOLDER + 'smallpower_configfiles.ods'
_FILECONF_SMALLPOWER_PKL = CONFFOLDER + 'smallpower_conf.pkl'
FILE_PLC_XLSM = glob.glob(CONFFOLDER+'*ALPHA*.xlsm')[0]
LOG_FOLDER=os.path.dirname(_appdir)+'/logs/'


if os.path.exists(_FILECONF_SMALLPOWER_PKL):
    _smallpower_objs= Utils().loads_pickle(_FILECONF_SMALLPOWER_PKL)
else:
    _smallpower_objs=generate_conf_small_power()

[BECKHOFF_PLC,PALETTES,DFCONSTANTS,CONSTANTS,ENUM_MODES_HUB,
    UNITDEFAULTCOLORS,PLC_INDICATOR_TAGS,DFTAGCOLORCODE,
    USEFUL_TAGS,TAGS_FOR_INDICATORS] = _smallpower_objs


FREQ_INDICATOR_TAGS = 1
