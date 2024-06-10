import sys

from aidm.environments.gymnasium.spaces_utils import gymnasium_space_val_to_key
from gymnasium import spaces
import numpy as np

box_space = spaces.Box(0, 60, [2, 2, 2, 2])
disc_space = spaces.Discrete(10)
txt_space = spaces.Text(40, min_length=10, charset='abcdefg')
md_space = spaces.MultiDiscrete([2, 4, 6])
mb_space = spaces.MultiBinary(12)

g_space = spaces.Graph(box_space, box_space)
tup_space = spaces.Tuple([box_space, disc_space, txt_space, md_space, mb_space, g_space])
seq_space = spaces.Sequence(txt_space)
seq_stack_space = spaces.Sequence(box_space, stack=True)
dict_space = spaces.Dict(spaces=dict(
    bos=box_space,
    disc=disc_space,
    txt=txt_space,
    md=md_space,
    mb=mb_space,
    graph=g_space
))


def test_space(space: spaces.Space, n_tries=10):
    try:
        for _ in range(n_tries):
            key = gymnasium_space_val_to_key(space.sample(), space)
            try:
                hash(key)
            except:
                print(f'could not hash {space} generated key: {key}')
    except:
        print(f'failed on space type {space}', file=sys.stderr)

    gymnasium_space_val_to_key(space.sample(), space)


test_space(box_space)
test_space(disc_space)
test_space(txt_space)
test_space(md_space)
test_space(mb_space)
test_space(g_space)
test_space(tup_space)
test_space(seq_space)
test_space(seq_stack_space)
test_space(dict_space)

