import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np

plt.rcParams['font.sans-serif']=['SimHei']  # 用于显示中文
plt.rcParams['axes.unicode_minus'] = False  # 用于显示中文

string = ""

def getcsv():#获取csv中的数据集
    results=[]
    with open('One/shop.csv',encoding='UTF-8')as f:
        f_csv = csv.reader(f)
        next(f_csv)
        for row in f_csv:
            isBlank = 0
            re=[]
            for i in range(len(row)):
                if 1 <= i <= 4 and row[i]!="":
                    re.append(row[i])
            results.append(re)
        return (results)

def loadDataSet():
    return [[1, 2, 3], [4, 2], [4, 1, 3], [4, 2], [1, 5, 3], [4, 1, 2], [4, 1, 5, 3], [4, 1, 2], [1, 2]]

# 获取候选1项集，dataSet为事务集。返回一个list，每个元素都是set集合
def createC1(dataSet):
    C1 = []   # 元素个数为1的项集（非频繁项集，因为还没有同最小支持度比较）
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()  # 这里排序是为了，生成新的候选集时可以直接认为两个n项候选集前面的部分相同
    # 因为除了候选1项集外其他的候选n项集都是以二维列表的形式存在，所以要将候选1项集的每一个元素都转化为一个单独的集合。
    return list(map(frozenset, C1))   #map(frozenset, C1)的语义是将C1由Python列表转换为不变集合（frozenset，Python中的数据结构）

# 找出候选集中的频繁项集
# dataSet为全部数据集，Ck为大小为k（包含k个元素）的候选项集，minSupport为设定的最小支持度
def scanD(dataSet, Ck, minSupport):
    ssCnt = {}   # 记录每个候选项的个数--字典形式
    for tid in dataSet:
        for can in Ck:
           if can.issubset(tid):#issubset() 方法用于判断集合的所有元素是否都包含在指定集合中
             ssCnt[can] = ssCnt.get(can, 0) + 1   # 计算每一个项集出现的频率
    #print(ssCnt)
    numItems = float(len(dataSet))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)  #将频繁项集插入返回列表的首部
            supportData[key] = support
    #print(retList)
    return retList, supportData   #retList为在Ck中找出的频繁项集（支持度大于minSupport的），supportData记录各频繁项集的支持度

# 通过频繁项集列表Lk和项集个数k生成候选项集C(k+1)。
def aprioriGen(Lk, k):
    retList = []
    #print(Lk)
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            # 前k-1项相同时，才将两个集合合并，合并后才能生成k+1项
            L1 = list(Lk[i])[:k-2];
            L2 = list(Lk[j])[:k-2]   # 取出两个集合的前k-1个元素
            L1.sort();
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    #print(retList)
    return retList

# 获取事务集中的所有的频繁项集
# Ck表示项数为k的候选项集，最初的C1通过createC1()函数生成。Lk表示项数为k的频繁项集，supK为其支持度，Lk和supK由scanD()函数通过Ck计算而来。
def apriori(dataSet, minSupport):
    C1 = createC1(dataSet)  # 从事务集中获取候选1项集
    D = list(map(set, dataSet))  # 将事务集的每个元素转化为集合
    L1, supportData = scanD(D, C1, minSupport)  # 获取频繁1项集和对应的支持度
    L = [L1]  # L用来存储所有的频繁项集
    k = 2
    while (len(L[k-2]) > 0): # 一直迭代到项集数目过大而在事务集中不存在这种n项集
        Ck = aprioriGen(L[k-2], k)   # 根据频繁项集生成新的候选项集。Ck表示项数为k的候选项集
        Lk, supK = scanD(D, Ck, minSupport)  # Lk表示项数为k的频繁项集，supK为其支持度
        L.append(Lk);
        supportData.update(supK)  # 添加新频繁项集和他们的支持度
        k += 1
    return L, supportData


def calcConf(freqSet, H, supportData, br1, minConf):  # 筛选符合可信度要求的规则，并返回符合可信度要求的右件
    prunedH = []  # 存储符合可信度的右件
    data = []
    for conseq in H:  # conseq就是右件，freqSet是原始频繁项,freqSet-conseq是左件
        conf = supportData[freqSet] / supportData[freqSet - conseq]  # 计算可信度
        lift = supportData[freqSet] / (supportData[freqSet - conseq] * supportData[conseq])
        if conf >= minConf:
            #print(freqSet - conseq, "-->", conseq, "\tconf:", conf,"\tlift:",lift)
            global string
            string = string + str((freqSet - conseq)) + "-->"+ str(conseq) + "\tconf:" + str(conf) +"\tlift:" + str(lift) + "\n"
            br1.append((freqSet - conseq, conseq, conf,lift))
        else:
            prunedH.append(conseq)  # 不符合可信度的右件添加到列表中
    return prunedH,data


def rulesFromConseq(freqSet, H, supportData, br1, minConf):  # 新版Apriori原理来减少创造的规则
    is_find = True  # 循环标志
    m = 1  # 先创造右件为一个元素的规则
    Hmp1 = H  # H是初始频繁项分散后的列表，[frozenset({2}),frozenset({3}),frozenset({5)],Hmp1是组合后的右件，因为我们的aprioriGen不能组建只有1个元素的右件，所以右件为1个元素的时候我们直接H赋值过去，当右件元素数是2以上的时候，再用aprioriGen组合出来
    while is_find:
        if len(freqSet) > m:  # 最多循环len(freqSet)-1次，因为右件最多len(freqSet)-1个元素，右件元素的数从1增长到len(freqSet)-1，故最多循环len(freqSet)-1次
            if m > 1:  # 我们改编的aprioriGen()函数至少产生C2,不能产生C1，因此这里加了if
                Hmp1 = aprioriGen(H, m)  # H里的元素自由组合成右件，右件的元素个数是m
            H_no = calcConf(freqSet, Hmp1, supportData, br1, minConf)  # 筛选符合可信度的规则,把不符合的右件存起来
            if len(H_no) != 0:  # 如果有不满足可信度的右件
                H_no = list(set(frozenset([item]) for row in Hmp1 for item in
                                row))  # 我们把列表中的每个元素都分割出来，比如[{2,3},{3,4}] 分割后为[{2},{3},{4}]，方便我们再次组合，这里也是Apriori原理的精髓所在，这么操作就是把不满足的右件及其超集提出来，然后后面做减法。
                H = list(set(H) - set(H_no))  # 可组合的集合减去不满足可信度的右件的集合
            m = m + 1  # 右件个数不断增加，第一次右件元素只有1个，第二次循环右件元素就有两个了
            if len(H) < m:  # 如果剩余的可自由组合的元素个数少于新右件所需要的元素数，比如就剩两个元素可组合了，想要组成C3作右件，肯定是不可能的，那么结束循环
                is_find = False
        else:  # 如果循环次数达到最大，也结束循环
            is_find = False


def generateRules(L, supportData, minConf):  # 产生规则
    bigRuleList = []
    for i in range(1, len(L)):  # 从L2开始创造规则
        if(i!=1):
            break
        for freqSet in L[i]:
            #print(freqSet)
            H1 = [frozenset([item]) for item in freqSet]
            if i > 1:  # L3开始使用Apriori原理
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:  # L2不能使用Apriori原理，只能老老实实挨个创造规则
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)

    return bigRuleList

def draw_heatmap(suppData):
    # pic = np.zeros((6, 6))  # 需要创建numpy矩阵填充支持度数据
    pic = np.eye(6)  # 需要创建numpy矩阵填充支持度数据
    for i in suppData.keys():  # 对支持度进行遍历，依次填充到矩阵当中
        if (len(i) == 2):
            d, e = i
            pic[d, e] = suppData[i]
            pic[e, d] = suppData[i]
    pic = np.delete(pic, 0, axis=1)
    pic = np.delete(pic, 0, axis=0)

    re = []
    for i in range(len(pic)):
        re.append([i, 0, str(pic[i][0])])
        re.append([i, 1, str(pic[i][1])])
        re.append([i, 2, str(pic[i][2])])
        re.append([i, 3, str(pic[i][3])])
        re.append([i, 4, str(pic[i][4])])

    return re

def load_data(minSupport = 0.15,minConf = 0.15):


    dataSet1 = getcsv()  # 牛奶面包数据
    L1, suppData1 = apriori(dataSet1, minSupport=minSupport)

    global string

    string = "二阶频繁项集为：\n"
    for ss in L1[1]:
        string = string + str(ss) + "\n"

    string = string + "关联规则以及其置信度和提升度：\n"

    rules= generateRules(L1, suppData1, minConf=minConf)


    dataSet0 = loadDataSet()  # 转换成数字的数据
    L0, suppData0 = apriori(dataSet0, minSupport=minSupport)
    re = draw_heatmap(suppData0)

    return re,string



