import time

import numpy
import psutil

"""
算数工具
"""


class Scaler:
    """
        比例器
        一些控制数值区间的方法
    """
    def __init__(self):
        pass

    def arctan(self, x, lower_point_x: int or float = 1, lower_limit=80, upper_limit=100):
        """
        the function graphic pass the point (lower_point_x, lower_limit)
        反正切函数, 用于控制连续变量最大值区间。
        人话就是用反正切计算比例，确保一个数不超出你锁定的范围
        要确定一个反正切函数，最少需要确定函数过某一个点，此处称为 锚点

        :param x                变量x
        :param lower_point_x    锚点的x值
        :param lower_limit      锚点的y值
        :param upper_limit      y值上限
        """

        up = upper_limit
        lo = lower_limit
        if isinstance(x, str):
            x = float(x)
        if x > 0:
            a = numpy.tan([numpy.pi / 2 * lo / up]) / lower_point_x
            score = (up / (numpy.pi / 2)) * numpy.arctan(a * x)[0]
        else:
            score = 0
        return score


def cpu_sta(interval=1.0, cpu_limit=None, memory_limit=None):
    cpu_limit = cpu_limit if cpu_limit else 99
    memory_limit = memory_limit if memory_limit else 90
    cpu_flag, memory_flag = 1, 1
    try:
        cpu_percent = psutil.cpu_percent(interval=interval)
        if cpu_percent > cpu_limit:
            cpu_flag = 0
        virtual_memory = psutil.virtual_memory()
        memory_percent = virtual_memory.percent
        if memory_percent > memory_limit:
            memory_flag = 0
    except Exception as e:
        print(e)
    return [cpu_flag, memory_flag]


def wait_cpu_available(cpu_limit=None, memory_limit=None, block=True, log=None, interval=1.0):
    cpu_limit = cpu_limit if cpu_limit else 99
    memory_limit = memory_limit if memory_limit else 90
    if not all([
        isinstance(cpu_limit, (int, float)),
        isinstance(memory_limit, (int, float)),
    ]):
        return True

    if block:
        wait_count = 0
        while sum(cpu_sta(interval, cpu_limit=cpu_limit, memory_limit=memory_limit)) != 2:
            time.sleep(1)
            wait_count += 1
            if log and (wait_count * interval) % 10 == 0:
                log(" - cpu or memory usage is over limit! - ")
    else:
        return sum(cpu_sta(interval, cpu_limit=cpu_limit, memory_limit=memory_limit)) != 2
    return True


if __name__ == "__main__":
    wait_cpu_available()
