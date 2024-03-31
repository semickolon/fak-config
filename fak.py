import hashlib
import re
import os
import sys
import shutil
import subprocess
import argparse

BUILD_DIR = 'build'
FAK_CACHE_DIR = '.fak_cache'
EVAL_NCL_PATH = FAK_CACHE_DIR + '/eval.ncl'


def check(proc):
    if proc.returncode != 0:
        sys.exit(proc.stderr)
        
    return proc.stdout


def sha1():
    return hashlib.sha1()


def compute_hash_ncl(file_path):
    h = sha1()

    with open(file_path, 'r') as f:
        file_contents = f.read()
        import_paths = re.findall(r'import\s+"(.*\.ncl)"', file_contents) 
        
        for import_path in import_paths:
            path = os.path.join(file_path, '..', import_path)
            path = os.path.realpath(path)

            if import_path.startswith('fak/'):
                if os.path.isfile(path):
                    sys.exit('.ncl files in any directory named "fak" are ambiguous and must not exist.')
                else:
                    continue
                
            h.update(compute_hash_ncl(path).encode('utf-8'))
        
        h.update(file_contents.encode('utf-8'))
    
    return h.hexdigest()


def evaluate(keyboard_name, keymap_name):
    path_prefix = f'{FAK_CACHE_DIR}/{keyboard_name}.{keymap_name}'
    sha1_path = path_prefix + '.sha1'
    json_path = path_prefix + '.json'
    
    last_hash = ''
    cur_hash = 'xxxx'

    if os.path.isfile(sha1_path) and os.path.isfile(json_path):
        with open(sha1_path, 'r') as f:
            last_hash = f.read()

    h = sha1()
    h.update(compute_hash_ncl(f'keyboards/{keyboard_name}/keyboard.ncl').encode('utf-8'))
    h.update(compute_hash_ncl(f'keyboards/{keyboard_name}/keymaps/{keymap_name}.ncl').encode('utf-8'))
    cur_hash = h.hexdigest()
    
    if cur_hash == last_hash:
        return open(json_path, 'r')
    
    with open(EVAL_NCL_PATH, 'w') as f:
        f.write(f'(import "fak/main.ncl") (import "keyboard.ncl") (import "keymaps/{keymap_name}.ncl")')
    
    print("Evaluating Nickel files (managed)...")

    evaluation = check(subprocess.run(
        ['nickel', 'export', '-Isubprojects/fak/ncl', f'-Ikeyboards/{keyboard_name}', EVAL_NCL_PATH],
        capture_output=True,
        text=True,
    ))
    
    with open(sha1_path, 'w') as f:
        f.write(cur_hash)

    with open(json_path, 'w') as f:
        f.write(evaluation)

    return open(json_path, 'r')


def update():
    check(subprocess.run(['meson', 'subprojects', 'update'], check=True))


def clean():
    for d in [FAK_CACHE_DIR, BUILD_DIR]:
        if os.path.isdir(d):
            shutil.rmtree(d)


def init():
    os.chdir(sys.path[0])
    os.makedirs(FAK_CACHE_DIR, exist_ok=True)

    if not os.path.isdir(BUILD_DIR):
        check(subprocess.run(['meson', 'setup', BUILD_DIR], check=True))


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        description='valid subcommands', 
        required=True,
        dest='subcmd'
    )

    subcmd_clean = subparsers.add_parser('clean')
    subcmd_compile = subparsers.add_parser('update')
    subcmd_compile = subparsers.add_parser('compile')
    subcmd_flash = subparsers.add_parser('flash', aliases=['flash_c', 'flash_central'])
    subcmd_flash_p = subparsers.add_parser('flash_p', aliases=['flash_peripheral'])

    for subcmd in [subcmd_compile, subcmd_flash, subcmd_flash_p]:
        subcmd.add_argument('-kb', '--keyboard', type=str, required=True)
        subcmd.add_argument('-km', '--keymap', type=str, default='default')

    return parser.parse_args()


args = parse_args()

if args.subcmd == 'clean':
    clean()
elif args.subcmd == 'update':
    init()
    update()
else:
    init()
    fak_py = ['python', 'subprojects/fak/fak.py']

    check(subprocess.run(
        fak_py + ['load_managed_eval'],
        stdin=evaluate(args.keyboard, args.keymap),
    ))
    
    check(subprocess.run(fak_py + [args.subcmd]))

    if args.subcmd == 'compile':
        for side in ['central', 'peripheral']:
            src = f'subprojects/fak/build/{side}.ihx'
            dst = f'.fak_cache/{args.keyboard}.{args.keymap}.{side}.ihx'

            if os.path.isfile(src):
                shutil.copyfile(src, dst)
                print(f'Firmware copied to: {dst}')
