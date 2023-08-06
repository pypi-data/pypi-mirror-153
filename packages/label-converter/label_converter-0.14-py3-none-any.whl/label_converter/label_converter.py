import imgkit
import numpy as np
from PIL import Image
import re
import io
import base64
from lxml import etree
import xml.etree.ElementTree as ET


def is_empty(value):
    if value:
        if isinstance(value, str):
            return len(value.strip()) == 0
    return True


def get_border_height(value):
    if is_empty(value):
        return "0"
    return "2px"


def create(head, body, footer, width, height, encode_files=False,
           force_black=True, zoom=1):
    # Add UTF-8 tag and line below head text
    head = '<meta charset="UTF-8"/><div style="height: {height}px; width: ' \
           '{width}px; position: relative;">{head}<div style="display: block; ' \
           'width: {width}px; height: {border};background: grey;"></div>'.format(
        height=height - 16,
        width=width-15, head=head,
        border=get_border_height(head)
    )
    # Add line above footer text
    footer = '<div style="display: block; width: {width}px; height: {border};background: grey;">' \
             '</div>{footer}'.format(
        width=width-15,
        footer=footer,
        border=get_border_height(footer)
    )
    # Create actual footer. This just creates normal invisble footer and actual
    #  footer is put to the bottom with absolute. Otherwise body could overlap
    #  with footer and checking image size doesn't notice that
    footer = '<div style="visibility: hidden;">{footer}</div></div><div '\
             'style="position: absolute; bottom: 0;">{footer}</div>'.format(
                 footer=footer)
    lines = get_lines(body)
    return generate_images(head, lines, footer, width, height,
                           encode_files=encode_files, force_black=force_black,
                           zoom=zoom)


def get_lines(html):
    # Cut body to lines/list using <p> tags. This is needded, because it's not
    #  possible to cut text with imgkit
    lines = []
    line_count = len(re.findall(r'<\/p>', html))
    for i in range(0, line_count):
        match = re.search(r'<\/p>', html)
        lines.append(html[:match.end()])
        html = html[match.end():]
    return lines


def estimate_size(html, options):
    image = io.BytesIO(imgkit.from_string(html, False, options=options))
    im = Image.open(image)
    return im.size


def estimate_header_size(html, options):
    tree = etree.fromstring(html, etree.HTMLParser())
    p_tag = tree.findall('.//p')
    if len(p_tag) > 0 and p_tag[0].find('..') is not None:
        p_tag[0].find('..').attrib.clear()
        p_tags_str = ET.tostring(p_tag[0].find('..')).decode()
        return estimate_size(p_tags_str, options)
    else:
        return (0, 0)


def generate_images(head, lines, footer, width, height, encode_files,
                    force_black, zoom):
    max_height = height
    max_width = width
    skips = 0
    img_count = 0
    images = []
    # Generate as many images as necessary
    for _ in range(100):
        n = 0
        html = head

        options = {'width': max_width, 'encoding': 'UTF-8', 'format': 'png',
                   'quiet': '', 'quality': 90}

        header_size = estimate_header_size(head, options)
        footer_size = estimate_size(footer, options)

        for line in range(0, len(lines) - skips):
            html = '{html}{line}'.format(html=html, line=lines[line])
            html = update_svg_size(html, max_width, max_height, header_size, footer_size)
            n += 1
        html = '{html}{footer}'.format(html=html, footer=footer)

        image = io.BytesIO(imgkit.from_string(html, False, options=options))
        im = Image.open(image)
        width, height = im.size

        # Check height
        if height > max_height:
            skips += 1
            # Generate the image, cannot do nothing to fix fitting issue
            # Generate the image, don't skip the rest when the height exceeds the max height
            if height > max_height:
                skips += 1
                # Generate the image, cannot do nothing to fix fitting issue
                if len(lines) - skips <= 0:
                    images.append(generate_image(html, max_width, max_height,
                                                 encode_files, force_black, zoom))
                    return images
        else:
            # Generate the image in correct size
            images.append(generate_image(html, max_width, max_height,
                                         encode_files, force_black, zoom))
            # Uncomment to save 1 image to current folder
            # imgkit.from_string(html, 'put.png', options=options)
            # Check if all lines are included
            if skips == 0:
                break
            else:
                # Reset counters and remove already used text
                skips = 0
                img_count += 1
                for line in range(0, n):
                    del lines[0]
                n = 0

    return images


def update_svg_size(html, max_width, max_height, header_size, footer_size):
    tree = etree.fromstring(html, etree.HTMLParser())
    p_tag = tree.find('.//p')
    svgs = tree.findall('.//svg')

    def abs_size(size):
        return 10 if size <= 0 else size

    if svgs:
        for svg in svgs:
            min_max_width_height = min(
                abs_size(max_width), abs_size(max_height-footer_size[1]-header_size[1])
            )
            width_height = min_max_width_height
            svg.attrib['width'] = str(width_height)
            svg.attrib['height'] = str(width_height)
        return ET.tostring(tree).decode()
    return html


def generate_image(html, max_width, max_height, encode_files,
                   force_black=True, zoom=1):
    options = {'width': max_width * zoom, 'height': max_height * zoom,
               'quiet': '', 'zoom': zoom, 'quality': 90,
               'encoding': 'UTF-8', 'format': 'png'}
    image = imgkit.from_string(html, False, options=options)
    image = io.BytesIO(image)
    if force_black:
        new_image = force_black_and_white(image)
        image = io.BytesIO()
        new_image.save(image, "PNG")
    # Encode actual image in base64
    if encode_files:
        image = base64.b64encode(image.getvalue())
    return image


def force_black_and_white(image):
    image = Image.open(image)
    data = np.asarray(image)
    new_data = np.where(data > 200, 255, 0)
    new_image = Image.fromarray(new_data.astype(np.uint8))
    return new_image
