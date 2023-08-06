# Label converter [![Build Status](https://travis-ci.org/finnishnetsolutions/label-converter.svg?branch=master)](https://travis-ci.org/finnishnetsolutions/label-converter)

## Description

**label_converter** is a Python library to turn HTML string to png file for label printing.

## Usage

```
from label_converter import label_converter

header = '<p>I\'m head</p>'
body = '<p>I\'m <strong>label</strong> <span style="font-size: 30px; color: rgb(184, 49, 47);">body</span></p>'
footer = '<p>I\'m footer</p>
width = 600
height = 500
base64_encoding = False

label_converter.create(header, body, footer, width, height, base64_encoding)
```
