import logging
import os
import shutil
from io import BytesIO, StringIO, TextIOBase

from PIL import Image, ImageDraw

logger = logging.getLogger(__name__)


# FIXME: Text size
# TODO: Caching?
# TODO: Image size choises: Icon, ...
# TODO: Width and height units (cm, mm, em, px, pt, pc, in, ...) default: px
# TODO: Background color


def _create_bitmap(name, width, height, filetype, text):
    """
    Create bitmap image.

    Returns:
        BytesIO:
    """
    file = BytesIO()
    file.name = name + '.' + filetype
    image = Image.new('RGBA', size=(width, height), color=(128, 128, 128))
    draw = ImageDraw.Draw(image)
    size = draw.textsize(text)
    draw.text(((width - size[0]) / 2, (height - size[1]) / 2), text)
    image.save(file, format=filetype)
    file.seek(0)
    return file


def _create_svg(name, width, height, text):
    """
    Create svg image.

    Returns:
        StringIO:
    """
    import svgwrite
    file = StringIO()
    file.name = name + '.svg'
    center = (width / 2, height / 2)
    image = svgwrite.Drawing(file.name, profile='tiny', height=height,
                             width=width)
    image.add(image.rect(insert=(0, 0), size=(width, height)))
    # TODO: Test if text fits inside rectangle
    image.add(image.text(text, insert=center))
    image.write(file)
    file.seek(0)
    return file


def _save_image(image, filedir):
    """
    Save in memory image to a file.

    Args:
        image (io.IOBase):
            In memory image.

        filedir (str):
            Path to the directory where `image` should be saved

    Raises:
        TypeError: If `image` is not correct type.
        FileExistsError: If file with name `image.name` exists in `filedir`.
    """
    if isinstance(image, TextIOBase):
        # Write as text file
        mode = 'wt'
    else:
        # Write as binary file
        mode = 'wb'

    filepath = os.path.join(filedir, image.name)
    if os.path.exists(filepath):
        raise FileExistsError(
            'File with name "{name}" already exists in path "{filepath}".'
            ''.format(name=image.name, filepath=filepath)
        )
    with open(filepath, mode) as file:
        shutil.copyfileobj(image, file)


def create_image(name='untitled', width=48, height=48, filetype='png',
                 text=None, savedir=None):
    """
    Creates in memory images for testing.

    Args:
        name (str):
            Name without file extension.

        width (int):
            Positive integer

        height (int):
            Positive integer

        filetype (str):
            Bitmap {'jpeg', 'png', 'gif'}. Vector graphics {'svg'}

        text (str, optional):
            None uses default "{width}x{height}" string. Otherwise supplied
            string is used if string is empty no text is set.

        savedir (str, optional):
            Directory for saving created image. Default value is None which
            doesn't save the image.

    Returns:
        BytesIO|StringIO:
            Image as BytesIO or StringIO object. It can be used in same fashion
            as file object created by opening a file.

    Resources:
    .. [#] http://wildfish.com/blog/2014/02/27/generating-in-memory-image-for-
           tests-python/
    .. [#] https://pillow.readthedocs.io/en/latest/
    .. [#] https://svgwrite.readthedocs.io/en/latest/overview.html
    """
    logging.info("")

    if text is None:
        text = "{width}x{height}".format(width=width, height=height)

    if filetype == 'svg':
        try:
            image = _create_svg(name, width, height, text)
        except ImportError as error:
            raise Exception(
                'You need to install svgwrite to create vector graphics.'
                '{msg}'.format(msg=error)
            )
    else:
        image = _create_bitmap(name, width, height, filetype, text)

    if savedir is not None:
        _save_image(image, savedir)

    return image