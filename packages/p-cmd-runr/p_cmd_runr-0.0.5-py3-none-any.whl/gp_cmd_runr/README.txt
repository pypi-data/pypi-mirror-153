
*** NO RESPONSIBILITY OR LIABILITY DISCLAIMER ***
IN NO EVENT SHALL THE AUTHOR BE LIABLE TO YOU OR ANY THIRD PARTIES FOR ANY SPECIAL, 
PUNITIVE, INCIDENTAL, INDIRECT OR CONSEQUENTIAL DAMAGES OF ANY KIND, 
OR ANY DAMAGES WHATSOEVER, INCLUDING, WITHOUT LIMITATION, 
THOSE RESULTING FROM LOSS OF USE, LOST DATA OR PROFITS, OR ANY LIABILITY, 
ARISING OUT OF OR IN CONNECTION WITH THE USE OF THIS SCRIPT.

The gp_cmd_runr.py script is a general purpose and flexible means of automatically 
running commands remotely on one or more service node(s) using SSH(/AMOS/MOSHELL).
It is able to jump to any number of SSH accessible nodes, with the option of running commands on each node.)
PLEASE MAKE SURE THAT YOU MANUALLY TEST THE COMMANDS ON THE INTENDED NODE(S) BEFORE RUNNING THEM 
AUTOMATICALLY WITH THIS SCRIPT.


The script is controlled by one or more configuration files. See Definitions.txt and/or the example configurations to 
have an idea on how to write your own.


Prerequisite:
1) Install the latest version of python 3 from https://www.python.org/ if you don't already have it.
During the python installation, make sure that the option to add the location of the python executable to your Windows PATH environment variable is selected.

2) Install the paramiko package by doing the following: (this should not be needed, as installing the p_cmd_runr package will install required dependencies.)
a) Right click on Windows PowerShell (or CMD prompt) and select Run as Administrator. (If Run as Administrator does not work, try using the regular mode.)
b) Type the following 2 commands: 
python -m pip install –upgrade pip
python -m pip install –upgrade paramiko



To install the package:
python -m pip install p_cmd_runr


To run the scrpit, type on the command line:
python -m gp_cmd_runr [-h] [-d] [-t] [-p] [-r|-n|-f] [-c CONFIG1 [CONFIG2 ...] ]

general purpose command runner

optional arguments:
  -h, --help            show this help message and exit
  -d, --dry_run         display loaded configuration, but do not execute
  -t, --timeout         sets command execution to non-blocking. default is blocking
  -p, --print_output    flag to print command output to the screen. default is not to print
  -r, --raw		no manipulation of output file(s)
  -n, --normal		remove duplicate '\n' between lines in output file(s). this normal appearance is the default behavior
  -f, --flatten		only have output file(s) containing a single '\n' between lines
  -c CONFIG1 [CONFIG2 ...], --config CONFIG1 [CONFIG2 ...]
                        list of one or many configuration files. default is config.txt



Limitations/Knon Issues:

Pagination type commands like 'more' or 'less' will lock after the first output. It is best to avoid such commands.
You may try to run gp_cmd_runr.py with the -t or --timeout option. This will force the script to send the next command after the delay you specify, which may result in unexpected behavior on the remote node.



Let me know if you have any questions: kaiyoux@gmail.com
