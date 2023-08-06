__version__ = '1.0.0'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from constants import Camp, Force, N_COLS, N_ROWS
from board import get_iccs_action_space
from env import Env
