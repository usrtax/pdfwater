#!/usr/bin/env python

import csv
from pikepdf import Pdf, Page, Rectangle
from pathlib import Path
from reportlab.lib import units
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from os.path import dirname, join
from datetime import datetime
from config import *

OUT = join('out',str(datetime.today())[:10])
result = Path(OUT)
result.mkdir(exist_ok=True,parents=True)

PWD  = dirname(__file__)

def 加水印(name, file):
  target = Pdf.open(join(PWD,'input.pdf'))  # 必须每次重新打开PDF，因为添加水印是inplace的操作
  water_mark_pdf = Pdf.open(str(file))
  water_mark = water_mark_pdf.pages[0]

  for page in target.pages:
    for x in range(水印列数):  # 每一行显示多少列水印
      for y in range(水印行数): # 每一页显示多少行PDF
        page.add_overlay(water_mark,
                         Rectangle(page.trimbox[2] * x / 水印列数,
                                   page.trimbox[3] * y / 水印行数,
                                   page.trimbox[2] * (x + 1) / 水印列数,
                                   page.trimbox[3] * (y + 1) / 水印行数))

    result_name = Path(OUT, 文件名前缀+f'{name}.pdf')
    target.save(str(result_name))


with open('user.csv',encoding = 'utf-8-sig') as f:
  reader = csv.DictReader(f)
  li = [x['name'] for x in reader]

FONT = 'AliHYAiHei'

pdfmetrics.registerFont(TTFont(FONT, join(PWD,FONT+'.ttf'))) # 加载中文字体

for name in li:
  path = PWD / Path(f'tmp.pdf')
  c = canvas.Canvas(str(path), pagesize=(水印视图边长 * units.mm, 水印视图边长 * units.mm)) # 生成画布，长宽都是水印视图边长毫米
  padding = 0.1
  c.translate(padding * 水印视图边长 * units.mm, (1-padding) * 水印视图边长 * units.mm)
  c.rotate(315)  # 把水印文字旋转315°
  c.setFont(FONT, 35)  # 字体大小
  c.setStrokeColorRGB(0, 0, 0)  # 设置字体颜色
  c.setFillColorRGB(0, 0, 0)  # 设置填充颜色
  c.setFillAlpha(0.1)  # 设置透明度，越小越透明
  c.drawString(0, 0, f'{name}{水印后缀}')
  c.save()
  加水印(name,path)
  path.unlink()
  print(name)
