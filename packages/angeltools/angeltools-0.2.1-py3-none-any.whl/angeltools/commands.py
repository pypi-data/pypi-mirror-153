import argparse
import json
import os.path
import time
from pathlib import Path

from BaseColor.base_colors import hred, green, yellow, hblue

from angeltools.SysTool import cmd_sta, run_cmd
from angeltools.ImageTool import text2chars, image2chars


def txt2chars(args=None):
    dp = ' *** 文字转字符块小工具'
    da = "--->   "
    parser = argparse.ArgumentParser(description=dp, add_help=True)
    parser.add_argument("text", type=str, default='Hello', help=f'{da} 任何文字')
    parser.add_argument("-f", "--font_path", type=str, dest="font_path",
                        default=None, help=f'{da} 指定字体文件，默认使用系统字体')
    parser.add_argument("-w", "--width", type=int, dest="width",
                        default=100, help=f'{da} 输出字符块的宽度')
    parser.add_argument("-k", "--aspect_ratio", type=float, dest="aspect_ratio",
                        default=1.0, help=f'{da} 输出字符块的宽高比')
    parser.add_argument("-s", "--outfile", type=str, dest="outfile",
                        default=None, help=f'{da} 输出字符块位置，默认在终端打印不保存')
    parser.add_argument("-c", "--chart_list", type=str, dest="chart_list",
                        default='[" ", ".", "-", "+", "=", "*", "#", "@"]',
                        help=f'{da} 灰度字符列表，json格式，默认：[" ", ".", "-", "+", "=", "*", "#", "@"]')

    args = parser.parse_args()
    text = args.text
    font_path = args.font_path
    width = args.width
    aspect_ratio = args.aspect_ratio
    outfile = args.outfile
    chart_list = args.chart_list

    if not text and not text.strip():
        raise ValueError('空白文字')
    if font_path and not os.path.exists(font_path):
        raise ValueError(f"字体文件不存在: {font_path}")
    if width:
        try:
            width = int(width)
        except:
            raise ValueError('-w width 参数应该为int类型')
        if width <= 0:
            raise ValueError("-w width 参数应该大于0")
    if aspect_ratio:
        try:
            aspect_ratio = float(aspect_ratio)
        except:
            raise ValueError('-k aspect_ratio 参数应该为float类型')
        if aspect_ratio <= 0:
            raise ValueError("-k aspect_ratio 参数应该大于0")
    if outfile:
        outfile_path = Path(outfile)
        try:
            outfile_path.touch()
        except:
            raise ValueError(f'无法在此路径创建文件: {outfile_path.parent.absolute()}')
    if chart_list:
        try:
            chart_list = json.loads(chart_list)
        except:
            raise ValueError("-c chart_list 参数不正确")

    text2chars(
        text,
        font_path=font_path,
        width=width,
        k=aspect_ratio,
        outfile=outfile,
        chart_list=chart_list,
    )


def img2chars(args=None):
    dp = ' *** 图片转字符块小工具'
    da = "--->   "
    parser = argparse.ArgumentParser(description=dp, add_help=True)
    parser.add_argument("image", type=str, default=None, help=f'{da} 图片路径')

    parser.add_argument("-w", "--width", type=int, dest="width",
                        default=100, help=f'{da} 输出字符块的宽度')
    parser.add_argument("-k", "--aspect_ratio", type=float, dest="aspect_ratio",
                        default=1.0, help=f'{da} 输出字符块的宽高比')
    parser.add_argument("-s", "--outfile", type=str, dest="outfile",
                        default=None, help=f'{da} 输出字符块位置，默认在终端打印不保存')
    parser.add_argument("-nr", "--not_reverse", type=bool, dest="not_reverse", nargs='?', default=False,
                        help=f'{da} 是否不先反转颜色再生成')
    parser.add_argument("-c", "--chart_list", type=str, dest="chart_list",
                        default='[" ", ".", "-", "+", "=", "*", "#", "@"]',
                        help=f'{da} 灰度字符列表，json格式，默认：[" ", ".", "-", "+", "=", "*", "#", "@"]')

    args = parser.parse_args()
    image = args.image
    width = args.width
    aspect_ratio = args.aspect_ratio
    outfile = args.outfile
    reverse = True if not args.not_reverse else False
    chart_list = args.chart_list

    if not image and not image.strip():
        raise ValueError('空白图片路径')

    if width:
        try:
            width = int(width)
        except:
            raise ValueError('-w width 参数应该为int类型')
        if width <= 0:
            raise ValueError("-w width 参数应该大于0")
    if aspect_ratio:
        try:
            aspect_ratio = float(aspect_ratio)
        except:
            raise ValueError('-k aspect_ratio 参数应该为float类型')
        if aspect_ratio <= 0:
            raise ValueError("-k aspect_ratio 参数应该大于0")
    if outfile:
        outfile_path = Path(outfile)
        try:
            outfile_path.touch()
        except:
            raise ValueError(f'无法在此路径创建文件: {outfile_path.parent.absolute()}')
    if chart_list:
        try:
            chart_list = json.loads(chart_list)
        except:
            raise ValueError("-c chart_list 参数不正确")

    image2chars(
        image_path=image,
        width=width,
        k=aspect_ratio,
        outfile=outfile,
        reverse=reverse,
        chart_list=chart_list
    )


def cmd_status(args=None):
    dp = ' *** linux 进程cpu内存查看'
    da = "--->   "
    parser = argparse.ArgumentParser(description=dp, add_help=True)
    parser.add_argument("keyword", type=str, default=None, help=f'{da} 关键字')

    parser.add_argument("-i", "--interval", type=float, dest="interval", default=1, help=f'{da} 刷新间隔')
    parser.add_argument("-s", "--sorted_by", type=str, dest="sorted_by", default='pid', help=f'{da} 排序方式，pid、cpu、men、name。分别对应：进程id，cpu百分比，内存百分比，进程名')
    parser.add_argument("-r", "--sorted_reverse", type=str, dest="sorted_reverse", nargs='?', default='n', help=f'{da}y/n 是否反向排序，默认否')
    parser.add_argument("-d", "--detail", type=str, dest="detail", nargs='?', default='n', help=f'{da}y/n 是否显示命令全路径，默认否')

    args = parser.parse_args()
    keyword = args.keyword
    if not keyword and keyword.strip():
        print("keyword is required!")
        return False

    try:
        interval = float(args.interval) or 1.0
    except:
        print("Interval Error, float number is required!")
        return False

    sorted_by = args.sorted_by
    sorted_reverse = args.sorted_reverse
    detail = args.detail
    detail = False if detail else True
    sorted_reverse = False if sorted_reverse else True

    try:
        cmd_sta(keyword, interval, detail, sorted_by, sorted_reverse)
    except KeyboardInterrupt:
        print("\n exit")
    except Exception as E:
        print(f"\n Error: {E}")
    return


def timing_cmd(args=None):
    dp = ' *** linux 定时执行命令'
    da = "--->   "
    parser = argparse.ArgumentParser(description=dp, add_help=True)
    parser.add_argument("cmd", type=str, default=None, nargs='?', help=f'{da} 命令')

    parser.add_argument("-i", "--interval", type=float, dest="interval", default=60, help=f'{da} 执行间隔，单位秒，默认60s')
    parser.add_argument("-f", "--file", type=str, dest="file", default=None, help=f'{da} 命令所在文件的路径，文件内每行一条命令。若设置了此文件参数，则前面位置参数将失效')

    args = parser.parse_args()
    cmd_list = [args.cmd]
    interval = float(args.interval) if args.interval else 60
    file = args.file

    if file and os.path.exists(file):
        with open(file, 'r') as rf:
            cmd_list = [x.strip() for x in rf.readlines()]
    try:
        print(f'will run this command(s) in every {hred(interval)} seconds')
        for cmd in cmd_list:
            print(f"    {green(cmd)}")
        print()
        for t in range(1, 5):
            print(f'\rstarting in {hred(5-t)} s', end='')
            time.sleep(1)
        print()

        count = 1
        while True:
            for cmd in cmd_list:
                try:
                    print(f"running {yellow(cmd)}")
                    run_cmd(cmd)
                except KeyboardInterrupt:
                    print(f'cancel command: {cmd}')
                    print(hred(f'hit ctrl+c again to quit all commands'))
                except Exception as RTE:
                    print(RTE)
            print(f"loop {hblue(count)} done! waiting {hred(interval)} seconds")
            time.sleep(interval)
            count += 1
    except KeyboardInterrupt:
        print('sys out')
    except Exception as RCE:
        print(RCE)


if __name__ == '__main__':
    txt2chars()
