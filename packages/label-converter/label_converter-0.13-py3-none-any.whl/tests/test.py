import io

from label_converter import label_converter


HEADER = """<style>p{font-weight: boldest;}</style><p><strong>
<span style="font-size: 18px;">&nbsp;Linda Svensson</span>
&nbsp;</strong></p>"""
BODY = """<p>Dalhemsvagen 26
<br style="color: rgb(0, 0, 0); font-family: Arial;
font-size: medium; font-style: normal; font-variant-ligatures: normal;
font-variant-caps: normal; font-weight: 400; letter-spacing: normal;
orphans: 2; text-align: start; text-indent: 0px; text-transform: none;
white-space: normal; widows: 2; word-spacing: 0px;
-webkit-text-stroke- text-decoration-thickness: initial;
text-decoration-style: initial; text-decoration-color: initial;">
<br style="color: rgb(0, 0, 0); font-family: Arial; font-size: medium;
font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal;
font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start;
text-indent: 0px; text-transform: none; white-space: normal; widows: 2;
word-spacing: 0px; -webkit-text-stroke- text-decoration-thickness: initial;
text-decoration-style: initial; text-decoration-color: initial;">
141 12 STOCKHOLM</p>"""
FOOTER = """<p>&nbsp;Test</p>"""


def test_create_encode_false_black_false():
    data = label_converter.create(HEADER, BODY, FOOTER, 600, 400,
                                  encode_files=False, force_black=False)
    assert len(data) == 1
    assert isinstance(data[0], io.BytesIO)


def test_create_encode_false_black_true():
    data = label_converter.create(HEADER, BODY, FOOTER, 600, 400,
                                  encode_files=False, force_black=True)
    assert len(data) == 1
    assert isinstance(data[0], io.BytesIO)


def test_create_encode_true_black_false():
    data = label_converter.create(HEADER, BODY, FOOTER, 600, 400,
                                  encode_files=True, force_black=False)
    assert len(data) == 1
    assert isinstance(data[0], bytes)


def test_create_encode_true_black_true():
    data = label_converter.create(HEADER, BODY, FOOTER, 600, 400,
                                  encode_files=True, force_black=True)
    assert len(data) == 1
    assert isinstance(data[0], bytes)
