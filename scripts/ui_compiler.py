import os
import subprocess

UI_DIR = os.path.abspath('./ui')
COMPILED_DIR = os.path.abspath('./compiled')

if not os.path.exists(COMPILED_DIR):
    os.makedirs(COMPILED_DIR)

for root, dirs, files in os.walk(UI_DIR):
    for file in files:
        if file.endswith('.ui'):
            ui_path = os.path.join(root, file)
            rel_dir = os.path.relpath(root, UI_DIR)
            target_dir = os.path.join(COMPILED_DIR, rel_dir)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            py_file = os.path.splitext(file)[0] + '.py'
            py_path = os.path.join(target_dir, py_file)
            cmd = ['pyuic6', ui_path, '-o', py_path]
            print(f"Compiling {ui_path} -> {py_path}")
            subprocess.run(cmd, check=True)