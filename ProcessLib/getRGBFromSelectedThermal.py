import os
import shutil

selected_thermal_folder = "/media/hkuit164/Backup/thermal/20230206_sunny_thermal_keepPerson"  # 指定红外图像的文件路径
rgb_folder = "/media/hkuit164/Backup/rgb/20230206_sunny_rgb"  # 指定RGB图像的文件路径
selected_rgb_folder = "/media/hkuit164/Backup/thermal/selected_rgb"
os.makedirs(selected_rgb_folder,exist_ok=True)

# 获取红外文件夹中指定的文件名列表
thermal_filenames = os.listdir(selected_thermal_folder)

# 遍历红外文件夹中的图片
for filename in thermal_filenames:
    # 构建红外文件的完整路径
    thermal_filepath = os.path.join(selected_thermal_folder, filename)

    # 构建对应的RGB文件的完整路径
    rgb_filename = filename.replace("thermal", "rgb")  # 取消扩展名并添加".jpg"扩展名
    rgb_filepath = os.path.join(rgb_folder, rgb_filename)

    # 判断RGB文件是否存在
    if os.path.exists(rgb_filepath):
        # 将RGB文件复制到新的目标文件夹中
        shutil.copy(rgb_filepath, selected_rgb_folder)
