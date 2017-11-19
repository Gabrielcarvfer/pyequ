import subprocess
import time
import os
cwd = os.path.dirname(os.path.realpath(__file__))
subprocess.Popen(['python', 'pyequ.py'], cwd=cwd)
subprocess.Popen(['python', 'cef_gui.py'], cwd=cwd)

time.sleep(300)