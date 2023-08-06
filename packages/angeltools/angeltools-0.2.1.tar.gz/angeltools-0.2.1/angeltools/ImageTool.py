# -*- coding: utf-8 -*-
import io
import os
import sys
from pathlib import Path

import requests
from numpy import array
from tqdm import tqdm

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


def image2chars(image_path, width=120, k=1.0, reverse=False, outfile=None, chart_list=None):
    """
    照片转为字符，默认120个字符宽度
    """
    from PIL import Image
    import numpy as np

    im = Image.open(image_path).convert("L")  # 打开图片文件，转为灰度格式
    height = int(k * width * im.size[1] / im.size[0])  # 打印图像高度，k为矫正系数，用于矫正不同终端环境像素宽高比
    # im.show()
    arr = np.array(im.resize((width, height)))  # 转为NumPy数组
    if reverse:  # 反色处理
        arr = 255 - arr
    arr = strip_empty_line(arr)

    chart_list = chart_list if chart_list else [" ", ".", "-", "+", "=", "*", "#", "@"]   # 灰度-字符映射表
    chs = np.array(chart_list)
    arr = chs[(arr / (int(255/len(chart_list))+1)).astype(np.uint8)]  # 灰度转为对应字符

    if outfile:
        with open(outfile, "w") as fp:
            for row in arr.tolist():
                row_str = "".join(row)
                fp.write(row_str)
                fp.write("\n")
    else:
        for i in range(arr.shape[0]):  # 逐像素打印
            for j in range(arr.shape[1]):
                print(arr[i, j], end=" ")
            print()


def text2image(text, size=None, font_color=None, back_color=None, save_path=None, font_path=None):
    """
    文字转照片
    :param text:
    :param size:
    :param font_color:
    :param back_color:
    :param save_path:
    :param font_path:
    :return:
    """

    font_path = check_font_path(font_path)
    size = int(size) if size else 50
    font_color = tuple(font_color) if font_color else (0, 0, 0)
    back_color = tuple(back_color) if back_color else (255, 255, 255)

    if save_path:
        save_path = Path(save_path)
        if save_path.exists():
            os.remove(save_path.absolute())
        save_path = str(save_path.absolute())
    else:
        save_path = io.BytesIO()

    pygame.init()
    font = pygame.font.Font(font_path, size)
    render_text = font.render(text, True, font_color, back_color)

    pygame.image.save(render_text, save_path)
    return save_path


def strip_empty_line(arr: array):

    r_temp = [sum(r) for r in arr]
    rs = get_empty_line_start(r_temp)
    re = get_empty_line_start(r_temp[::-1])
    re = len(r_temp) - re

    r_temp_t = [sum(r) for r in arr.T]
    cs = get_empty_line_start(r_temp_t)
    ce = get_empty_line_start(r_temp_t[::-1])
    ce = len(r_temp_t) - ce

    return arr[rs:re, cs:ce]


def get_empty_line_start(num_lis: list):
    rs = 0
    has_empty = False
    for ri, r_temp_sum in enumerate(num_lis):
        if not r_temp_sum:
            rs = ri
            has_empty = True
        else:
            break
    return rs + 1 if has_empty else rs


def check_font_path(font_path):
    if font_path and os.path.exists(font_path):
        return font_path
    base_path = Path(__file__).parent
    local_font_dir = base_path / 'fonts'
    local_msyh_font_path = local_font_dir / 'msyh-B.ttf'
    if os.path.exists(local_msyh_font_path.absolute()):
        return local_msyh_font_path
    print("downloading font: msyh-B.ttf")
    if not os.path.exists(local_font_dir.absolute()):
        os.makedirs(local_font_dir.absolute())
    try:
        font_res = requests.get('https://www.tuling.icu/static/admin/fonts/msyh-B.ttf', stream=True)
        total_size = int(int(font_res.headers["Content-Length"]) / 1024 + 0.5)
        with open(local_msyh_font_path.absolute(), 'wb') as fd:
            for chunk in tqdm(iterable=font_res.iter_content(1024), total=total_size, unit='k', desc=None):
                fd.write(chunk)
            print("download success!")
    except Exception as E:
        print(f"Error when downloading font: {E}")
        sys.exit(1)
    return str(local_msyh_font_path.absolute())


def text2chars(text, font_path=None, width=None, k=None, outfile=None, chart_list=None):
    img = text2image(text, size=100, font_path=font_path)
    image2chars(img, width=width, k=k, outfile=outfile, reverse=True, chart_list=chart_list)


if __name__ == "__main__":
    # text2image(
    #     'ABC',
    #     size=50,
    #     # font_path='/etc/fonts/msyh.ttf',
    #     font_color=[0, 0, 0],
    #     back_color=[],
    #     # save_path='/home/ABC.png'
    # )

    # image2chars(
    #     '/home/测试123.png',
    #     width=100,
    #     k=0.6,
    #     # outfile='/home/测试123.txt',
    #     reverse=True
    # )

    text2chars(
        "ANGEL",
        # font_path='/etc/fonts/msyh.ttf',
        width=50,
        k=0.6,
        # outfile='/home/测试123.txt',
        chart_list=[' ', '-', '/', '%'],
    )
