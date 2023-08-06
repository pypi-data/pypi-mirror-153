from decimal import *


def add(nums, *args) -> float or int:
    """
    计算多个数字的和
    例如：
    >>> add(12, 12, 12)
    36
    >>> add([12, 11, 10])
    33
    
    """
    result = 0
    if type(nums) != list:
        for i in args:
            nums += i
        return nums
    else:
        for i in nums:
            result += i
        return result
        


def multiply(nums, *args) -> float or int:
    """
    计算多个数字的乘积
    """
    for i in args:
        nums *= i
    return nums


def div(nums, *args) -> float or int:
    """
    计算数字之间的商
    """
    for i in args:
        nums /= i
    return nums


def power(n, ex) -> float:
    """
    计算数字的多次幂
    例如:
    >>> power(2, 2)
    4.0
    >>> power(1.1, 2)
    1.21
    >>> power(-2, 3)
    -8.0
    """
    result = Decimal('1.0')
    for i in range(ex):
        result *= Decimal(str(n))
    return float(result)


def average(nums, *args) -> float:
    """
    计算平均数
    例如:
    >>> average(1, 3, 5)
    3.0
    >>> average([1, 2, 3])
    2.0
    """
    if type(nums) == list:
        return add(nums) / len(nums)
    else:
        return add(list(tuple([nums]) + args)) / (len(args) + 1)


def delta(nums: list) -> float:
    """
    求方差
    例如:
    >>> delta([1, 2, 3, 4, 5])
    2.0
    """
    l = []
    for i in nums:
        l.append(power(i - average(nums), 2))
    return add(l) / len(nums)


def wac(nums: dict) -> float:
    """
    求加权平均数
    例如:
    >>> wac({10: 1, 20: 2, 30: 1})
    20.0
    """
    n1, n2 = Decimal(), Decimal()
    for k, v in nums.items():
        n1 += k * v
        n2 += v
    return float(n1 / n2)


class Point(tuple):
    def __init__(self):
        self.x = self[0]
        self.y = self[1]

    @classmethod
    def distance(cls, p1, p2):
        x_d = p1.x - p2.x
        y_d = p1.y - p2.y
        return (x_d ** 2 + y_d ** 2) ** 0.5

    @classmethod
    def judge(cls, p1, p2, p3):
        side1 = cls.distance(p1, p2)
        side2 = cls.distance(p2, p3)
        side3 = cls.distance(p1, p3)
        sides = [side1, side2, side3]
        sides.sort()

        if sides[0] + sides[1] <= sides[2]:
            return 'Error'
