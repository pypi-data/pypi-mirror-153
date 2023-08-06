The find_overlap.py script will return any B#/Routing Case overlaps that may exist.
To use the script, you can either:
- provide it with the name of the file(s) that contains the ANBSP printouts from which you want 
  to check for overlaps.
- or provide it with the name of a file that contains ANBSI or ANBSP commands (from the LERG). 
  The first step is to look for ANBSI commands, and if found, convert them to their ANBSP equvalents in a temporary file called defs_to_query.txt.
  If there are no ANBSI commands, it will look for ANBSP commands and save them in defs_to_query.txt instead.
  It will then query the MSC(s) using the commands from defs_to_query.txt and generate a temporary file containing the ANBSP printouts. 
  After checking for overlaps in that temporary file, it will attemp to move the tempory files to the tmp folder.

The script's overlap detection logic is based on a single rule, as per my current understanding... 
Let me know if there are any special cases that need to be incorporated.

Edit the config.txt configuration file by entering your username and password for your OSSUMTS 
and ENM access (for the MSCs).


Prerequisite:
1) Install the latest version of python 3 from https://www.python.org/ if you don't already have it.
During the python installation, make sure that the option to add the location of the python executable to your Windows PATH environment variable is selected.

2) Install the paramiko package by doing the following:
a) Right click on Windows PowerShell (or CMD prompt) and select Run as Administrator. (If Run as Administrator does not work, try using the regular mode.)
b) Type the following 2 commands: 
python -m pip install –upgrade pip
python -m pip install –upgrade paramiko


To run the scrpit, type on the command line:
usage: python -m find_overlap [-h] [-f FILENAME | -l LOCAL [LOCAL ...]] [-t] [-p] [-c CONFIG]

Finds potentional overlaps in LERG B-number definitions

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        name of file to process. defaults to input.txt if not
                        specified.
  -l LOCAL [LOCAL ...], --local LOCAL [LOCAL ...]
                        find overlaps in provided file(s) without contacting
                        MSC(s).
  -t, --timeout         sets command execution to non-blocking. default is
                        blocking
  -p, --print_output    flag to print command output to the screen. default is
                        not to print
  -c CONFIG, --config CONFIG
                        name of configuration file. defaults to config.txt if
                        not specified.


Let me know if you have any questions: issa.lompo@rci.rogers.com