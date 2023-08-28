import os
import random
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='RtspDataCollection')
    parser.add_argument('--InputFolder', "-i",
                        help="Inuput image's folder",
                        required=True,
                        type=str)
    parser.add_argument('--Output_1', '-o1',
                        help="train.txt",
                        default=False,
                        type=str)
    parser.add_argument('--Output_2', '-o2',
                        help="val.txt",
                        default=False,
                        type=str)
    parser.add_argument('--Ratio', '-r',
                        help="smaller than 1",
                        default=False,
                        type=float)
    args = parser.parse_args()
    return args

args = parse_args()
folder_path = args.InputFolder
output_file_1 = args.Output_1
output_file_2 = args.Output_2
split_ratio = args.Ratio

file_names = os.listdir(folder_path)
image_names = [file_name for file_name in file_names if file_name.endswith((".jpg", ".jpeg", ".png"))]
random.shuffle(image_names)

split_point = int(len(image_names) * split_ratio)

with open(output_file_1, "w") as file1, open(output_file_2, "w") as file2:
    for i, image_name in enumerate(image_names):
        if i < split_point:
            file1.write("data/yolo/" + os.path.basename(folder_path) + "/" + image_name + "\n")
        else:
            file2.write("data/yolo/" + os.path.basename(folder_path) + "/" + image_name + "\n")
