import os
import os.path as osp
import shutil
from functools import reduce


# def get_flatpairs(src, dst, cam=''):
#     outputs = []
#     src = src.rstrip(os.path.sep)
#     assert os.path.isdir(src)
#     for root, dirs, files in sorted(os.walk(src)):
#         new_root = root.replace(f'/{cam}', '').replace(f'{src}/', '').replace('/', '_').replace('(', '').replace(')', '').replace(' ', '_')
#         num_seps = root.count(os.path.sep)
#         output = os.path.join(dst, new_root)
#         if num_seps == 5:
#             outputs += [(root, output)]
#     return outputs

def get_flatpairs(src, dst):
    outputs = []
    src = src.rstrip(os.path.sep)
    assert os.path.isdir(src)
    for root, dirs, files in sorted(os.walk(src)):
        new_root = root.replace(src + '/', '').replace('/', '_').replace('(', '').replace(')', '').replace(' ', '_')
        num_seps = root.count(os.path.sep)
        output = os.path.join(dst, new_root)
        if num_seps == 4:
            outputs += [(root, output)]
    return outputs


def rm(folder: str):
    if os.path.exists(folder):
        shutil.rmtree(folder)


def copy(src, dst):
    if os.path.isfile(src):
        shutil.copy(src, dst)
    else:
        for src_folder, _, files in os.walk(src):
            dst_folder = src_folder.replace(src, dst)
            touch(dst_folder)
            for f in files:
                file = os.path.join(src_folder, f)
                shutil.copy(file, dst_folder)


def move(src, dst):
    if os.path.isfile(src):
        shutil.move(src, dst)
    else:
        for src_folder, _, files in os.walk(src):
            dst_folder = src_folder.replace(src, dst)
            touch(dst_folder)
            for f in files:
                file = os.path.join(src_folder, f)
                shutil.move(file, dst_folder)


def touch(folder: str):
    # shutil.rmtree(path, ignore_errors=True)
    os.makedirs(folder, exist_ok=True)


def flatten(item) -> list:
    if not isinstance(item, list): return item
    return reduce(lambda x, y: x + [y] if not isinstance(y, list) else x + [*flatten(y)], item, [])


def get_subfolders(folder):
    output = []
    for root, _, inp_files in sorted(os.walk(folder)):
        output += [root]
    return output


def get_files(folder, ext=None):
    outputs = []
    if type(ext) is list:
        for root, folder, files in sorted(os.walk(folder)):
            output = []
            for file in sorted(files):
                for e in ext:
                    if file.endswith(e):
                        output += [osp.join(root, file)]
            if output:
                outputs += [output]
    else:
        for root, folder, files in sorted(os.walk(folder)):
            for file in sorted(files):
                if ext == None:
                    outputs += [osp.join(root, file)]
                else:
                    if file.endswith(ext):
                        outputs += [osp.join(root, file)]
    return outputs


def enum_files(folder, exts):
    outputs = []
    for i, (csv_file, json_file) in enumerate(get_files(folder, exts)):
        outputs += [(i, csv_file, json_file)]
    return outputs


def get_lines(folder):
    return max([len(open(file).readlines()) for file in get_files(folder, 'csv')])


def padded(df, n):
    return df.reindex(range(n)).fillna(0, downcast='infer')
