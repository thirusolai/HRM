#!/usr/bin/env python3
"""
Rename occurrences of 'horilla' to 'kangaroo' across the repository.

Rules:
- Replace text in files (skip binary files and virtualenvs/node_modules/.git)
- Rename files and directories containing 'horilla' (case-sensitive and TitleCase)
- Skip .venv and .git
"""
import os
import sys
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SKIP_DIRS = {'.git', '.venv', 'venv', 'node_modules', '__pycache__'}

def is_binary(path):
    try:
        with open(path, 'rb') as f:
            chunk = f.read(8192)
            if b'\0' in chunk:
                return True
    except Exception:
        return True
    return False

def replace_in_file(path):
    if is_binary(path):
        return False
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
    except Exception:
        return False

    new = data.replace('horilla', 'kangaroo')
    new = new.replace('Horilla', 'Kangaroo')
    new = new.replace('HORILLA', 'KANGAROO')

    if new != data:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        return True
    return False

def walk_and_replace():
    changed = []
    for dirpath, dirnames, filenames in os.walk(ROOT, topdown=True):
        # skip directories
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            path = os.path.join(dirpath, name)
            # skip this script
            if os.path.abspath(path) == os.path.abspath(__file__):
                continue
            if replace_in_file(path):
                changed.append(path)
    return changed

def rename_paths():
    # Collect all paths that need renaming, sort by depth (deepest first)
    rename_map = []
    for dirpath, dirnames, filenames in os.walk(ROOT, topdown=False):
        # skip virtualenv and git
        parts = set(dirpath.split(os.sep))
        if parts & SKIP_DIRS:
            continue
        # files
        for name in filenames:
            if 'horilla' in name or 'Horilla' in name:
                src = os.path.join(dirpath, name)
                dst_name = name.replace('horilla', 'kangaroo').replace('Horilla', 'Kangaroo')
                dst = os.path.join(dirpath, dst_name)
                rename_map.append((src, dst))
        # dirs
        for name in dirnames:
            if 'horilla' in name or 'Horilla' in name:
                src = os.path.join(dirpath, name)
                dst_name = name.replace('horilla', 'kangaroo').replace('Horilla', 'Kangaroo')
                dst = os.path.join(dirpath, dst_name)
                rename_map.append((src, dst))

    # perform renames
    for src, dst in sorted(rename_map, key=lambda x: -x[0].count(os.sep)):
        try:
            if os.path.exists(dst):
                # merge by moving contents if src is dir
                if os.path.isdir(src) and os.path.isdir(dst):
                    for item in os.listdir(src):
                        s = os.path.join(src, item)
                        d = os.path.join(dst, item)
                        shutil.move(s, d)
                    shutil.rmtree(src)
                else:
                    # if file exists, overwrite
                    os.remove(dst)
                    shutil.move(src, dst)
            else:
                shutil.move(src, dst)
            print(f"RENAMED: {src} -> {dst}")
        except Exception as e:
            print(f"FAILED to rename {src} -> {dst}: {e}")

def main():
    print('Running replacements...')
    changed = walk_and_replace()
    print(f'Replaced text in {len(changed)} files')
    print('Renaming files and directories...')
    rename_paths()
    print('Done. Please run your tests and adjust configuration files as needed.')

if __name__ == '__main__':
    main()
