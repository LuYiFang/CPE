import os
import sys


_BOSS_NORMAL = 'src/static/boss_normal.png'
_BOSS_HIT = 'src/static/boss_hit.png'
_HIT_SPARK = 'src/static/hit_spark.png'
_RECOVER_SHINING = 'src/static/recover_shining.png'
_COUNTDOWN_3 = 'src/static/3.png'
_COUNTDOWN_2 = 'src/static/2.png'
_COUNTDOWN_1 = 'src/static/1.png'
_ATTACK_HINT = 'src/static/attack.png'
_RECOVER_HINT = 'src/static/recover.png'
_YOU_DIE = 'src/static/you_die.png'
_YOU_WIN = 'src/static/you_win.png'


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


BOSS_NORMAL = resource_path(_BOSS_NORMAL)
BOSS_HIT = resource_path(_BOSS_HIT)
HIT_SPARK = resource_path(_HIT_SPARK)
RECOVER_SHINING = resource_path(_RECOVER_SHINING)
COUNTDOWN_3 = resource_path(_COUNTDOWN_3)
COUNTDOWN_2 = resource_path(_COUNTDOWN_2)
COUNTDOWN_1 = resource_path(_COUNTDOWN_1)
ATTACK_HINT = resource_path(_ATTACK_HINT)
RECOVER_HINT = resource_path(_RECOVER_HINT)
YOU_DIE = resource_path(_YOU_DIE)
YOU_WIN = resource_path(_YOU_WIN)
