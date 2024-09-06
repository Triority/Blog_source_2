import os

# 设置您的文件夹路径
folder_path = '/hexo/source/photo/media/'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 检查文件名是否以 _ 开头并且扩展名为 .jpg
    if filename.startswith('_') and filename.lower().endswith('.jpg'):
        # 创建新的文件名，即删除开头的 _
        new_filename = filename[1:]
        # 重命名文件
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
        print(f'Renamed {filename} to {new_filename}')
print('Completed')
