import xmltodict
import numpy as np
import pandas as pd
import os


from scipy.io import wavfile

path_to_xml_files='E:\\Databases\\BeMaTaC\\MapTask_Ger\\l1_exmaralda_2.1'
path_to_wav_files='E:\\Databases\\BeMaTaC\\MapTask_Ger\\l1_wav_2.1'
path_to_save='E:\\Databases\\BeMaTaC\\MapTask_Ger\\extracted_fillers'
if not os.path.exists(path_to_save):
    os.mkdir(path_to_save)
xml_filelist = sorted(os.listdir(path_to_xml_files))
wav_filelist = sorted(os.listdir(path_to_wav_files))

#params
list_of_filler_types=['f1', 'f2', 'f3', 'ff1']
tier_categories=['instructor_df','instructee_df', 'len']

print(xml_filelist)
print(wav_filelist)

for file_idx in range(len(xml_filelist)):
    samplerate, wav_file = wavfile.read(os.path.join(path_to_wav_files,wav_filelist[file_idx]))
    with open(os.path.join(path_to_xml_files, xml_filelist[file_idx]), encoding='utf-8') as fd:
        xml_file = xmltodict.parse(fd.read(), encoding='utf-8')
    # create directory to save fillers in this concrete wav file
    directory_to_save=os.path.join(path_to_save, wav_filelist[file_idx].split('.')[0])
    if not os.path.exists(directory_to_save):
        os.mkdir(directory_to_save)
    # extracting timesteps for every event
    timing={}
    tmp_timing=xml_file['basic-transcription']['basic-body']['common-timeline']['tli']
    for event in tmp_timing:
        event_id=event['@id']
        event_time=event['@time']
        timing[event_id]=event_time

    # tiers, which are annotations of every word, discorse particles, ...
    tiers=xml_file['basic-transcription']['basic-body']['tier']
    for tier in tiers:
        a=1+1
        pass
















with open(os.path.join(path_to_files, xml_filelist[0]), encoding='utf-8') as fd:
    doc = xmltodict.parse(fd.read(), encoding='utf-8' )
print(doc['basic-transcription']['basic-body'])
for key in doc['basic-transcription']['basic-body']['tier']:
    for key_key in key:
        print(key_key)
