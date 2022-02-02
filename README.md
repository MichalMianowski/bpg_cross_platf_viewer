# bpg_cross_platf_viewer created by Michal Mianowski
Cross platform image viewer with bpg handling

This is image viewer using imageIO to load and save images also supporting BPG format.
It contains plugin to imageIO extend supporting BPG format - files bpg.py and bpg_load_save_lib.so bpg_load_save_lib.dll

GUI is created in PyQt5 so can be run on multiple systems (tested Windows 10 and Ubuntu 20.04.3 LTS with standard gnome GUI)

to run image viewer you must run main.py script

Dependencies:
python - preferred version 3.8
pip and install requirements from requirements.txt
command: python -m pip install -r requirements.txt
