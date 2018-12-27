# coding=utf-8
import math

#自有工具类
class MyTools():
    def __init__(self):
        pass
        
    #删除所有空格
    def trim(self, s):
        ss = str(s)
        A = ss.split()
        return ''.join(A)

    #数字小写一对一转汉字大写
    def convertNumToCap(self, s):
        if not self.legal_numbers(s):
            return ''
        dictChinese = ['零','壹','贰','叁','肆','伍','陆','柒','捌','玖']
        A = []
        for c in list(s):
            i = int(c)
            A.append(dictChinese[i])
        return ''.join(A)
        
    #金额小写转大写
    def convertNumToChinese(self, totalPrice):
        if not self.legal_numbers(totalPrice):
            return ''
        dictChinese = ['零','壹','贰','叁','肆','伍','陆','柒','捌','玖']
        unitChinese = ['','拾','佰','仟','萬','拾','佰','仟']
        #将整数部分和小数部分区分开
        partA = int(math.floor(totalPrice))
        partB = round(totalPrice-partA, 2)
        strPartA = str(partA)
        strPartB = ''
        if partB != 0:
            strPartB = str(partB)[2:]
    
        singleNum = []
        if len(strPartA) != 0:
            i = 0
            while i < len(strPartA):
                singleNum.append(strPartA[i])
                i = i+1
        #将整数部分先压再出，因为可以从后向前处理，好判断位数 
        tnumChinesePartA = []
        numChinesePartA = []
        j = 0
        bef = '0';
        if len(strPartA) != 0:
            while j < len(strPartA) :
                curr = singleNum.pop()
                if curr == '0' and bef !='0':
                    tnumChinesePartA.append(dictChinese[0])
                    bef = curr
                if curr != '0':
                    tnumChinesePartA.append(unitChinese[j])
                    tnumChinesePartA.append(dictChinese[int(curr)])
                    bef = curr
                if j == 3:
                    tnumChinesePartA.append('萬')
                    bef = '0'
                j = j+1
    
            for i in range(len(tnumChinesePartA)):
                numChinesePartA.append(tnumChinesePartA.pop())
        A = ''      
        for i in numChinesePartA:
            A = A+i
        #小数部分很简单，只要判断下角是否为零
        B = ''
        if len(strPartB) == 1:
            B = dictChinese[int(strPartB[0])] + '角'
        if len(strPartB) == 2 and strPartB[0] != '0':
            B = dictChinese[int(strPartB[0])] + '角' + dictChinese[int(strPartB[1])] + '分'
        if len(strPartB) == 2 and strPartB[0] == '0':
            B = dictChinese[int(strPartB[0])] + dictChinese[int(strPartB[1])] + '分'
    
        if len(strPartB) == 0:
            S = A + '圆整'
        if len(strPartB)!= 0:
            S = A + '圆' +B
        return S 
    
    #是否合法数字
    def legal_numbers(self, s):
        try:
            float(s)
        except ValueError:
            return False
        else:
            return True
            
    #是否合法数字，包括汉字数字
    def is_number(self, s):
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
    
    #str转BOOL类型
    def str_to_bool(str):
        return True if str.lower() == 'true' else False
