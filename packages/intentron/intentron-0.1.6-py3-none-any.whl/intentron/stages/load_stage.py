from alive_progress import alive_bar
from intentron.utils import *


def load_stage(src, dst):
    if osp.exists(dst):
        log.info("Loading is done")
    else:
        log.info("Loading started")
        touch(dst)
        flatpairs = get_flatpairs(src, dst)
        total = len(flatpairs)
        with alive_bar(total, theme='classic', title='Loading') as bar:
            for s, d in flatpairs:
                bar()
                touch(d)
                copy(os.path.join(s, 'info.json'), d)
                copy(os.path.join(s, 'color'), d)
