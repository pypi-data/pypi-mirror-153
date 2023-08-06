#  The MIT License (MIT)
#
#  Copyright (c) 2021. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.


from sc_utilities import Singleton


class MoneyUtils(metaclass=Singleton):
    """
    金额相关工具类
    """

    def __init__(self):
        pass

    @classmethod
    def transfer_money_unit(cls, money: float, amount_unit="万元"):
        # 根据金额单位计算金额除数
        divider = cls.get_money_unit_divider(amount_unit)
        return money / divider

    @classmethod
    def get_money_unit_divider(cls, amount_unit):
        divider = 1
        if amount_unit == "元":
            divider = 1
        elif amount_unit == "万元":
            divider = 10000
        elif amount_unit == "亿元":
            divider = 100000000
        return divider
