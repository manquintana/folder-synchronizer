# folder-synchronizer
Python folder synchronizer synchronizes two folders: 'source' and 'replica'. 
It maintains a full, identical copy of source folder at replica folder and the synchronization is performed at your desired interval.

USAGE: 
1. Install the required dependencies (refer to requirements.txt)
2. Run the script:
python3 synchronizer.py -s [source_route] -r [replica_route] -i [interval_in_seconds] -l [logs_route]
3. Need help?
python3 synchronizer.py -h
