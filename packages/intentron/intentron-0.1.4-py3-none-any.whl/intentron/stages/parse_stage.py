import csv
import json
import cv2
import mediapipe as mp
from alive_progress import alive_bar
from glob import glob
from intentron.utils import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mph = mp.solutions.holistic


def parse_stage(src, dst):
    if osp.exists(dst):
        log.info("Parsing is done")
    else:
        touch(dst)
        log.info("Parsing started")
        bones = [str(it) for it in mph.POSE_CONNECTIONS]
        files = [it for it in glob(f'{src}/**/*.png', recursive=True) + glob(f'{src}/**/*.jpg', recursive=True) + glob(f'{src}/**/*.jpeg', recursive=True) if 'depth' not in it]
        n_files = len(files)

        with open(osp.join(dst, 'bones.txt'), 'w') as out:
            out.write('\n'.join(bones))

        holistic = mph.Holistic(
            static_image_mode=False,
            model_complexity=2,
            smooth_landmarks=True,
            enable_segmentation=True,
            smooth_segmentation=True,
            refine_face_landmarks=False
        )

        with alive_bar(n_files, theme='classic', title='Parsing') as bar:
            for src_folder, _, src_files in sorted(os.walk(src)):
                if 'depth' not in src_folder:
                    joints = []
                    dst_folder = src_folder.replace(src, dst)
                    info_file = os.path.join(src_folder, 'info.json')
                    touch(dst_folder)

                    if os.path.exists(info_file):
                        label = '_'.join(osp.basename(dst_folder).split('_')[0:-1])
                        info_file = os.path.join(src_folder, 'info.json')
                        new_info_file = os.path.join(dst_folder, 'info.json')
                        if os.path.exists(info_file):
                            with open(info_file, 'r') as inp:
                                info = json.loads(inp.read())
                                is_valid = info['label']['is_valid_performance']
                                new_info = {
                                    'label': label,
                                    'is_valid': is_valid
                                }
                                with open(new_info_file, 'w') as out:
                                    out.write(json.dumps(new_info, indent=4, sort_keys=True))

                    if dst_folder.endswith('color'):
                        dst_folder = dst_folder.replace('/color', '')
                    for src_file in sorted(src_files):
                        if src_file.endswith('.png') or src_file.endswith('.jpg') or src_file.endswith('.jpeg'):
                            bar()
                            inp_path = os.path.join(src_folder, src_file)
                            image = cv2.imread(inp_path)
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                            height, width, _ = image.shape
                            result = holistic.process(image)

                            joint = []

                            if result.pose_landmarks:
                                for it in mph.PoseLandmark:
                                    lp = result.pose_landmarks.landmark[it]
                                    if lp:
                                        joint += [lp.x, lp.y, lp.z]
                                    else:
                                        joint += [None, None, None]
                            else:
                                joint += [None] * 33

                            if result.pose_world_landmarks:
                                for it in mph.PoseLandmark:
                                    pw = result.pose_world_landmarks.landmark[it]
                                    if pw:
                                        joint += [pw.x, pw.y, pw.z]
                                    else:
                                        joint += [None, None, None]
                            else:
                                joint += [None] * 33

                            if result.left_hand_landmarks:
                                for it in mph.HandLandmark:
                                    lh = result.left_hand_landmarks.landmark[it]
                                    if lh:
                                        joint += [lh.x, lh.y, lh.z]
                                    else:
                                        joint += [None, None, None]
                            else:
                                joint += [None] * 21

                            if result.right_hand_landmarks:
                                for it in mph.HandLandmark:
                                    rh = result.right_hand_landmarks.landmark[it]
                                    if rh:
                                        joint += [rh.x, rh.y, rh.z]
                                    else:
                                        joint += [None, None, None]
                            else:
                                joint += [None] * 21

                            joints += [joint]

                    if joints:
                        head = []
                        for it in mph.PoseLandmark:
                            head += [f'pose__{it.name.lower()}__x']
                            head += [f'pose__{it.name.lower()}__y']
                            head += [f'pose__{it.name.lower()}__z']
                        for it in mph.PoseLandmark:
                            head += [f'world_pose__{it.name.lower()}__x']
                            head += [f'world_pose__{it.name.lower()}__y']
                            head += [f'world_pose__{it.name.lower()}__z']
                        for it in mph.HandLandmark:
                            head += [f'left_hand__{it.name.lower()}__x']
                            head += [f'left_hand__{it.name.lower()}__y']
                            head += [f'left_hand__{it.name.lower()}__z']
                        for it in mph.HandLandmark:
                            head += [f'right_hand__{it.name.lower()}__x']
                            head += [f'right_hand__{it.name.lower()}__y']
                            head += [f'right_hand__{it.name.lower()}__z']

                        joints_file = os.path.join(dst_folder, 'joints.csv')
                        with open(joints_file, 'w', encoding='UTF8') as out:
                            writer = csv.writer(out)
                            writer.writerow(head)
                            for joint in joints:
                                writer.writerow(joint)

                        labels_file = os.path.join(dst, 'joints.txt')
                        with open(labels_file, 'w', encoding='UTF8') as out:
                            out.write('\n'.join(head))
