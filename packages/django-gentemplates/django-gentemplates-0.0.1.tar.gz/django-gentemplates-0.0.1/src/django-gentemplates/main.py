import sys
import os
import shutil
import logging

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.INFO,
    datefmt='%m/%d/%Y %H:%M:%S'
)

logger = logging.getLogger(__name__)


TEMPLATES = [
    '_confirm_delete.html',
    '_create_form.html',
    '_detail.html',
    '_form.html',
    '_list.html',
]


def main():
    app = sys.argv[1]
    name = sys.argv[2]
    destination = f'src/{app}/templates/{app}/'
    sourcedir = 'templates'
    copy_files_to_folder(sourcedir, TEMPLATES, destination, name)
    for file in TEMPLATES:
        replace_text_in_file(f'{destination}{name}{file}', 'object', name)


def copy_files_to_folder(sourcedir, files, destination, prefix):
    for f in files:
        logger.info(f'Copying "{sourcedir}/{f}" to "{destination}{prefix}{f}"')
        shutil.copy(f'{sourcedir}/{f}', f'{destination}{prefix}{f}')


def replace_text_in_file(file, search_txt, replace_txt):
    logger.info(
        f'Searching file for "{search_txt}" and replacing with "{replace_txt}"'
    )
    with open(file, 'r') as f:
        data = f.read()
        data = data.replace(search_txt, replace_txt)

    with open(file, 'w') as f:
        f.write(data)


if __name__ == '__main__':
    main()
