#!/usr/bin/env python
#
#	Run this script with ipython for interactive testing:
#   $ ipython -i test_interactive_local_acomms.py
#
#   When run this way, the interpreter runs the python code below then
#   drops you into an interactive shell to test say, um.send_single_shot_sst()

#   !! You must have your $PYTHONPATH set correctly so it has the path for 
#   !! the local pyacomms directory (e.g., /home/user/pyacomms) run:
#   $ export PYTHONPATH:/home/user/pyacomms:$PYTHONPATH

#   I recommend running in a virtual env to make sure you're not using the pip package

from acomms import micromodem, unifiedlog
import logging

unified_log = unifiedlog.UnifiedLog(log_path='./', console_log_level=logging.INFO)

um = micromodem.Micromodem(name='Micromodem2',unified_log=unified_log)

print('\n---')
print('Not currently connected to a micromodem!')
print('To connect:...... um.connect_serial(\'/dev/ttyUSB0\', 19200)')
print('To disconnect:... um.disconnect()')
print('\n---')
