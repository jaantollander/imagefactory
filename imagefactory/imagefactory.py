from io import BytesIO, StringIO
from PIL import Image, ImageDraw
import logging

try:
    import svgwrite
    SVG_SUPPORT = True
except ImportError:
    SVG_SUPPORT = False


logger = logging.getLogger(__name__)


def _create_bitmap(name, width, height, filetype, text):
    """
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
    Returns:
        StringIO:
    """
    file = StringIO()
    file.name = name + '.svg'
    center = (width / 2, height / 2)
    image = svgwrite.Drawing(file.name, profile='tiny',
                             height=height, width=width)
    image.add(image.rect(insert=(0, 0), size=(width, height)))
    image.add(image.text(text, insert=center))
    image.write(file)
    file.seek(0)
    return file


def create_image(name, width=48, height=48, filetype='png', text=None):
    """
    Creates in memory images for testing.

    Args:
        name (str): Name without file extension.
        width (int): Positive integer
        height (int): Positive integer
        filetype (str): Bitmap {'jpg', 'jpeg', 'png', 'gif'}
                        Vector graphics {'svg'}
        text (str, optional): None uses default "{width}x{height}" string.
                    Otherwise supplied string is used if string is empty
                    no text is set.

    Returns:
        BytesIO|StringIO: Image as BytesIO or StringIO object.
            It can be used in same fashion as file object
            >>> file = open("image.ext", 'rb')
            created by opening a file.

    Resources:
    .. [#] http://wildfish.com/blog/2014/02/27/generating-in-memory-image-for-tests-python/
    .. [#] https://pillow.readthedocs.io/en/latest/
    .. [#] https://svgwrite.readthedocs.io/en/latest/overview.html
    """
    # FIXME: Text size
    # TODO: Width and height units (cm, em, px, ...)
    logging.info("")

    if text is None:
        text = "{width}x{height}".format(width=width, height=height)

    if filetype.lower() == 'svg':
        return _create_svg(name, width, height, text)
    else:
        return _create_bitmap(name, width, height, filetype, text)
