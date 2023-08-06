import pathlib

from .image_comparator import ImageComparator


def is_image(file_path):
    IMAGE_EXTENTIONS = {'.bmp', '.png', '.jpg', '.ps', '.eps', '.cps', '.tif', '.tiff'}
    return file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENTIONS


def list_image_files(left_topdir, right_topdir, subdir=pathlib.Path('.')):
    if left_topdir.is_dir():
        leftdir = left_topdir/subdir
        if right_topdir.is_dir():
            rightdir = right_topdir/subdir

            dirs = set()
            images = set()

            if leftdir.is_dir():
                leftdir_paths = list(leftdir.glob('[!.]*'))
                dirs |= set(map(lambda p: p.relative_to(left_topdir), filter(pathlib.Path.is_dir, leftdir_paths)))
                images |= set(map(lambda p: p.name, filter(is_image, leftdir_paths)))

            if rightdir.is_dir():
                rightdir_paths = list(rightdir.glob('[!.]*'))
                dirs |= set(map(lambda p: p.relative_to(right_topdir), filter(pathlib.Path.is_dir, rightdir_paths)))
                images |= set(map(lambda p: p.name, filter(is_image, rightdir_paths)))

            for image in sorted(images):
                yield str(subdir/image), ImageComparator(leftdir/image, rightdir/image)

            for d in sorted(dirs):
                for item in list_image_files(left_topdir, right_topdir, d):
                    yield item
