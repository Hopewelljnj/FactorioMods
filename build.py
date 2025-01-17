import json
import os
import shutil

import pathlib
import zipfile

from utils import update_2ish

FACTORIO_PATH = pathlib.Path(os.getenv('APPDATA')) / 'Factorio' / 'mods'


def build_mod(path, out_path):
    # Folder shenanigans and getting actual name
    name = path.name
    with (path / 'info.json').open('r') as f:
        info = json.load(f)
    version = info['version']
    target_name = f'{name}_{version}'

    build_path = out_path / target_name

    # prepare files for zip
    shutil.copytree(path, build_path, ignore=shutil.ignore_patterns('README.md'), dirs_exist_ok=True)

    # create zip
    zip_name = out_path / f'{target_name}.zip'
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in build_path.rglob('*'):
            if not item.is_file():
                continue
            rel_path = item.relative_to(out_path)
            zipf.write(item, rel_path)

    # remove build dir
    shutil.rmtree(build_path, ignore_errors=True)
    print('Build complete:', zip_name.absolute().as_uri())

    for old_build in FACTORIO_PATH.glob(f'{name}*.zip'):
        old_build.unlink()
    shutil.copyfile(zip_name, FACTORIO_PATH / zip_name.name)


if __name__ == '__main__':
    out_path = pathlib.Path('out')

    # clean out dir
    shutil.rmtree(out_path, ignore_errors=True)
    for mod_path in pathlib.Path.cwd().iterdir():
        if not mod_path.is_dir():
            continue
        if mod_path.name in ('out', 'media') or mod_path.name.startswith(('.', '__')):
            continue
        if mod_path.name == 'factorio-2ish':
            with update_2ish(mod_path):
                build_mod(mod_path, out_path)
        else:
            build_mod(mod_path, out_path)
