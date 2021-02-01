import numpy as np
import pandas as pd
import os

import xmltodict
from scipy.io import wavfile


class fillers_extractor():
    sample_rate:int

    def __init__(self):
        pass

    @staticmethod
    def read_wav_file(path:str):
        sample_rate, wav_file=wavfile.read(path)
        return sample_rate, wav_file

    @staticmethod
    def read_xml_file(path:str, encoding:str='utf-8'):
        with open(path, encoding=encoding) as fd:
            xml_file = xmltodict.parse(fd.read(), encoding='utf-8')
        return xml_file

    @staticmethod
    def write_wav_file(path:str, wav_file: np.ndarray, sample_rate:int):
        wavfile.write(path, rate=sample_rate, data=wav_file)


class fillers_extractor_BeMaTaC(fillers_extractor):
    wav_file:wavfile
    xml_file:dict

    def __init__(self, path_to_wavfile:str, path_to_xml_file:str):
        super(fillers_extractor, self).__init__()
        self.sample_rate, self.wav_file = self.read_wav_file(path_to_wavfile)
        self.xml_file = self.read_xml_file(path_to_xml_file)

    def extract_event_timings_from_xml_dict(self, xml_dict:dict):
        # extracting timesteps for every event
        event_timings = {}
        tmp_timing = xml_dict['basic-transcription']['basic-body']['common-timeline']['tli']
        for event in tmp_timing:
            event_id = event['@id']
            event_time = float(event['@time'])
            event_timings[event_id] = event_time
        return event_timings

    def extract_utterances(self, xml_dict:dict, wav_file: np.ndarray, event_timings:dict,
                           entities:list=['instructor_df','instructee_df'], list_of_filler_types:list=['f1', 'f2', 'f3', 'ff1'], pad_sec:float=0):
        # tiers, which are annotations of every word, discorse particles, ...
        extracted_utterances = []
        tiers = xml_dict['basic-transcription']['basic-body']['tier']
        for tier in tiers:
            if tier['@category'] in entities and 'event' in tier:
                events = tier['event']
                if not isinstance(events, list):
                    events = [events]
                for event in events:
                    if '#text' in event and event['#text'] in list_of_filler_types:
                        event_start_id = event['@start']
                        event_end_id = event['@end']
                        # calculate start and end indexes to cut wav_file
                        event_start_idx = int(
                            np.round(event_timings[event_start_id] * self.sample_rate - pad_sec * self.sample_rate))
                        event_end_idx = int(
                            np.round(event_timings[event_end_id] * self.sample_rate + pad_sec * self.sample_rate))
                        # cut wav_file
                        # if event_start_id<0 or event_end_id> the length of wav, then pad with zeros
                        if event_start_idx < 0:
                            audio_chunk = wav_file[0:event_end_idx]
                        else:
                            audio_chunk = wav_file[event_start_idx:event_end_idx]
                        overall_length = event_end_idx - event_start_idx
                        if event_start_idx < 0:
                            zero_pad = np.zeros((-event_start_idx, wav_file.shape[1]))
                            audio_chunk = np.concatenate([zero_pad, audio_chunk], axis=0)
                        if event_end_idx > wav_file.shape[0]:
                            zero_pad = np.zeros((event_end_idx - wav_file.shape[0], wav_file.shape[1]))
                            audio_chunk = np.concatenate([audio_chunk, zero_pad], axis=0)
                        assert (audio_chunk.shape[0] == overall_length)
                        extracted_audio = audio_chunk
                        label = event['#text']
                        extracted_utterances.append([extracted_audio, label, event_start_id, event_end_id])
        return extracted_utterances

    def save_utterances_in_dir(self, path_to_dir:str, extracted_utterances:list):
        for extracted_audio, label, event_start_id, event_end_id in extracted_utterances:
            filename = '%s_%s_%s.wav' % (label, event_start_id, event_end_id)
            full_path = os.path.join(path_to_dir, label, filename)
            self.write_wav_file(full_path, extracted_audio, self.sample_rate)
