#!/usr/bin/env python3.13
import os

from Assets.data                 import totalGameStatus as s
from Game.core.system.dataLoader import makePath


s.s = '/'

s.TFP = str(os.path.abspath(''))+s.s

s.path['data'] = {k:makePath(*p)for k,p in s.path['data'].items()}
s.path['info'] = {k:makePath(*p)for k,p in s.path['info'].items()}

os.system("clear")

import Game.main