import os, signal
import sys

os.kill(int(sys.argv[1]), signal.SIGUSR1)
