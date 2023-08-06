from intentron.utils import *
from . import *


def pipeline_stage(src, dst):
    """
    Pipeline.
    :param src: source directory
    :param dst: destination directory
    :return: None
    """
    dst = dst if dst else f'{src}-pipeline'

    if osp.exists(dst):
        log.info("Resuming the pipeline")
    else:
        log.info("Initializing the pipeline")
        touch(dst)

    for folder in sorted(os.listdir(src)):
        load_stage(osp.join(src, folder), osp.join(dst, f'01.{folder}-loaded'))
        parse_stage(osp.join(dst, f'01.{folder}-loaded'), osp.join(dst, f'02.{folder}-parsed'))
        fuse_stage(osp.join(dst, f'02.{folder}-parsed'), osp.join(dst, f'03.{folder}-fused'))
    gather_stage(dst, osp.join(dst, f'04.{osp.basename(dst)}-gathered'))
