import glob
import os
from flowpic2 import FlowPic2
from nfstream import NFStreamer
from datetime import datetime


def get_last_dir_in_path(dir_path):
    '''
    General Purpose
    '''
    return os.path.basename(os.path.normpath(dir_path))

def current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f'[{current_time}]'

print(current_time(), 'Starting...')
for fn in glob.glob(r'flowpic_extracted_flows/*/*.pcap'):
    print(current_time(), 'input', fn)
    output_dirpath = os.path.join(os.path.dirname(fn), 'output')
    print(current_time(), 'output', output_dirpath)
    try:
        os.mkdir(output_dirpath)
    except:
        print(current_time(), 'Directory creation: FAILED!', output_dirpath)
    
    streamer = NFStreamer(source=fn,
                        decode_tunnels=True,
                        bpf_filter=None,
                        promiscuous_mode=True,
                        snapshot_length=1536,
                        idle_timeout=99999999,
                        active_timeout=99999999,
                        accounting_mode=3,
                        udps=[
                        #FlowPic2019('./temp', 0,  flow_active_time=60)
                        FlowPic2(output_dirpath, time_per_subflow=60)
                        #GrayPic1('./temp')
                        ],
                        n_dissections=20,
                        statistical_analysis=True,
                        splt_analysis=0,
                        n_meters=0,
                        performance_report=0)
    list(streamer)