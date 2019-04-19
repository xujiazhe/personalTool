# -*- coding: utf-8 -*-
#
# Created by xujiazhe on 2019-04-10.
#
#  在图片相应位置添加红色半透明文字水印, 文字有倾斜角 覆盖全图

import os.path as path
from os.path import join as join

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def ID_watermark_text(input_image_path, output_image_path,
                      text, text_pos, text_color, text_angle):
    """
    :param input_image_path:
    :param output_image_path:
    :param text:  水印文字内容
    :param text_pos: 相应位置
    """
    imagebg = Image.open(input_image_path)

    # 创建相同大小的 alpha 层
    waterMarkLayer = Image.new("RGBA", imagebg.size)

    # Get an ImageDraw object so we can draw on the image
    waterdraw = ImageDraw.ImageDraw(waterMarkLayer, "RGBA")
    textFont = ImageFont.truetype("/Library/Fonts/Microsoft/Kaiti.ttf", 150)
    waterdraw.text(text_pos, text, fill=text_color, font=textFont)

    # Get the waterMarkLayer image as grayscale and fade the image
    # See <http://www.pythonware.com/library/pil/handbook/image.htm#Image.point>
    #  for information on the point() function
    # Note that the second parameter we give to the min function determines
    #  how faded the image will be. That number is in the range [0, 256],
    #  where 0 is black and 256 is white. A good value for fading our white
    #  text is in the range [100, 200].
    watermask = waterMarkLayer.convert("L").point(lambda x: min(x, 100))
    # Apply this mask to the waterMarkLayer image, using the alpha filter to
    #  make it transparent
    waterMarkLayer.putalpha(watermask)
    waterMarkLayer = waterMarkLayer.rotate(text_angle)
    # Paste the waterMarkLayer (with alpha layer) onto the original image and save it
    imagebg.paste(waterMarkLayer, None, waterMarkLayer)
    imagebg.show()

    imagebg.save(output_image_path, "JPEG")


if __name__ == '__main__':
    up = path.expanduser('~')

    input = join(up, '百度云同步盘/相册/ID1.JPEG')
    output = join(up, '百度云同步盘/相册/qingguan2.JPEG')

    textcontent = u"""仅供海关清关用, 他用无效\n 有效期: 2019.4.8-2019.4.10"""
    textcolor = (255, 8, 12)  # red
    textangle = 30

    ID_watermark_text(input, output,
                      text=textcontent, text_color=textcolor,
                      text_pos=(150, 500), text_angle=textangle)
