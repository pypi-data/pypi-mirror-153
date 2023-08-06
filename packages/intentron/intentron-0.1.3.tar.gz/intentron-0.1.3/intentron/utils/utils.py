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


def rmdir(folder: str):
    if os.path.exists(folder):
        shutil.rmtree(folder)


def copy(src, dst):
    if os.path.isfile(src):
        shutil.copy(src, dst)
    else:
        for root, _, files in os.walk(src):
            for f in files:
                path = os.path.join(root, f)
                if os.path.isfile(path):
                    shutil.copy(path, dst)


def touch(folder: str):
    # shutil.rmtree(path, ignore_errors=True)
    os.makedirs(folder, exist_ok=True)


def flatten(item) -> list:
    if not isinstance(item, list): return item
    return reduce(lambda x, y: x + [y] if not isinstance(y, list) else x + [*flatten(y)], item, [])


def get_subfolders(folder):
    output = []
    for inp_folder, _, inp_files in sorted(os.walk(folder)):
        output += [inp_folder]
    return output


def get_files(folder, ext):
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
                if ext == 'all':
                    outputs += [osp.join(root, file)]
                else:
                    if file.endswith(ext):
                        outputs += [osp.join(root, file)]
    return outputs


def enum_files(folder, exts):
    outputs = []
    for i, (csv_file, json_file) in enumerate(get_files(folder, ['json', 'csv'])):
        outputs += [(i, csv_file, json_file)]
    return outputs


def get_lines(folder):
    return max([len(open(file).readlines()) for file in get_files(folder, 'csv')])


def padded(df, n):
    return df.reindex(range(n)).fillna(0, downcast='infer')
