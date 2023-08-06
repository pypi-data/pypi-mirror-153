import os
from alive_progress import alive_bar
from intentron.utils import (
    get_flatpairs,
    touch,
    copy
)


def split_job(src, dst, cam):
    """
    Split multi-camera dataset to multiple single-camera datasets.
    :param src: source directory
    :param dst: destination directory
    :param cam: camera
    :return: None
    """
    assert cam in ['cam_left', 'cam_center', 'cam_right']
    # touch(dst)
    flatpairs = get_flatpairs(src, dst, cam)
    total = len(flatpairs)
    with alive_bar(total, theme='classic') as bar:
        for source, dest in flatpairs:
            # if 'depth' in source:
            #     bar()
            #     continue
            bar()
            print(source, dest)
            # touch(dest)
            # s = os.path.join(source, 'color')
            # print(source, dest)
            # copy(os.path.join(source, 'info.json'), dest)
            # copy(os.path.join(source, 'color'), dest)
