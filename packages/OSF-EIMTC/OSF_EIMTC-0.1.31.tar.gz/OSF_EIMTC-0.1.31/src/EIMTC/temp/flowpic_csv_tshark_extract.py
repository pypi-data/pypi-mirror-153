import subprocess
import csv
import glob
import os
from datetime import datetime


def run_tshark(input_filepath, output_filepath, tshark_location, ip1, port1, ip2, port2, protocol, error_log_filepath='./tshark_error_log.txt', ):
    filter = f'{protocol} and ip.addr=={ip1} and {protocol}.port=={port1} and ip.addr=={ip2} and {protocol}.port=={port2}'
    splitted_save = f'-w {output_filepath}'.split()
    command =  f'{tshark_location} -r {input_filepath} -2 -n -R'
    splitted_command = command.split() + [filter] + splitted_save
    print(' '.join(splitted_command))
    with open(output_filepath, "w") as outfile:
        with open(error_log_filepath, "w") as error_log_file:
            proc = subprocess.run(
                splitted_command, 
                stdout = outfile, 
                stderr = error_log_file,
                check=True
            )

def read_flowpic_csv(filepath):
    session_tuple_keys = []
    with open(filepath, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader):
            session_tuple_key = [s.lower() for s in tuple(row[:8])]
            print(i, session_tuple_key)
            session_tuple_keys.append(session_tuple_key)
    return session_tuple_keys
            
def get_last_dir_in_path(dir_path):
    '''
    General Purpose
    '''
    return os.path.basename(os.path.normpath(dir_path))
             
def current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time



## main
filename_mapping = {
    'facebook_video1a': 'nonvpn-streaming-facebook-19.pcap',
    'facebook_video1b': 'nonvpn-streaming-facebook-20.pcap',
    'facebook_video2a': 'nonvpn-streaming-facebook-21.pcap',
    'facebook_video2b': 'nonvpn-streaming-facebook-22.pcap',
    'facebook_audio1a': 'nonvpn-voip-facebook-11.pcap',
    'facebook_audio1b': 'nonvpn-voip-facebook-12.pcap',
    'facebook_audio2a': 'nonvpn-voip-facebook-13.pcap',
    'facebook_audio2b': 'nonvpn-voip-facebook-14.pcap',
    'facebook_audio3':  'nonvpn-voip-facebook-15.pcap',
    'facebook_audio4':  'nonvpn-voip-facebook-16.pcap',
    'hangouts_audio1a': 'nonvpn-voip-hangouts-30.pcap',
    'hangouts_audio1b': 'nonvpn-voip-hangouts-31.pcap',
    'hangouts_audio2a': 'nonvpn-voip-hangouts-32.pcap',
    'hangouts_audio2b': 'nonvpn-voip-hangouts-33.pcap',
    'hangouts_audio3': 'nonvpn-voip-hangouts-34.pcap',
    'hangouts_audio4': 'nonvpn-voip-hangouts-35.pcap',
    'skype_audio1a': 'nonvpn-voip-skype-68.pcap',
    'skype_audio1b': 'nonvpn-voip-skype-69.pcap',
    'skype_audio2a': 'nonvpn-voip-skype-70.pcap',
    'skype_audio2b': 'nonvpn-voip-skype-71.pcap',
    'skype_audio3': 'nonvpn-voip-skype-72.pcap',
    'skype_audio4': 'nonvpn-voip-skype-73.pcap',
    'voipbuster1b': 'nonvpn-voip-voipbuster-96.pcap',
    'voipbuster2b': 'nonvpn-voip-voipbuster-97.pcap',
    'voipbuster3b': 'nonvpn-voip-voipbuster-98.pcap',
    'voipbuster_4a': 'nonvpn-voip-voipbuster-99.pcap',
    'voipbuster_4b': 'nonvpn-voip-voipbuster-100.pcap',
    'vpn_hangouts_audio1': '',
    'vpn_hangouts_audio1': '',
    'vpn_hangouts_audio2': '',
    'vpn_hangouts_audio2': '',
    'vpn_hangouts_audio2': '',
    'vpn_hangouts_audio2': '',
    'vpn_skype_audio1': '',
    'vpn_skype_audio1': '',
    'vpn_skype_audio2': '',
    'vpn_skype_audio2': '',
    'vpn_voipbuster1a': '',
    'vpn_voipbuster1a': '',
    'vpn_voipbuster1b': '',
    'vpn_voipbuster1b': '',
    'facebook_video1a': 'nonvpn-streaming-facebook-19.pcap',
    'facebook_video1b': 'nonvpn-streaming-facebook-20.pcap',
    'facebook_video2a': 'nonvpn-streaming-facebook-21.pcap',
    'facebook_video2b': 'nonvpn-streaming-facebook-22.pcap',
    'hangouts_video1b': 'nonvpn-streaming-hangouts-37.pcap',
    'hangouts_video2a': 'nonvpn-streaming-hangouts-38.pcap', # missing
    'hangouts_video2b': 'nonvpn-streaming-hangouts-39.pcap',
    'netflix1': 'nonvpn-streaming-netflix-44.pcap',
    'netflix2': 'nonvpn-streaming-netflix-45.pcap',
    'netflix3': 'nonvpn-streaming-netflix-46.pcap',
    'netflix4': 'nonvpn-streaming-netflix-47.pcap',
    'skype_video1a': 'nonvpn-streaming-skype-84.pcap', # one skype video is missing
    'skype_video1b': 'nonvpn-streaming-skype-85.pcap',
    'skype_video2a': 'nonvpn-streaming-skype-86.pcap',
    'skype_video2b': 'nonvpn-streaming-skype-87.pcap',
    'vimeo1': 'nonvpn-streaming-vimeo-92.pcap',
    'vimeo3': 'nonvpn-streaming-vimeo-94.pcap',
    'vimeo4': 'nonvpn-streaming-vimeo-95.pcap',
    'youtube5': 'nonvpn-streaming-youtube-135.pcap',
    'youtubeHTML5_1': '', # missing
    'ftps_down_1a': 'nonvpn-filetransfer-ftps-25.pcap',
    'ftps_down_1b': 'nonvpn-filetransfer-ftps-26.pcap',
    'scp1': 'nonvpn-filetransfer-scp- .pcap', # unknown
    'scpUp1': 'nonvpn-filetransfer-scp- .pcap',
    'scpUp2': 'nonvpn-filetransfer-scp- .pcap',
    'sftp_down_3a': 'nonvpn-filetransfer- - .pcap',
    'sftp_down_3b': 'nonvpn-filetransfer- - .pcap',
    'sftp_up_2a': 'nonvpn-filetransfer- - .pcap',
    'sftp_up_2b': 'nonvpn-filetransfer- - .pcap',
    'sftpUp1': 'nonvpn-filetransfer- - .pcap',
    'skype_file2': 'nonvpn-filetransfer-skype-76.pcap',
    'skype_file3': 'nonvpn-filetransfer-skype-77.pcap',
    'skype_file6': 'nonvpn-filetransfer-skype-78.pcap',
    'skype_file7': 'nonvpn-filetransfer-skype-81.pcap',
    'skype_file8': 'nonvpn-filetransfer-skype-82.pcap',


}

extracted_flows = set()

flowpic_csv_dir = r"flowpic_csvs/*.csv"
pcap_dir = r"/mnt/d/temp/University/masters/thesis/research/temp/FlowPic/Ofek's_implementation/data/nonvpn_cleaned"
output_dir = 'flowpic_extracted_flows'


print(current_time(), 'Starting')
for filepath in glob.glob(flowpic_csv_dir):
    output_subdir = os.path.join(output_dir, get_last_dir_in_path(filepath)[:-4])
    try:
        os.mkdir(output_subdir)
        print(current_time(), 'Directory created', output_subdir)
    except:
        print(current_time(), 'FAILED TO CREATE A DIRECTORY', output_subdir)
    keys = read_flowpic_csv(filepath)
    for key in keys:
        if tuple(sorted(key[0:6])) in extracted_flows:
            continue
        
        print(current_time(), 'Extracting with TShark', key)
        
        run_tshark(
            os.path.join(
                pcap_dir, 
                filename_mapping[key[0]]
            ),
            os.path.join(
                output_subdir, 
                '-'.join(key + ['.pcap'])
            ),
            'tshark',
            key[1],
            key[2],
            key[3],
            key[4],
            key[5]
        )
        
        extracted_flows.add(tuple(sorted(key[0:6])))
        