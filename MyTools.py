# coding=utf-8
from decimal import Decimal

# 自有工具类
# noinspection PyPep8Naming
class MyTools:
    def __init__(self):
        pass

    # 删除所有空格
    @staticmethod
    def trim(s):
        ss = str(s)
        A = ss.split()
        return ''.join(A)

    # 数字小写一对一转汉字大写
    @staticmethod
    def convertNumToCap(d):
        dictChinese = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
        A = []
        s = "%d" %d
        for c in list(s):
            i = int(c)
            A.append(dictChinese[i])
        return ''.join(A)

    @staticmethod
    def convertNumToChinese(n):
        units = ['', '万', '亿']
        nums = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
        decimal_label = ['角', '分']
        small_int_label = ['', '拾', '佰', '仟']
        d = Decimal(n).quantize(Decimal('0.00'))
        int_part, decimal_part = str(int(d)), str(d - int(d))[2:] # 分离整数和小数部分

        res = []
        if decimal_part:
            tmp = ''.join([nums[int(x)] + y for x, y in list(zip(decimal_part, decimal_label)) if x != '0'])
            if tmp == '':
                tmp = '整'
            res.append(tmp)
        else:
            res.append('整')

        if int_part != '0':
            res.append('圆')
            while int_part:
                small_int_part, int_part = int_part[-4:], int_part[:-4]
                tmp = ''.join([nums[int(x)] + (y if x != '0' else '') for x, y in
                               list(zip(small_int_part[::-1], small_int_label))[::-1]])
                tmp = tmp.rstrip('零').replace('零零零', '零').replace('零零', '零')
                unit = units.pop(0)
                if tmp:
                    tmp += unit
                    res.append(tmp)
        return ''.join(res[::-1])


        # 是否合法数字

    @staticmethod
    def legal_numbers(s):
        try:
            float(s)
        except ValueError:
            return False
        else:
            return True

    # 是否合法数字，包括汉字数字
    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    # str转BOOL类型
    @staticmethod
    def str_to_bool(s):
        return True if s.lower() == 'true' else False
