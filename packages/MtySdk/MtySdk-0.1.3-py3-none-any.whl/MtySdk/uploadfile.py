from MtyApi import *
import os
import time
import sys
from tqdm import tqdm

# 文件夹地址
UPLOADFILEPATH = "E:\回测数据\CACE.CF209"
USERNAME = "credi"
PASSWORD = "admin123"

auth = MtyAuth(USERNAME, PASSWORD)
data2Api = Data2Api(auth);
matyapi = MtyApi(auth=MtyAuth(USERNAME, PASSWORD))

class UploadMath(object):

    def __init__(self ):

        # 期货
        self.QIHUOLIST = []
        # 期权
        self.QIQUANLIST = []
        # 总任务
        self.SUMNUM = 0;
        # 目前任务
        self.LIMITNUM = 0;

    """
    通过期货期权的名称获得交易单位
    """
    def getTradingUnity(self,symbolname):
        resp = data2Api.getMc(symbolname);
        if(resp == None ):
            raise Exception('%s这个品种在行情信息表中没有数据');
        return resp['tradingUnit'];


    """
    期货上传
    """
    def qihuoUpload(self):
        for qihuo in self.QIHUOLIST:

            filepath = UPLOADFILEPATH+"\\"+qihuo;
            symbolname = qihuo.split('.csv')[0];
            TradingUnity = self.getTradingUnity(symbolname);

            # 数据是否上传完成
            at = data2Api.mathAt(symbolname);
            if at == False:
                # B . 期货数据上传
                # 从本地csv文件加载期货数据
                mathlist = data2Api.clearMath(filepath)
                # 行情信息
                mc = data2Api.getMc(symbolname)
                # 游标
                currentindex = 0;
                # 为期货挂载手续费和保证金计算结果
                for item in mathlist:
                    item['earnestmoney'] = data2Api.getEarnestMoney(mc, symbolname, data2Api.OPEN , item['close'], None)
                    item['servicechargeOpenclose']  = data2Api.getServiceCharge(mc,symbolname,data2Api.OPEN , item['close']);
                    item['servicechargeClosetoday'] = data2Api.getServiceCharge(mc,symbolname,data2Api.CLOSETODAY , item['close']);

                    item['tradingunit'] = TradingUnity
                    # 打印数据挂载加载进度
                    currentindex+=1;
                    self.printSymboLoading(symbolname, len(mathlist) , currentindex);

                # 上传数据
                data2Api.upload(symbolname , mathlist);

            # 进度条刷新
            self.LIMITNUM += 1;
            self.printProject();

    """
    期权上传
    """
    def qiquanUpload(self):
        for qiquan in self.QIQUANLIST:
            filepath = UPLOADFILEPATH + "\\" + qiquan;
            symbolname = qiquan.split('.csv')[0];
            TradingUnity = self.getTradingUnity(symbolname);

            # 行情信息
            mc = data2Api.getMc(symbolname)

            # 数据是否上传完成
            at = data2Api.mathAt(symbolname);
            if at == False:

                # B . 期货数据上传
                # 从本地csv文件加载期货数据
                mathlist = data2Api.clearMath(filepath)
                # 为期货挂载手续费和保证金计算结果
                currentindex = 0;

                # 期权名称转化期货名称
                qihuoname = data2Api.getFuturesname(symbolname);
                # 期货名称获取历史数据,
                list = data2Api.queryMathList(qihuoname, USERNAME, PASSWORD);

                uploadlist = []

                for item in mathlist:

                    try:
                        item['earnestmoney'] = data2Api.getEarnestMoney(mc, symbolname, data2Api.OPEN, item['close'], self.getqihuoprice(list , item['datetimeNano']))
                        item['servicechargeshare'] = data2Api.getServiceCharge(mc,symbolname,data2Api.OPEN,item['close']);
                        item['tradingunit'] = TradingUnity
                        uploadlist.append(item);
                    except:
                        continue;

                    # 打印数据挂载加载进度
                    currentindex += 1;
                    self.printSymboLoading(symbolname, len(mathlist), currentindex);

                # 上传数据
                data2Api.upload(symbolname, uploadlist);

            # 进度条刷新
            self.LIMITNUM += 1;
            self.printProject();

    """
    通过名称和时间戳获取对应期货品种对应时间的价格
    """
    def getqihuoprice(self , list, datetimeNano:int ):

        # 获取指定时间戳的数据
        item = self.getItemByTime(list , datetimeNano)
        return item['close'];

    def getItemByTime(self , list ,datetimeNano):
        for item in list :
            if item['datetimeNano'] == datetimeNano:
                return item;

        return None;

    '''
    加载文件夹目录
    :param dirPath:
    :return:
    '''
    def readDir(self,dirPath):

        if dirPath[-1] == '/':
            print
            u'文件夹路径末尾不能加/'
            return

        if os.path.isdir(dirPath):
            fileList = os.listdir(dirPath)
            self.SUMNUM =len(fileList);

            for f in fileList:
                if len(f) > 12+4:
                    self.QIQUANLIST.append(f)
                else:
                    self.QIHUOLIST.append(f)
        else:
            print('Error,not a dir')

    """
    数据挂载进度打印
    """
    def printSymboLoading(self ,symboname, length , currentSize):
        pansal = currentSize / length * 100
        limit = (int)(currentSize / length * 100);

        str = "\033[1;32;40m[%s]  " %currentSize;
        str = str + "%s数据处理进度: %s [" % (symboname,round(pansal, 2))
        for item in range(1, 100):
            if (item <= limit):
                str = str + " -";
            else:
                str = str + " .";
        str = str + "] ";
        # print(str)


    """
    任务进度打印
    """
    def printProject(self):

        #os.system('cls')
        # 百分比进度
        pansal = self.LIMITNUM / self.SUMNUM * 100
        limit = (int)(self.LIMITNUM / self.SUMNUM * 100);

        str = "\033[31m任务进度: %s [" % round(pansal, 2);
        for item in range(1, 100):
            if (item <= limit):
                str = str + " -"
            else:
                str = str + " ."
        print(str)

if __name__ == '__main__':

    upload = UploadMath();
    ## 加载文件路径
    upload.readDir(UPLOADFILEPATH);

    ## 初始进度打印
    upload.printProject();

    # 期货上传
    upload.qihuoUpload();

    # 期权上传
    upload.qiquanUpload();


