from MtySdk import *

USERNAME    =   "请输入用户名"
PASSWORD    =   "请输入密码"

# 注册信息模型
auth = MtyAuth(USERNAME,PASSWORD)
# 声明数据操作工具
mty2Api = Mty2Api(auth);

# 目标品种
symbolnames  =  ["DCE.i2203","DCE.i2203-C-1000"]
# 时间颗粒度  mty2Api.FIVE_MINUTE： 5分钟，  mty2Api.SIXTY_MINUTE： 整点
timeStepSize = mty2Api.SIXTY_MINUTE;

# 数据时间段
starttime    =  "2021-04-06 14:55:00"
endtime      =  "2022-02-11 14:55:00"

# 账户初始资金
amount = 100000;

# 数据挂载数据工厂
mty2Api.initmath(symbolnames=symbolnames , starttime=starttime , endtime=endtime ,timeStepSize=timeStepSize);

# 消费数据
while mty2Api.ishaving():
    # 获取下一条数据的时间间隔 ， 秒为单位
    item = mty2Api.getmath(None);

    if(item['time'] == '2021-04-08 14:00:00'):
        # 开仓
        symbol = 'DCE.i2203-C-1000';
        mty2Api.openorder(symbol,mty2Api.BUY,2,item[symbol]);

    if (item['time'] == '2021-04-08 14:00:00'):
        # 开仓
        symbol = 'DCE.i2203';
        mty2Api.openorder(symbol, mty2Api.BUY, 1, item[symbol]);

    if (item['time'] == '2021-10-25 21:00:00'):
        # 平仓
        symbol = 'DCE.i2203';
        mty2Api.closeorder(symbol, mty2Api.SELL, 1, item[symbol]);

    if (item['time'] == '2021-10-25 21:00:00'):
        # 平仓
        symbol = 'DCE.i2203-C-1000';
        mty2Api.closeorder(symbol, mty2Api.SELL, 2, item[symbol]);
    print(item)

# 保存数据
mty2Api.saveplan(amount);


