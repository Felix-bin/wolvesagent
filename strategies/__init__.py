# -*- coding: utf-8 -*-
"""策略模块"""

from .base_strategy import BaseStrategy
from .werewolf_strategy import WerewolfStrategy
from .seer_strategy import SeerStrategy
from .witch_strategy import WitchStrategy
from .hunter_strategy import HunterStrategy
from .villager_strategy import VillagerStrategy

__all__ = [
    'BaseStrategy',
    'WerewolfStrategy',
    'SeerStrategy',
    'WitchStrategy',
    'HunterStrategy',
    'VillagerStrategy'
]