import argparse, os, sys
from datetime import datetime
import logging
import shutil






parser = argparse.ArgumentParser()
parser.add_argument('-s', type = str, help = 'Source folder path', required = True)
parser.add_argument('-r', type = str, help = 'Replica folder path', required = True)
parser.add_argument('-i', type = int, help = 'Interval between synchronization [seconds]', required = True)
parser.add_argument('-l', type = str, help = 'Log file path', required = True)
args = parser.parse_args()
source, replica, interval, log = args.s, args.r, args.i, args.l

log_file = f'{log}/log-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
try:
    os.system(f'touch {log_file}')
except Exception as e:
    print(e)



#print(f'Synchronizer input values:\n-Source: {source}\n-Replica: {replica}\n-Interval: {interval}\n-Log: {log}\n\n')

def log_update(type, incident_type, rel_path):
    # Setting up some fancy colors
    incident = { 
        'creation' : '\033[32m',
        'deletion' : '\033[91m',
        'warning' : '\033[33m',
        'end' : '\033[0m'
    }
    print(f'{incident[incident_type]}{type} {incident_type}: {rel_path}{incident["end"]}') # Shows only relative path on terminal
    try:
        logging.basicConfig(filename=log_file, level=logging.INFO)
        logging.info(f' {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} > {type} {incident_type}: {replica}{rel_path}') # but logs the full path
    except Exception as e:
        print(e)
            
        
    
def list_files_dirs(route):
    '''
    Scans the "route" path and returns a list
    with all the directories in the path
    Strategy: From root to leaves.
    '''
    files_list = []
    dirs_list = []
    for root, dirs, files in os.walk(route, topdown=True):
        for name in files:
            files_list.append(os.path.join(root, name).replace(route, '')) # Sanitizing the output while keeping the structure
        for name in dirs:
            dirs_list.append(os.path.join(root, name).replace(route, ''))
    return dirs_list, files_list

def update_dirs(list_source, list_replica):
    '''
    Looks for directories in both directions.
    parameters:
    list_source: List with all the directories in the source path
    list_replica: List with all the directories in the replica path
    '''
    # Remove old unexisting directories from replica
    for dir in list_replica:
        if dir not in list_source:
            try:
                shutil.rmtree(replica+dir)
                log_update('File', 'deletion', dir)
                # print(f'{COLOR_RED}Directory {dir} has been removed.{COLOR_RED_END}')
                # logging.basicConfig(filename=log_file, level=logging.INFO)
                # logging.info(f'Directory {replica}{dir} has been removed.')
            except Exception as e:
                print(e)
    # Create new directories
    for dir in list_source:
        if dir not in list_replica:
            try:
                os.mkdir(replica+dir)
                log_update('Directory', 'creation', dir)
                # print(f'{COLOR_GREEN}Directory {dir} has been created.{COLOR_GREEN_END}')
                # logging.basicConfig(filename=log_file, level=logging.INFO)
                # logging.info(f'Directory {replica}{dir} has been created.')
            except Exception as e:
                print(e)
    
                

def update_files(list_source, list_replica):
    '''
    Looks for files in both directions.
    parameters:
    list_source: List with all the files in the source path
    list_replica: List with all the files in the replica path
    '''   
    # Remove old unexisting files from replica
    for file in list_replica:
        if file not in list_source:
            try:
                os.remove(replica+file)
                log_update('File', 'deletion', file)
                # print(f'{COLOR_RED}File {file} has been removed.{COLOR_RED_END}')
                # logging.basicConfig(filename=log_file, level=logging.INFO)
                # logging.info(f'File {replica}{file} has been removed.')
            except Exception as e:
                print(e)
    
    # Copy new files
    for file in list_source:
        if file not in list_replica:
            try:
                shutil.copy2(source+file, replica+file)
                log_update('File', 'creation', file)
            except Exception as e:
                print(e)


# Get files and dirs list
source_dirs, source_files = list_files_dirs(source)
replica_dirs, replica_files = list_files_dirs(replica)

# print(f'Source dirs: {source_dirs}')
# print(f'Replica dirs: {replica_dirs}')
update_dirs(source_dirs, replica_dirs)

#print(f'Source files: {source_files}')
#print(f'Replica files: {replica_files}')
update_files(source_files, replica_files)


