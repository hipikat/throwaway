# Rename files in the current directory matching [month]-[big|small].jpg
# to files named [target_year]_[month_number]_[top|bottom].jpg

import calendar
from glob import glob
from os import path, rename
import re


target_year = 2014
flat_months = [mnth.lower() for mnth in calendar.month_name]

img_dir = path.dirname(path.abspath(__file__))
imgs = glob(path.join(img_dir, '*.jpg'))
img_parts = [path.split(img) for img in imgs]
for img_dir, from_name in img_parts:
    month_name, size, _ = re.split(r'[-\.]', from_name)
    month_num = flat_months.index(month_name)
    month_pos = 'top' if size == 'big' else 'bottom'
    to_name = '{}_{}_{}.jpg'.format(target_year, month_num, month_pos)
    print('moving {} to {} ...'.format(from_name, to_name))
    rename(path.join(img_dir, from_name), path.join(img_dir, to_name))
