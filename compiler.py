import Cython.Build
import distutils.core
import json
import os
import shutil
import re
import datetime


cfg = json.load(open('config.json', 'r', encoding='utf-8'))

    
def get_all_dirs(folder_path):
    dirs = []  # List to store all directories
    for root, _, _ in os.walk(folder_path):
        dirs.append(root)
    return dirs


def py2c(file):
    cpy = Cython.Build.cythonize(file)
    
    distutils.core.setup(
        name=cfg['name'],
        version=cfg['version'],
        author=cfg['author'],
        author_email=cfg['author_email'],
        ext_modules=cpy,
    )
    
    
if __name__ == '__main__':
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    src_dir = './app_to_compile'
    dst_dir = f'./app_saved/{current_time}/app_to_compile'
    shutil.copytree(src_dir, dst_dir)

    for root, dirs, files in os.walk('./app_to_compile'):
        for file in files:
            if file.endswith('.py'):
                source_file = os.path.join(root, file)
                print(f"Compiling {source_file}")
                py2c(source_file)
                
                file_name = file.split('.')[0]
                pattern = fr"^{file_name}\..+\.pyd$"
                
                for item in os.listdir('./'):
                    if re.match(pattern, item):
                        print("Compiled pyd file found")
                        destination_file = source_file.replace('./app_to_compile', './app_compiled')
                        os.makedirs(os.path.dirname(destination_file), exist_ok=True)
                        shutil.move(item, os.path.dirname(destination_file))
                        break
                else:
                    raise Exception(f"No match after compiling {file}")
    
    shutil.rmtree(src_dir)
    shutil.rmtree('./build')
    os.mkdir(src_dir)

