import os
import os.path as osp
from intentron.utils import *
from . import *


def pipeline_stage(src, dst):
    """
    Pipeline.
    :param src: source directory
    :param dst: destination directory
    :return: None
    """
    src = osp.abspath(src)
    dst = osp.abspath(dst) if dst else f'{src}-pipeline'
    print(src, dst)

    if osp.exists(dst):
        log.info("Resuming the pipeline")
    else:
        log.info("Initializing the pipeline")
        touch(dst)

    for folder in sorted(os.listdir(src)):
        load_stage(osp.join(src, folder), osp.join(dst, f'01.{src}-loaded'))
        parse_stage(osp.join(dst, f'01.{src}-loaded'), osp.join(dst, f'02.{src}-parsed'))
        fuse_stage(osp.join(dst, f'02.{src}-parsed'), osp.join(dst, f'03.{src}-fused'))
