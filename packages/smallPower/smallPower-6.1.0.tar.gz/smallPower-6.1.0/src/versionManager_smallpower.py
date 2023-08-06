# ==============================================================================
#                           UPDATE HISTORICAL DATA
import os,sys,glob,pickle,re,importlib,datetime as dt
import subprocess as sp, pandas as pd,numpy as np,time, pickle
import dorianUtils.comUtils as comutils
import dorianUtils.utilsD as ut
importlib.reload(comutils)
importlib.reload(ut)
import smallPowerDash.smallPower as smallPower
importlib.reload(smallPower)
# for k in range(50):print()
utils=ut.Utils()

svm = smallPower.SmallPower_VM()
svm = smallPower.SmallPower_VM(buildFiles=[False,True,True])
# svm = smallPower.SmallPower_VM(buildFiles=[True,False,False])
# svm = smallPower.SmallPower_VM()
# svm.remove_notds_tags(patPeriod='**')
# sys.exit()

# def makeItCompatible_to_2.42():
# t0,t1 = [svm.tmin,svm.tmax]
t0,t1 = [pd.Timestamp('2022-01-30',tz='CET'),pd.Timestamp('2022-02-01',tz='CET')]
for transition in svm.transitions:
# for transition in svm.transitions[0:0]:
    print('transition:',transition)
    patternsMap   = svm.getCorrectVersionCorrespondanceSheet(transition)
    map_renametag = svm.get_renametagmap_transition_v2(transition)
    # print(map_renametag)
    replacedmap = svm.make_it_compatible_with_renameMap(map_renametag,period=[t0,t1])

svm.create_emptytags_version([t0,t1],svm.df_plcs['2.42'])
svm = smallPower.SmallPower_VM(buildFiles=[False,True,True])
svm.show_map_of_compatibility(False,zmax=150);

mapc=svm.map_missingTags.T
mapc.loc['2021-11-01','2.42']
svm.get_renametagmap_transition_v2('2.30_2.31')
# df = svm.get_patterntags_inPLCs('SIS.TT')
# svm.get_patterntags_inPLCs('TT_00_HC20')
sys.exit()
# ==============================================================================
#                           TESTS
def test_get_functions_minutely():
    folderminute  = svm.folderData+'2021-12-15/15/00/'
    brand_newtags = map_renametag.loc[map_renametag['oldtag'].isna(),'newtag']
    dfcreate      = svm.get_createnewtag_folderminute(folderminute,list(brand_newtags))
    map_pressenceTags=svm.get_presenceTags_folder(folderminute)
    map_missingTags=svm.get_missing_tags_versions(folderminute)

def test_loading_functions_daily():
    folderday  = svm.folderData+'2022-01-22/'
    ###### list tags in a folder
    # svm.get_listTags_folder(folderday)
    # svm.get_lentags(folderday)
    ###### in all tags history get a list of those present in the folder
    svm.get_presenceTags_folder(folderday)
    ###### for all tags history get the list of missing tags of a folder for all versions
    svm.get_missing_tags_versions(folderday)
    ###### in all tags history get a map of missing tags for all versions for all folders
    svm.load_missingTags_versions(pool=False)
    #### get a map of tags/period for the presence of tags having the pattern
    svm.get_patterntags_folders(['2021-12-26','2022-01-02'],'F004')

    #### create a tag as empty dataframe in a folder
    # svm.get_createnewtag_folder(svm.folderData+'2021-12-31/',['C00000017-F004-kW L3-JTW'])
    #### replace a list of old tags by a list of new tags in a folder
    # tag2replace = map_renametag.set_index('oldtag').loc[['C00000016-GENERAL_ADMINISTRATIF-23-kWh-JTWH']].reset_index()
    # svm.get_replace_tags_folder(svm.folderData+'2021-12-31/',tag2replace)

def test_show_functions():
    svm.show_nbFolder()
    svm.show_map_of_compatibility(True)
    svm.show_map_of_compatibility(False)
    tags=list(pd.Series(svm.all_tags_history).sample(n=20))
    svm.show_map_presenceTags(tags)
