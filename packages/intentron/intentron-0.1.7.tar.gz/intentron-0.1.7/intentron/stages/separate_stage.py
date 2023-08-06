from alive_progress import alive_bar
from intentron.utils import *


def separate_stage(src, dst, cam):
    """
    Split multi-camera dataset to multiple single-camera datasets.
    :param src: source directory
    :param dst: destination directory
    :param cam: camera
    :return: None
    """

    if osp.exists(dst):
        log.info("Separating is done")
    else:
        log.info("Separating started")
        touch(dst)

    folders = []
    for gesture in os.listdir(src):
        for side in os.listdir(osp.join(src, gesture)):
            for trial in os.listdir(osp.join(src, gesture, side)):
                folders += [osp.join(src, gesture, side, trial)]
    n = len(folders)

    with alive_bar(n, theme='classic', title='Loading') as bar:
        for gesture in os.listdir(src):
            # touch(osp.join(dst, gesture))
            for side in os.listdir(osp.join(src, gesture)):
                # touch(osp.join(dst, gesture, side))
                for trial in os.listdir(osp.join(src, gesture, side)):
                    bar()
                    touch(osp.join(dst, gesture, side, trial))
                    info_src_file = osp.join(src, gesture, side, trial, 'info.json')
                    info_dst_file = osp.join(dst, gesture, side, trial, 'info.json')
                    src_folder = osp.join(src, gesture, side, trial, cam)
                    dst_folder = osp.join(dst, gesture, side, trial)
                    copy(info_src_file, info_dst_file)
                    copy(src_folder, dst_folder)
