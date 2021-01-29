import xmltodict
import numpy as np
import pandas as pd
import os
import wave

path_to_xml_files='C:\\Users\\Dresvyanskiy\\Desktop\\BeMaTaC\\MapTask_Ger\\l1_exmaralda_2.1'
path_to_wav_files='C:\\Users\\Dresvyanskiy\\Desktop\\BeMaTaC\\MapTask_Ger\\l1_wav_2.1'
path_to_save='C:\\Users\\Dresvyanskiy\\Desktop\\BeMaTaC\\MapTask_Ger\\extracted_fillers'
if not os.path.exists(path_to_save):
    os.mkdir(path_to_save)
xml_filelist = sorted(os.listdir(path_to_xml_files))
wav_filelist = sorted(os.listdir(path_to_wav_files))

#params
list_of_filler_types=['f1', 'f2', 'f3', 'ff1']

print(xml_filelist)
print(wav_filelist)

for file_idx in range(len(xml_filelist)):
    wav_file=wave.open(os.path.join(path_to_wav_files,wav_filelist[file_idx]))
    with open(os.path.join(path_to_xml_files, xml_filelist[0]), encoding='utf-8') as fd:
        xml_file = xmltodict.parse(fd.read(), encoding='utf-8')
    # create directory to save fillers in this concrete wav file
    directory_to_save=os.path.join(path_to_save, wav_file.split('.')[0])
    if not os.path.exists(directory_to_save):
        os.mkdir(directory_to_save)
















with open(os.path.join(path_to_files, xml_filelist[0]), encoding='utf-8') as fd:
    doc = xmltodict.parse(fd.read(), encoding='utf-8' )
print(doc['basic-transcription']['basic-body'])
for key in doc['basic-transcription']['basic-body']['tier']:
    for key_key in key:
        print(key_key)
