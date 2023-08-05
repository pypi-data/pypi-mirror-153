from MtySdk import *
import sys

def getNameList(symbolname):
    """
    获取测试范围，通过期货名称
    :param symbolname:
    :return:
    """
    resultlist = [];
    # 名称寻找对应的期权
    mathlist = data2Api.getMathNames();
    for mathItem in mathlist:
        mathname = mathItem['symbolname']
        container = symbolname in mathname
        if container :
            resultlist.append(mathname)
    return resultlist;

def getZhixingjia(symbolname):
    """
    获取执行价
    :param symbolname:
    :return:
    """
    if ('DCE.' in symbolname) or ("CFFEX." in symbolname):
        return symbolname[symbolname.rfind('-') + 1:len(symbolname)]

    if ('CZCE.' in symbolname) or ('SHFE.' in symbolname):
        for i in range(len(symbolname), 0, -1):
            # 倒数第一个大写字母
            if symbolname[i - 1].isupper():
                return symbolname[symbolname.rfind(symbolname[i - 1]) + 1: len(symbolname)]

def getQiquanName(qihuoname , zhixingjia , corp):
    '''
    根据期货名称和执行价还原一个看涨或看跌期权名称
    :param qihuoname:  期权名称
    :param zhixingjia:  执行价
    :param corp:        看涨或者看跌
    :return:
    '''
    if ('DCE.' in qihuoname):
        return qihuoname+ ("-%s-%s"%(corp , zhixingjia));
    if ('CZCE.' in qihuoname) or ('SHFE.' in qihuoname) :
        return qihuoname + corp + zhixingjia;

def getKsymbols(currentprice , symbolnames , num):
    """
    获取测试品种范围
    :param currentprice:    现价
    :param symbolnames:     品种列表
    :param num:             品种数量
    :return:
    """
    for symbos in symbolnames:
        # 执行价最近的8个执行价
        zhixingjialist = [];
        for index in range(len(symbolnames)):
            symbol =  symbolnames[index]
            getKsymbol(zhixingjialist,symbol,currentprice,num*2);
        return zhixingjialist;

def getKsymbol(zhixingjialist , symbolname , currentprice , num):
    if len(symbolname) <= 12 : return;
    if len(zhixingjialist) < num :
        zhixingjialist.append(getZhixingjia(symbolname));
    else:
        index = 0;
        # 差距最大执行价
        maxIndex = None ;
        for zhixingjia in zhixingjialist:
            if maxIndex == None:
                maxIndex = index;
            else:
                if abs(float(zhixingjialist[index]) - float(currentprice)) > abs(float(zhixingjialist[maxIndex]) - float(currentprice)):
                    maxIndex = index;
            index += 1;

        # 差距是否比列表中的差距最大的元素小
        symbolnamezhixingjialimit = abs(float(getZhixingjia(symbolname)) - float(currentprice));
        if symbolnamezhixingjialimit < abs(float(zhixingjialist[maxIndex]) - float(currentprice)) and getZhixingjia(symbolname)  not in zhixingjialist:
            zhixingjia = int(getZhixingjia(symbolname))
            zhixingjialist[maxIndex] = str(zhixingjia)

def filterItem(item,symbolnames):
    """
    过滤没有价格的品种列表
    :param item:
    :param symbolnames:
    :return:
    """
    symbolsareas = [];
    for symbolname in symbolnames:
        if item[symbolname] is not None:
            symbolsareas.append(symbolname)
    return symbolsareas;

def mp_sort(arr):

    if len(arr) <= 1:
        return
    i = 0
    # 外循环控制循环次数 每一次循环结束后，最大的数都会在后面
    while i < len(arr):
        j = 0
        # 内循环从0开始控制比较次数
        while j < len(arr)-1-i:
            # 比较 如果前一个数大于后一个数 则换位置
            if int(arr[j]) > int(arr[j+1]):
                temp = arr[j+1]
                arr[j+1] = arr[j]
                arr[j] = temp
            j += 1
        i += 1
    return arr;

def noMath(c, p , item ):
    try:
        if item[c] == None:
            return True;
    except:
        # print(c + "没有数据");
        return True;
        pass

    try:
        if item[p] == None:
            return True;
    except:
        # print(c + "没有数据");
        return True;
        pass

    return False;

def maypoint(keysymbols , item , qihuoname , percent):
    '''
    是否买点
    :param keysymbols:          [执行价区间]
    :param item:                [数据包]
    :param qihuoname:           期货名称
    :param percent:             千分之8
    :return:
    '''
    # 遍历组合
    # 遍历K1和K2
    havepoint = False;
    k1index = 0
    while k1index < len(keysymbols):
        k2index = 0
        k1zhixingjia = keysymbols[k1index];
        c1 = getQiquanName(qihuoname ,k1zhixingjia , "C");
        p1 = getQiquanName(qihuoname ,k1zhixingjia , "P");
        if noMath(c1, p1,item):
            k1index += 1
            continue;

        c1currentprice = item[c1]['close'];
        p1currentprice = item[p1]['close'];

        # 内循环从0开始控制比较次数
        while k2index < len(keysymbols) - 1 - k1index:

            k2zhixingjia = keysymbols[k2index];
            c2 = getQiquanName(qihuoname, k2zhixingjia, "C");
            p2 = getQiquanName(qihuoname, k2zhixingjia, "P");
            if noMath(c2, p2, item ):
                k2index += 1
                continue;
            c2currentprice = item[c2]['close'];
            p2currentprice = item[p2]['close'];

            # a值计算
            a = geta(c1,p1,c2,p2,item , percent);

            # 公式比较
            havepoint = calcPoint(c1currentprice , p1currentprice , k1zhixingjia , c2currentprice , p2currentprice , k2zhixingjia , a );
            if havepoint: return True;

            k2index += 1
        k1index += 1

    return False;

def geta(c1,p1,c2,p2,item, percent):
    # 4个单子的手续费（开平）
    servicecharge = None;
    # 权利金
    quanlijin = None;
    try:
        # 4个单子的手续费（开平）
        servicecharge =  (float(item[c1]["servicechargeshare"]) +
                            float(item[p1]["servicechargeshare"]) +
                                float(item[c2]["servicechargeshare"]) +
                                    float(item[p2]["servicechargeshare"])) * 2;
        # 权利金
        quanlijin = ((float(item[c1]['close']) * float(item[c1]['tradingunit'])) +
                        (float(item[c2]['close']) * float(item[c2]['tradingunit'])) +
                            (float(item[p1]['close']) * float(item[p1]['tradingunit'])) +
                                (float(item[p2]['close']) * float(item[p2]['tradingunit'])));
    except:
        print(c1,p2,c2,p2, " 在这组数据测试中， 上传的数据可能是有问题的.")
        sys.exit(-1)

    a = ( servicecharge + quanlijin ) * percent;
    return a ;

def calcPoint(c1 , p1 , k1 , c2 , p2 , k2 , a):
    """
    判断此刻是否是买点
    :param c1:
    :param p1:
    :param k1:
    :param c2:
    :param p2:
    :param k2:
    :param a:
    :return:
    """
    if ( float(c1) - float(p1) + float(k1)) - (float(c2) - float(p2) +  float(k2) ) > a :
        print("have may point !!!!");
        return True;

if __name__ == '__main__':
    USERNAME = "credi"
    PASSWORD = "admin123"
    # 测试期货
    testsymbol = "CZCE.CF209"
    # 数据时间段
    starttime = "2021-06-10 14:55:00"
    endtime = "2022-02-11 14:55:00"
    # 测试组数
    num = 4;
    # 乘量， 止盈比例
    percent = 0.008;

    # 注册信息模型
    auth = MtyAuth(USERNAME, PASSWORD)
    data2Api = Data2Api(auth=auth)

    # 声明数据操作工具
    mty2Api = Mty2Api(auth);

    # 测试品种列表
    symbolnames = getNameList(testsymbol);

    # 时间颗粒度  mty2Api.FIVE_MINUTE： 5分钟，  mty2Api.SIXTY_MINUTE： 整点
    timeStepSize = mty2Api.FIVE_MINUTE;

    # 数据挂载数据工厂
    mty2Api.initmath(symbolnames=symbolnames, starttime=starttime, endtime=endtime, timeStepSize=timeStepSize);

    # 消费数据
    while mty2Api.ishaving():
        # 获取下一条数据的时间间隔 ， 秒为单位
        item = mty2Api.getmath(None);
        # 期货实时价格
        qihuocurrentprice:str = item[testsymbol]['close']
        # 有行情的品种名单
        symbolareas:list = filterItem(item, symbolnames);
        # 品种范围
        keysymbols:list = getKsymbols(qihuocurrentprice, symbolareas , num);
        keysymbols = mp_sort(keysymbols);
        # 买点
        if keysymbols is None : continue;
        havemaypoint = maypoint(keysymbols , item ,testsymbol, percent);

        print(qihuocurrentprice)
        print(havemaypoint);
        if havemaypoint == None:
            print(havemaypoint);
            maypoint(keysymbols, item, testsymbol, percent)
        if havemaypoint :
            sys.exit(-1)

        '''
        是否买点
        :param keysymbols:          [执行价区间]
        :param item:                [数据包]
        :param qihuoname:           期权名称
        :param percent:             千分之8
        '''


