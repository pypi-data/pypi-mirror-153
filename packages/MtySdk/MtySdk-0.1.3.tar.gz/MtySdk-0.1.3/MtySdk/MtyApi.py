#coding=utf-8

from websocket import create_connection
import json
import csv
import datetime
import sys
import matplotlib.pyplot as plt
import requests
import time

IP = "192.168.0.114"
WSPORT = "9999"
HTTPPORT = "9999"


class MtyAuth(object):
    """
    客户信息类
    """
    def __init__(self,user_name: str = "", password: str = ""):
        self.username=user_name;
        self.password=password;

class Data2Api(object):

    BUY = 1;
    SELL = 2;

    OPEN = 1;
    CLOSE = 2;
    CLOSETODAY = 3;

    def __init__(self,auth: MtyAuth=""):
        self.mathlist = [];
        self.username = auth.username;
        self.password = auth.password;

        self.OPEN = 1;
        self.CLOSE = 2;
        self.CLOSETODAY = 3;

    def getMathNames(self):
        """
        获取数据库所有品种
        :return:
        """
        url = "http://%s:%s/mtyj/regresstest2/data/urecord" %(IP,HTTPPORT)
        response = requests.get(url)
        if (response.status_code == 200):
            resp = json.loads(response.text)
            if (resp['code'] == 200):
                return resp['result'];
            else:
                print(resp['msg'])
                return;
        else:
            print("网络通信失败")
            return;

    def clearMath(self, filePath: str):
        """
        约定格式csv文件读取函数
        :param filePath:
        :return:
        """

        try:
            with open(filePath) as f:
                csvTemplete = csv.reader(f)
                header = next(csvTemplete)

                index = 0;
                list = [];

                for row in csvTemplete:
                    model = {
                        'datetime': datetime.datetime.strftime(datetime.datetime.fromtimestamp(int(row[1][0:10])),
                                                               '%Y-%m-%d %H:%M:%S'),
                        'datetimeNano': int(row[1][0:10]),
                        'open': row[2],
                        'high': row[3],
                        'low': row[4],
                        'close': float(row[5]),
                        'volume': row[6]
                    }
                    list.append(model)
                    index += 1;

                return list;
        except Exception as e:
            print("非约定格式的csv文件")
            sys.exit(0);

    def getMc(self, symbolname):

        url = "http://%s:%s/mtyj/mc/queryByParam?symbol=%s" % (IP, HTTPPORT, symbolname)

        response = requests.get(url)

        if (response.status_code == 200):
            resp = json.loads(response.text)
            if (resp['code'] == 200):
                return resp['result'];
            else:
                print(resp['msg'])
                return;
        else:
            print("网络通信失败")
            return;

    def getZhixingjialogo(self,symbolname):
        """
        期权名称获取期权的涨跌标志
        :param symbolname:
        :return:  C/P
        """
        if ('DCE.' in symbolname) or ("CFFEX." in symbolname):
            return symbolname[symbolname.rfind('-')-1:symbolname.rfind('-')]
        if ('CZCE.' in symbolname) or ('SHFE.' in symbolname):
            for i in range(len(symbolname), 0, -1):
                # 倒数第一个大写字母
                if symbolname[i - 1].isupper():
                    return symbolname[str.rfind(str[i - 1]): str.rfind(str[i - 1]) + 1]

    def getZhixingjia(self,symbolname):
        """
        期权名称获取期权的执行价
        :param symbolname:
        :return:
        """
        if ('DCE.' in symbolname) or ("CFFEX." in symbolname):
            return symbolname[symbolname.rfind('-') + 1:len(symbolname)]

        if ('CZCE.' in symbolname) or ('SHFE.' in symbolname):
            for i in range(len(symbolname), 0, -1):
                # 倒数第一个大写字母
                if symbolname[i - 1].isupper():
                    return symbolname[str.rfind(str[i - 1]) + 1: len(str)]

    # 计算保证金
    def getEarnestMoney(self ,mc, symbolname , direction ,currentprice , qihuocurrentprice):
        """
        计算保证金
        :param mc                   行情信息
        :param symbolname:          品种名称
        :param direction:           买卖方向
        :param currentprice:        当前价格
        :param qihuocurrentprice:   对应期货价格
        :return:
        """
        # 交易单位
        tradingUnity = float(mc['tradingUnit'])
        # 保证金费率
        smRate = float(mc['smRate']);

        # 期货保证金
        if len(symbolname) <= 12:
            # 期货价格 * 交易单位 * 保证金费率
            return float(currentprice) * tradingUnity * smRate

        # 期权保证金
        if len(symbolname) > 12:
            # 买期权(BUY)保证金为0
            if direction == self.BUY:
                return 0;

            # 卖期权(SELL)保证金计算：
            # A. （期权价格 * 交易单位） + （期权对应期货价格 * 交易单位 * 保证金费率） - （0.5 * 虚值额）
            # B.(期权价格 * 交易单位) + （0.5 *（期权对应期货价格 * 交易单位 * 保证金费率））
            # A和B计算结果做比较 ， 期权保证金取大的值。
            if direction == self.SELL:

                xvzhie = self.getxvzhie(symbolname,currentprice,qihuocurrentprice)
                a = (float(currentprice) * tradingUnity) + (float(qihuocurrentprice) * tradingUnity * smRate) - (0.5 * xvzhie);
                b = (float(currentprice) * tradingUnity) + (0.5*(float(qihuocurrentprice) * tradingUnity * smRate))
                if a > b:
                    return a;
                else:
                    return b;

    # 计算虚值额
    def getxvzhie(self,symbolname , currentprice , qihuoprice):
        logo = self.getZhixingjialogo(symbolname);
        if logo == 'C':
            # (期权对应期货价格 - 期货行权价格) > 0 , 保证金 = 0
            # (期权对应期货价格 - 期货行权价格) < 0 , 保证金 = 期权对应期货价格 - 期货行权价格
            if float(currentprice) - float(qihuoprice) > 0:
                return 0;
            else:
                return float(qihuoprice) - float(currentprice);
        if logo == 'P':
            # (期权对应期货价格 - 期货行权价格) > 0, 保证金 = 期权对应期货价格 - 期货行权价格
            # (期权对应期货价格 - 期货行权价格) < 0, 保证金 = 0
            if float(currentprice) - float(qihuoprice) > 0:
                return float(qihuoprice) - float(currentprice);
            else:
                return 0;

    # 计算手续费
    def getServiceCharge(self,mc,symboname,direction,currentprice):
        """
        计算手续费
        :param mc:          行情信息
        :param symboname:   名称
        :param direction:   开平方向
        :param currentprice: 现价
        :return:
        """
        # 期权交易费用
        optionsCose = float(mc['optionsCost'])
        # 交易所费用
        brokerageFee = float(mc['brokerageFee'])
        # 交易单位
        tradingUnity = float(mc['tradingUnit'])
        # 期货交易费率
        tradeRate = float(mc['tradeRate'])
        # 期货交易费用
        tradeCost = float(mc['tradeCost'])
        # 平今费率
        rateWithindays = float(mc['rateWithindays'])
        # 平今费用
        costWithindays = float(mc['costWithindays'])

        # 期权手续费计算
        if len(symboname) > 12:
            # (期权交易费用 + 交易所费用) ， 结果乘以手数
            return optionsCose + brokerageFee

        # 期货手续费
        if len(symboname) <= 12 :
            # 期货开仓和平昨手续费计算公式：
            #   (期货现价 * 交易单位 * 期货交易费率) + 期货交易费用 + 交易所费用 ， 得到的结果乘以手数
            if direction == self.OPEN or direction == self.CLOSE:
                return ( currentprice * tradingUnity * tradeRate) + tradeCost + brokerageFee
            # 期货平今手续费计算公式:
            #   (期货现价 * 交易单位 * 平今费率) + 平今费用 + 交易所费用 ， 得到的结果乘以手数
            if direction == self.CLOSETODAY:
                return (currentprice * tradingUnity * rateWithindays) +  costWithindays + brokerageFee


    def upload(self,symboname: str, mathlist: list):

        isFutures = len(symboname) <= 12;                                        # 是期货
        for item in mathlist:

            if item['tradingunit'] == None:
                print("请为tradingunit值添加交易单位")
                return;

            if(isFutures):
                if item['earnestmoney'] == None:
                    print("请为earnestmoney值添加期货保证金计算结果")
                    return;
                if item['servicechargeOpenclose'] == None:
                    print("请为servicechargeOpenclose值添加期货开仓平昨手续费计算结果")
                    return;
                if item['servicechargeClosetoday'] == None:
                    print("请为servicechargeClosetoday值添加期货平今手续费计算结果")
                    return;

            else:
                if item['earnestmoney'] == None:
                    print("请为earnestmoney值添加期权卖时保证金计算结果")
                    return;
                if item['servicechargeshare'] == None:
                    print("请为servicechargeshare值添加期权手续费计算结果")
                    return;



        """
        数据上传功能
        :param symboname:       品种名称
        :param username:        用户名
        :param password:        密码
        :param mathlist:        数据列表
        :return:
        """
        param = {
            'datalist': mathlist,
            'symboname': symboname,
            'username': self.username,
            'password': self.password
        }
        header = {
            'Content-Type': 'application/json;charset=UTF-8'
        }

        url = "http://%s:%s/mtyj/regresstest2/data/addlist" % (IP,HTTPPORT)


        response = requests.post(url, data=json.dumps(param),headers=header, timeout=60)
        print(response.status_code)
        print(response.text)

    def registerData(self, symbolname ):
        """
        注册一个历史数据到内容
        :param symboname:
        :return:
        """
        url = "http://%s:%s/mtyj/regresstest2/data/futuresMath?password=%s&symboname=%s&username=%s"%(IP,HTTPPORT,self.password,symbolname,self.username)
        response = requests.get(url)
        if(response.status_code == 200):
            result = json.loads(response.text);
            if(result['code'] == 200):
                self.mathlist = result['result']
            else:
                print(result['msg'])
                return;
        else:
            print("网络连接未成功");
            return;

    def getResiterDataByTime(self, timezone:int):
        """
        从注册数据池中获取数据
        :param timezone:
        :return:
        """
        isInt = isinstance(timezone, int)

        if isInt == False & len(str(timezone)) :
            print("请输入int类型的10位时间戳");
            return ;

        if len(self.mathlist) <= 0:
            print("请在查询使用前，使用registerData函数来注册数据")
            return;

        for item in self.mathlist:
            if(item['datetimeNano'] == timezone):
                return item;
        return None;

    def getFuturesname(self , shareOptionName):
        """
        通过期权名称找期货名称
        :param shareOptionName:
        :return:
        """
        url = "http://%s:%s/mtyj/regresstest2/data/getFuturesname?shareOptionName=%s"%(IP,HTTPPORT,shareOptionName)
        response = requests.get(url)
        if (response.status_code == 200):
            result = json.loads(response.text);
            if (result['code'] == 200):
                return result['result']
            else:
                print(result['msg'])
                return;
        else:
            print("网络连接未成功");
            return;

    def queryMathList(self, symboname ,username , password):
        """
        获取品种的历史数据
        :param symboname:
        :return:
        """
        url = "http://%s:%s/mtyj/regresstest2/data/futuresMath?symboname=%s&username=%s&password=%s" % (
        IP, HTTPPORT, symboname, username , password)
        response = requests.get(url)
        if (response.status_code == 200):
            result = json.loads(response.text);
            if (result['code'] == 200):
                return result['result']
            else:
                print(result['msg'])
                return;
        else:
            print("网络连接未成功");
            return;

    def mathAt(self,symboname):
        """
        数据是否上传完成
        :param symboname:
        :return:
        """
        url = "http://%s:%s/mtyj/regresstest2/data/mathAt?symboname=%s" % (IP, HTTPPORT, symboname)
        response = requests.get(url)
        if (response.status_code == 200):
            result = json.loads(response.text);
            if (result['code'] == 200):
                return result['result']
            else:
                print(result['msg'])
                return;
        else:
            print("网络连接未成功");
            return;

class Mty2Api(object):

    FIVE_MINUTE  = 1;
    SIXTY_MINUTE = 2;

    BUY = 1;
    SELL = 2;

    def __init__(self, auth: MtyAuth = ""):
        # 测试计划id
        self.testplanid = None;
        # 数据索引
        self.index = 0;
        # 品种集
        self.symbols = [];
        # 时间尺
        self.timecriterion = []
        # 数据集
        self.datalist = [];
        self.username = auth.username;
        self.password = auth.password;
        # 注册数据参数
        self.starttime = None;
        self.endtime = None;

    def ishaving(self):
        '''
        数据推送2 . 数据工厂是否还有下一条数据
        :return:
        '''
        if self.index < len(self.timecriterion):
            return True;
        else:
            self.uptestplanid = self.testplanid;
            self.testplanid = None;
            self.starttime = None;
            self.endtime = None;
            self.symbols = [];
            self.timecriterion = [];
            self.datalist = [];
            self.index = 0;


            return False;

    def getmath(self,second:int):
        """
        数据推送3 . 从数据工厂获取下一条未读数据
        :param second: 获取数据的时间间隔
        :return:
        """
        # 延迟功能
        if second != None:
            time.sleep(second)

        itemResult = {}
        # 历史时间
        timezone = self.timecriterion[self.index]
        itemResult['time'] = time.strftime("%Y-%m-%d %H:%M:%S", (time.localtime(timezone)));
        for symbol in self.symbols:
            # 品种的数据包
            itemlist = self.datalist[symbol];
            # 从品种数据包提取指定时间的数据
            item = self.getItemToListByTime(itemlist, timezone);
            itemResult[symbol] = item;

        # 下标游动
        self.index = self.index + 1;
        return itemResult;

    def getItemToListByTime(self , itemList , timezong):
        """
        从数据堆中找指定时间的数据
        :param itemList:
        :param timezong:
        :return:
        """
        for item in itemList:
            if item['datetimeNano'] == timezong:
                return item;
                break;

        return None;

    def initmath(self ,symbolnames:list , starttime:str , endtime:str, timeStepSize:int):
        """
        数据推送1 . 数据装载数据工厂
        :param symbolnames:
        :param starttime:
        :param endtime:
        :param timeStepSize:
        :return:
        """
        if isinstance(symbolnames, list) == False:
            print("symbolnames参数要求一个list类型参数")
            return
        if len(symbolnames) <= 0:
            print("至少一个目标品种数据")
            return

        url = "http://%s:%s/mtyj/regresstest2/data/futruesMathList" %(IP,HTTPPORT)
        url = url + "?timeStepSize=%s&endDate=%s&startDate=%s" %(timeStepSize,endtime,starttime)

        for symbolname in symbolnames:
            url = url + ("&symbolnames=%s" %symbolname)

        print(">>>>>>>>>>>>>>>>>>>数据工厂开始装卸数据<<<<<<<<<<<<<<<<<<<<<<<")

        response = requests.get(url)
        if response.status_code == 200:
            result = json.loads(response.text)
            if(result['code'] == 200):
                resultInfo = result['result']
                self.symbols = symbolnames;
                self.starttime = starttime;
                self.endtime = endtime;
                self.timestepsize = timeStepSize;
                self.timecriterion = resultInfo['timecriterion'];
                self.datalist = resultInfo['math'];
            else:
                print(result['msg'])
                return;
        else:
            print("请检查参数后，重新请求");
            return;

    def closeorder(self,symbol:str , statu:int , volumn:int , item:object):
        """
        平仓
        :param symbol:
        :param statu:
        :param volumn:
        :param item:
        :return:
        """
        param = {
            "testPlanId": self.testplanid,
            "statu": statu,
            "volume": volumn,
            "item": item,
            "symboname": symbol,
            "symbonames": self.symbols,
            "starttime": self.starttime,
            "endtime": self.endtime
        }
        url = "http://%s:%s/mtyj/regresstest2/data/closeorder" % (IP, HTTPPORT)
        header = {
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = requests.post(url, data=json.dumps(param), headers=header);
        if (response.status_code == 200):
            result = json.loads(response.text);
            if (result['code'] == 200):
                self.testplanid = self.testplanid;
                return result['msg']
            else:
                print(result['msg']);
                return;
        else:
            return "网络通信失败,请检查参数后重试";

    def openorder(self , symbol:str ,statu:int , volumn:int , item:object ):
        """
        开仓
        :param symbol:
        :param statu:
        :param volumn:
        :param item:
        :return:
        """
        param = {
            "testPlanId": self.testplanid,
            "statu":statu,
            "volume":volumn,
            "item":item,
            "symboname":symbol,
            "symbonames": self.symbols,
            "starttime": self.starttime,
            "endtime": self.endtime,
            "timestepsize":self.timestepsize,
            "username":self.username,
            "password":self.password
        }
        url = "http://%s:%s/mtyj/regresstest2/data/openorder" % (IP, HTTPPORT)
        header = {
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = requests.post(url,data=json.dumps(param),headers=header);
        if(response.status_code == 200):
            result = json.loads(response.text);
            if(result['code'] == 200):
                self.testplanid = result['result']['testplanid'];
                return result['msg']
            else:
                print(result['msg']);
                return;
        else:
            return "网络通信失败,请检查参数后重试";

    def saveplan(self , initamount):
        """
        保存测试计划
        :param initamount:
        :return:
        """
        if initamount is None:
            print("初始资金错误");
            return;

        url = "http://%s:%s/mtyj/regresstest2/data/savePlanMath?testplanId=%s&amount=%s" % (IP, HTTPPORT , self.uptestplanid , initamount)
        header = {
            'Content-Type': 'application/json;charset=UTF-8'
        }
        response = requests.get(url,  headers=header);
        if (response.status_code == 200):
            result = json.loads(response.text);
            if (result['code'] == 200):
                print(result['msg'])
                return result['msg']
            else:
                print(result['msg']);
                return;
        else:
            return "网络通信失败,请检查参数后重试";

class DataApi(object):

    def clearMath(self,filePath: str):
        """
        约定格式csv文件读取函数
        :param filePath:
        :return:
        """

        try:
            with open(filePath) as f:
                csvTemplete = csv.reader(f)
                header = next(csvTemplete)

                index = 0;
                list = [];

                for row in csvTemplete:
                    model = {
                        'datetime': datetime.datetime.strftime(datetime.datetime.fromtimestamp(int(row[1][0:10])),
                                                               '%Y-%m-%d %H:%M:%S'),
                        'datetimeNano': int(row[1][0:10]),
                        'open': row[2],
                        'high': row[3],
                        'low': row[4],
                        'close': float(row[5]),
                        'volume': row[6]
                    }
                    list.append(model)
                    index += 1;

                return list;
        except Exception as e:
            print("非约定格式的csv文件")
            sys.exit(0);

    def upload(self,symboname: str, username: str, password: str, mathlist: list):
        """
        数据上传功能
        :param symboname:       品种名称
        :param username:        用户名
        :param password:        密码
        :param mathlist:        数据列表
        :return:
        """
        param = {
            'datalist': mathlist,
            'symboname': symboname,
            'username': username,
            'password': password
        }
        header = {
            'Content-Type': 'application/json;charset=UTF-8'
        }

        url = "http://%s:%s/mtyj/regresstest/data/addlist" % (IP,HTTPPORT)

        response = requests.post(url, data=json.dumps(param),headers=header)
        print(response.status_code)
        print(response.text)

class MtyApi(object):
    """
    API类
    """
    def __init__(self,auth: MtyAuth=""):
        """
        初始化通信管道
        :param auth:
        """
        self.IP = IP
        self.WSPORT = WSPORT
        self.HTTPPORT = HTTPPORT
        self.ws = create_connection("ws://%s:%s/mtyj/regres/%s/%s/" %(self.IP,self.WSPORT,auth.username,auth.password))
        createresult = self.ws.recv()
        print(createresult)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    def is_having(self):
        """
        队列是否还有数据
        :return:
        """
        param = {
            'function': 'ishaving'
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        result = json.loads(result)
        if (result['code'] == 200):
            return result['result']

    def query_math(self,name: str,starttime: str=None , endtime: str=None):
        """
        # 申请消费队列的消息
        ;param name:         名称
        :param starttime:   开始时间
        :param endtime:     结束时间
        :return:
        """
        param={
            'function':'registerserver',
            'name':name,
            'startDate':starttime,
            'endData':endtime
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        result = json.loads(result)
        if (result['code'] == 0):
            print(result['msg'])
            return;
        if (result['code'] == 200):
            result['name']=name
            result['testplanid']=result['result']
            return result

        self.close();
        return None;

    def get_math(self,math):

        if math is None: return;

        """
        队列消费数据
        :param order:
        :return:
        """
        param = {
            'function': 'queryqueue',
            'name':math['name']
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        result = json.loads(result)
        return result;

    def closeposition(self,math,result,statu,price:float,volume:int):

        if statu != 'BUY' and statu!= 'SELL':
            print("statu必须是 SELL 或 BUY")
            return;

        symbol = math['name']
        if symbol is None:
            print("品种名称未填写");
            return;

        testplanid = math['testplanid']
        if testplanid is None:
            print("不符合规则的使用")
            return;

        datetime = result['datetime']
        if datetime is None:
            print("不符合规则的使用")
            return;

        if price is None:
            print("请填写报价");
            return

        if volume is None:
            print("请填写手数")
            return

        param = {
            'function': 'closeposition',
            'statu': statu,
            'symbol': symbol,
            'testplanid': testplanid,
            'datetime': datetime,
            'price': price,
            'volume': volume
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        print(result)

    def openoptions(self,math,result,statu,price:float,volume:int):

        if statu != 'BUY' and statu!= 'SELL':
            print("statu必须是 SELL 或 BUY")
            return;

        symbol = math['name']
        if symbol is None:
            print("品种名称未填写");
            return;

        testplanid = math['testplanid']
        if testplanid is None:
            print("不符合规则的使用")
            return;

        datetime = result['datetime']
        if datetime is None:
            print("不符合规则的使用")
            return;

        if price is None:
            print("请填写报价");
            return

        if volume is None:
            print("请填写手数")
            return

        param = {
            'function': 'openposition',
            'statu': statu,
            'symbol': symbol,
            'testplanid': testplanid,
            'datetime': datetime,
            'price':price,
            'volume':volume
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        print(result)

    def incomeline(self,testPlanId):

        param = {
            'function': 'earnings',
            'testPlanId': testPlanId
        }
        self.ws.send(json.dumps(param))

    def incomelineresult(self):
        result = self.ws.recv()
        return result;

    def queryEarnestMoney(self, volume:int,symboname:str,price:float,direction:str,fururePrice:float):
        """
        获取期货交易保证金
        :param volume:      手数
        :param symboname:   期货名称
        :param price:       期货价格
        :param direction:   买卖方向（BUY | SELL)
        :param fururePrice: 非必填，查询期权保证金时需要输入对应期期货的价格
        :return:
        """

        if volume is None:
            print("手数未设置")
            return
        if symboname is None:
            print("名称未设置")
            return
        if direction is None:
            print("买卖方向未设置")
            return
        if direction != 'BUY' and direction != 'SELL' :
            print("买卖方向只允许BUY,SELL")
            return;
        if price is None:
            print("期货价格未设置")
            return;

        url = "http://%s:%s/mtyj/regresstest/historydata/earnestMoney?volume=%s&symboname=%s&price=%s&direction=%s" % (
            self.IP,self.HTTPPORT,volume, symboname, price, direction)
        if fururePrice is not None:
            url = url + "&fururePrice=%s" %fururePrice;

        response = requests.get(url);
        if response.status_code == 200:
            return json.loads(response.text)['result'];
        else:
            return print(json.loads(response.text)['msg']);


    def queryServiceCharge(self,volume: int, symboname: str, direction: str, currentPrice: float):
        """
        获取交易手续费
        :param volume:      手数
        :param symboname:   期货名称
        :param direction:   多空方向 （OPEN | CLOSE | TODAYCLOSE）
        :param currentPrice: 期货价格
        :return:
        """
        if volume is None :
            print("手数未设置")
            return
        if symboname is None:
            print("名称未设置")
            return
        if direction is None:
            print("开平标志未设置")
            return
        if direction != 'CLOSE' and direction != 'OPEN' and direction != 'TODAYCLOSE':
            print("开平标志只允许OPEN,CLOSE,TODAYCLOSE")
            return
        if currentPrice is None:
            print("期货价格未设置")
            return;

        url = "http://%s:%s/mtyj/regresstest/historydata/serviceCharge?volume=%s&symboname=%s&direction=%s&price=%s" % (
        self.IP,self.HTTPPORT,volume, symboname, direction, currentPrice)
        response = requests.get(url);
        if response.status_code == 200:
            return json.loads(response.text)['result'];
        else:
            return print(json.loads(response.text)['msg']);

    def close(self):
        self.ws.close();

def showline(code):
    # 使用员工账号连接系统
    api = MtyApi(auth=MtyAuth('credi', 'admin123'))

    # 2. 查询资金
    api.incomeline(code);

    # 开窗
    plt.ion()
    # 开窗
    plt.figure(1)
    # x轴
    t_list = []
    # 实时价格
    result_list = []
    # 实时收益
    result_list2 = []

    while True:
        try:

            result = api.incomelineresult()
            if result is '':
                api.close();
                while True:
                    plt.pause(10)  # 暂停0,1秒

            result = json.loads(result)
            print(result)

            t_list.append(result['datetime'])  # x轴
            # result_list.append(result['close'])
            result_list2.append(result['income'])

            # plt.plot(t_list, result_list, color='red', marker='*', linestyle='-', label='A')
            plt.plot(t_list, result_list2, color='blue', marker='*', linestyle='-', label='B')

            plt.pause(0.1)  # 暂停0,1秒

        except:
            api.close();
            t_list.clear()
            result_list2.clear()
            result_list.clear()
            plt.clf()  # 清理窗体数据
            break
            pass