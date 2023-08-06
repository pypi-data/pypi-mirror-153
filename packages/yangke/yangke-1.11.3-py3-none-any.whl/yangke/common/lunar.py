# encoding: utf-8
g_lunar_month_day = [
    0x00752, 0x00ea5, 0x0ab2a, 0x0064b, 0x00a9b, 0x09aa6, 0x0056a, 0x00b59, 0x04baa, 0x00752,  # 1901 ~ 1910
    0x0cda5, 0x00b25, 0x00a4b, 0x0ba4b, 0x002ad, 0x0056b, 0x045b5, 0x00da9, 0x0fe92, 0x00e92,  # 1911 ~ 1920
    0x00d25, 0x0ad2d, 0x00a56, 0x002b6, 0x09ad5, 0x006d4, 0x00ea9, 0x04f4a, 0x00e92, 0x0c6a6,  # 1921 ~ 1930
    0x0052b, 0x00a57, 0x0b956, 0x00b5a, 0x006d4, 0x07761, 0x00749, 0x0fb13, 0x00a93, 0x0052b,  # 1931 ~ 1940
    0x0d51b, 0x00aad, 0x0056a, 0x09da5, 0x00ba4, 0x00b49, 0x04d4b, 0x00a95, 0x0eaad, 0x00536,  # 1941 ~ 1950
    0x00aad, 0x0baca, 0x005b2, 0x00da5, 0x07ea2, 0x00d4a, 0x10595, 0x00a97, 0x00556, 0x0c575,  # 1951 ~ 1960
    0x00ad5, 0x006d2, 0x08755, 0x00ea5, 0x0064a, 0x0664f, 0x00a9b, 0x0eada, 0x0056a, 0x00b69,  # 1961 ~ 1970
    0x0abb2, 0x00b52, 0x00b25, 0x08b2b, 0x00a4b, 0x10aab, 0x002ad, 0x0056d, 0x0d5a9, 0x00da9,  # 1971 ~ 1980
    0x00d92, 0x08e95, 0x00d25, 0x14e4d, 0x00a56, 0x002b6, 0x0c2f5, 0x006d5, 0x00ea9, 0x0af52,  # 1981 ~ 1990
    0x00e92, 0x00d26, 0x0652e, 0x00a57, 0x10ad6, 0x0035a, 0x006d5, 0x0ab69, 0x00749, 0x00693,  # 1991 ~ 2000
    0x08a9b, 0x0052b, 0x00a5b, 0x04aae, 0x0056a, 0x0edd5, 0x00ba4, 0x00b49, 0x0ad53, 0x00a95,  # 2001 ~ 2010
    0x0052d, 0x0855d, 0x00ab5, 0x12baa, 0x005d2, 0x00da5, 0x0de8a, 0x00d4a, 0x00c95, 0x08a9e,  # 2011 ~ 2020
    0x00556, 0x00ab5, 0x04ada, 0x006d2, 0x0c765, 0x00725, 0x0064b, 0x0a657, 0x00cab, 0x0055a,  # 2021 ~ 2030
    0x0656e, 0x00b69, 0x16f52, 0x00b52, 0x00b25, 0x0dd0b, 0x00a4b, 0x004ab, 0x0a2bb, 0x005ad,  # 2031 ~ 2040
    0x00b6a, 0x04daa, 0x00d92, 0x0eea5, 0x00d25, 0x00a55, 0x0ba4d, 0x004b6, 0x005b5, 0x076d2,  # 2041 ~ 2050
    0x00ec9, 0x10f92, 0x00e92, 0x00d26, 0x0d516, 0x00a57, 0x00556, 0x09365, 0x00755, 0x00749,  # 2051 ~ 2060
    0x0674b, 0x00693, 0x0eaab, 0x0052b, 0x00a5b, 0x0aaba, 0x0056a, 0x00b65, 0x08baa, 0x00b4a,  # 2061 ~ 2070
    0x10d95, 0x00a95, 0x0052d, 0x0c56d, 0x00ab5, 0x005aa, 0x085d5, 0x00da5, 0x00d4a, 0x06e4d,  # 2071 ~ 2080
    0x00c96, 0x0ecce, 0x00556, 0x00ab5, 0x0bad2, 0x006d2, 0x00ea5, 0x0872a, 0x0068b, 0x10697,  # 2081 ~ 2090
    0x004ab, 0x0055b, 0x0d556, 0x00b6a, 0x00752, 0x08b95, 0x00b45, 0x00a8b, 0x04a4f, ]

# 农历数据 每个元素的存储格式如下：
#    12~7         6~5    4~0
#  离元旦多少天  春节月  春节日
#####################################################################################
g_lunar_year_day = [
    0x18d3, 0x1348, 0x0e3d, 0x1750, 0x1144, 0x0c39, 0x15cd, 0x1042, 0x0ab6, 0x144a,  # 1901 ~ 1910
    0x0ebe, 0x1852, 0x1246, 0x0cba, 0x164e, 0x10c3, 0x0b37, 0x14cb, 0x0fc1, 0x1954,  # 1911 ~ 1920
    0x1348, 0x0dbc, 0x1750, 0x11c5, 0x0bb8, 0x15cd, 0x1042, 0x0b37, 0x144a, 0x0ebe,  # 1921 ~ 1930
    0x17d1, 0x1246, 0x0cba, 0x164e, 0x1144, 0x0bb8, 0x14cb, 0x0f3f, 0x18d3, 0x1348,  # 1931 ~ 1940
    0x0d3b, 0x16cf, 0x11c5, 0x0c39, 0x15cd, 0x1042, 0x0ab6, 0x144a, 0x0e3d, 0x17d1,  # 1941 ~ 1950
    0x1246, 0x0d3b, 0x164e, 0x10c3, 0x0bb8, 0x154c, 0x0f3f, 0x1852, 0x1348, 0x0dbc,  # 1951 ~ 1960
    0x16cf, 0x11c5, 0x0c39, 0x15cd, 0x1042, 0x0a35, 0x13c9, 0x0ebe, 0x17d1, 0x1246,  # 1961 ~ 1970
    0x0d3b, 0x16cf, 0x10c3, 0x0b37, 0x14cb, 0x0f3f, 0x1852, 0x12c7, 0x0dbc, 0x1750,  # 1971 ~ 1980
    0x11c5, 0x0c39, 0x15cd, 0x1042, 0x1954, 0x13c9, 0x0e3d, 0x17d1, 0x1246, 0x0d3b,  # 1981 ~ 1990
    0x16cf, 0x1144, 0x0b37, 0x144a, 0x0f3f, 0x18d3, 0x12c7, 0x0dbc, 0x1750, 0x11c5,  # 1991 ~ 2000
    0x0bb8, 0x154c, 0x0fc1, 0x0ab6, 0x13c9, 0x0e3d, 0x1852, 0x12c7, 0x0cba, 0x164e,  # 2001 ~ 2010
    0x10c3, 0x0b37, 0x144a, 0x0f3f, 0x18d3, 0x1348, 0x0dbc, 0x1750, 0x11c5, 0x0c39,  # 2011 ~ 2020
    0x154c, 0x0fc1, 0x0ab6, 0x144a, 0x0e3d, 0x17d1, 0x1246, 0x0cba, 0x15cd, 0x10c3,  # 2021 ~ 2030
    0x0b37, 0x14cb, 0x0f3f, 0x18d3, 0x1348, 0x0dbc, 0x16cf, 0x1144, 0x0bb8, 0x154c,  # 2031 ~ 2040
    0x0fc1, 0x0ab6, 0x144a, 0x0ebe, 0x17d1, 0x1246, 0x0cba, 0x164e, 0x1042, 0x0b37,  # 2041 ~ 2050
    0x14cb, 0x0fc1, 0x18d3, 0x1348, 0x0dbc, 0x16cf, 0x1144, 0x0a38, 0x154c, 0x1042,  # 2051 ~ 2060
    0x0a35, 0x13c9, 0x0e3d, 0x17d1, 0x11c5, 0x0cba, 0x164e, 0x10c3, 0x0b37, 0x14cb,  # 2061 ~ 2070
    0x0f3f, 0x18d3, 0x12c7, 0x0d3b, 0x16cf, 0x11c5, 0x0bb8, 0x154c, 0x1042, 0x0ab6,  # 2071 ~ 2080
    0x13c9, 0x0e3d, 0x17d1, 0x1246, 0x0cba, 0x164e, 0x10c3, 0x0bb8, 0x144a, 0x0ebe,  # 2081 ~ 2090
    0x1852, 0x12c7, 0x0d3b, 0x16cf, 0x11c5, 0x0c39, 0x154c, 0x0fc1, 0x0a35, 0x13c9,  # 2091 ~ 2100
]

# ==================================================================================

from datetime import date, datetime, timedelta
from yangke.web.webQA import *
import re
import sxtwl

# 开始年份
START_YEAR = 1901

month_DAY_BIT = 12
month_NUM_BIT = 13

# 　todo：正月初一 == 春节   腊月二十九/三十 == 除夕
yuefeng = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "冬月", "腊月"]
riqi = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
        "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "廿十",
        "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]

xingqi = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
shengxiao = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

sFtv = [  # 阳历节日 * 表示国家法定假日
    "0101#元旦节#*",
    "0202#世界湿地日#",
    "0210#国际气象节#",
    "0214#情人节#",
    "0301#国际海豹日#",
    "0303#全国爱耳日#",
    "0305#学雷锋纪念日#",
    "0308#妇女节#",
    "0312#植树节# #孙中山逝世纪念日#",
    "0314#国际警察日#",
    "0315#消费者权益日#",
    "0317#中国国医节# #国际航海日#",
    "0321#世界森林日# #消除种族歧视国际日# #世界儿歌日#",
    "0322#世界水日#",
    "0323#世界气象日#",
    "0324#世界防治结核病日#",
    "0325#全国中小学生安全教育日#",
    "0330#巴勒斯坦国土日#",
    "0401#愚人节# #全国爱国卫生运动月(四月)# #税收宣传月(四月)#",
    "0404/0405/0406#清明节#<谷雨>+15*",  # 虽为农历的节气，但每年必然是这三天之一，谷雨后的第15天
    "0407#世界卫生日#",
    "0422#世界地球日#",
    "0423#世界图书和版权日#",
    "0424#亚非新闻工作者日#",
    "0501#劳动节#*",
    "0504#青年节#",
    "0505#碘缺乏病防治日#",
    "0508#世界红十字日#",
    "0512#国际护士节#",
    "0515#国际家庭日#",
    "0517#国际电信日#",
    "0518#国际博物馆日#",
    "0520#全国学生营养日#",
    "0523#国际牛奶日#",
    "0531#世界无烟日#",
    "0601#国际儿童节#",
    "0605#世界环境保护日#",
    "0606#全国爱眼日#",
    "0617#防治荒漠化和干旱日#",
    "0623#国际奥林匹克日#",
    "0625#全国土地日#",
    "0626#国际禁毒日#",
    "0701#中国共·产党诞辰# #香港回归纪念日# #世界建筑日#",
    "0702#国际体育记者日#",
    "0707#抗日战争纪念日#",
    "0711#世界人口日#",
    "0730#非洲妇女日#",
    "0801#建军节#",
    "0808#中国男子节(爸爸节)#",
    "0815#抗日战争胜利纪念#",
    "0908#国际扫盲日# #国际新闻工作者日#",
    "0909#毛·泽东逝世纪念#",
    "0910#中国教师节#",
    "0914#世界清洁地球日#",
    "0916#国际臭氧层保护日#",
    "0918#九·一八事变纪念日#",
    "0920#国际爱牙日#",
    "0927#世界旅游日#",
    "0928#孔子诞辰#",
    "1001#国庆节# #世界音乐日# #国际老人节#*",
    "1002#国庆节假日# #国际和平与民主自由斗争日#",
    "1003#国庆节假日#",
    "1004#世界动物日#",
    "1006#老人节#",
    "1008#全国高血压日# #世界视觉日#",
    "1009#世界邮政日# #万国邮联日#",
    "1010#辛亥革命纪念日# #世界精神卫生日#",
    "1013#世界保健日# #国际教师节#",
    "1014#世界标准日#",
    "1015#国际盲人节(白手杖节)#",
    "1016#世界粮食日#",
    "1017#世界消除贫困日#",
    "1022#世界传统医药日#",
    "1024#联合国日#",
    "1031#世界勤俭日#",
    "1107#十月社会主义革命纪念日#",
    "1108#中国记者日#",
    "1109#全国消防安全宣传教育日#",
    "1110#世界青年节#",
    "1111#国际科学与和平周(本日所属的一周)#",
    "1112#孙中山诞辰纪念日#",
    "1114#世界糖尿病日#",
    "1116#国际宽容日#",
    "1117#国际大学生节# #世界学生节#",
    "1120#彝族年#",
    "1121#彝族年# #世界问候日# #世界电视日#",
    "1122#彝族年#",
    "1129#国际声援巴勒斯坦人民国际日#",
    "1201#世界艾滋病日#",
    "1203#世界残疾人日#",
    "1205#国际经济和社会发展志愿人员日#",
    "1208#国际儿童电视日#",
    "1209#世界足球日#",
    "1210#世界人权日#",
    "1212#西安事变纪念日#",
    "1213#南京大屠杀(1937年)纪念日#",
    "1220#澳门回归纪念#",
    "1221#国际篮球日#",
    "1224#平安夜#",
    "1225#圣诞节#",
    "1226#毛·泽东诞辰纪念日#"
]

lFtv = [  # 农历节日
    "0101#春节#*",
    "0115#元宵节#",
    "0202#春龙节",
    # "0314#清明节#", #每年不一样，此为2012年，事实上为公历节日
    "0505#端午节#*",
    "0707#七夕情人节#",
    "0715#中元节#",
    "0815#中秋节#*",
    "0909#重阳节#",
    "1208#腊八节#",
    "1223#小年#",
    "1229/1230#除夕#"  # 每年不一样，可能是1229或1230，但一定是岁末最后一天，即春节前一天
]


def change_year(num):
    dx = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    tmp_str = ""
    # 将年份 转换为字符串，然后进行遍历字符串 ，将字符串中的数字转换为中文数字
    for i in str(num):
        tmp_str += dx[int(i)]
    return tmp_str


# 获取星期
def week_str(tm):
    return xingqi[tm.weekday()]


# 获取天数
def lunar_day(day):
    return riqi[(day - 1) % 30]


def lunar_day1(month, day):
    if day == 1:
        return lunar_month(month)
    else:
        return riqi[day - 1]


# 判断是否是闰月
def lunar_month(month):
    leap = (month >> 4) & 0xf
    m = month & 0xf
    month = yuefeng[(m - 1) % 12]
    if leap == m:
        month = "闰" + month
    return month


# 求什么年份，中国农历的年份和 什么生肖年
def lunar_year(year):
    return tiangan[(year - 4) % 10] + dizhi[(year - 4) % 12] + '[' + shengxiao[(year - 4) % 12] + ']'


# 返回：
# a b c
# 闰几月，该闰月多少天 传入月份多少天
def lunar_month_days(lunar_year, lunar_month):
    if (lunar_year < START_YEAR):
        return 30

    leap_month, leap_day, month_day = 0, 0, 0  # 闰几月，该月多少天 传入月份多少天

    tmp = g_lunar_month_day[lunar_year - START_YEAR]

    if tmp & (1 << (lunar_month - 1)):
        month_day = 30
    else:
        month_day = 29

        # 闰月
    leap_month = (tmp >> month_NUM_BIT) & 0xf
    if leap_month:
        if (tmp & (1 << month_DAY_BIT)):
            leap_day = 30
        else:
            leap_day = 29

    return (leap_month, leap_day, month_day)


# 算农历日期
# 返回的月份中，高4bit为闰月月份，低4bit为其它正常月份
def get_ludar_date(tm):
    year, month, day = tm.year, 1, 1
    code_data = g_lunar_year_day[year - START_YEAR]
    days_tmp = (code_data >> 7) & 0x3f
    chunjie_d = (code_data >> 0) & 0x1f
    chunjie_m = (code_data >> 5) & 0x3
    span_days = (tm - datetime(year, chunjie_m, chunjie_d)).days
    # print("span_day: ", days_tmp, span_days, chunjie_m, chunjie_d)

    # 日期在该年农历之后
    if (span_days >= 0):
        (leap_month, foo, tmp) = lunar_month_days(year, month)
        while span_days >= tmp:
            span_days -= tmp
            if (month == leap_month):
                (leap_month, tmp, foo) = lunar_month_days(year, month)  # 注：tmp变为闰月日数
                if (span_days < tmp):  # 指定日期在闰月中
                    month = (leap_month << 4) | month
                    break
                span_days -= tmp
            month += 1  # 此处累加得到当前是第几个月
            (leap_month, foo, tmp) = lunar_month_days(year, month)
        day += span_days
        return year, month, day
        # 倒算日历
    else:
        month = 12
        year -= 1
        (leap_month, foo, tmp) = lunar_month_days(year, month)
        while abs(span_days) >= tmp:
            span_days += tmp
            month -= 1
            if (month == leap_month):
                (leap_month, tmp, foo) = lunar_month_days(year, month)
                if (abs(span_days) < tmp):  # 指定日期在闰月中
                    month = (leap_month << 4) | month
                    break
                span_days += tmp
            (leap_month, foo, tmp) = lunar_month_days(year, month)
        day += (tmp + span_days)  # 从月份总数中倒扣 得到天数
        return year, month, day


# 打印 某个时间的农历
def _show_month(tm):
    (year, month, day) = get_ludar_date(tm)
    print("%d年%d月%d日" % (tm.year, tm.month, tm.day), week_str(tm), end='')
    print("\t农历 %s年 %s年%s%s " % (lunar_year(year), change_year(year), lunar_month(month), lunar_day(day)))  # 根据数组索引确定
    return lunar_year(year), change_year(year), lunar_month(month), lunar_day(day)


# 判断输入的数据是否符合规则
def show_month(day_datetime: datetime.date = date.today()):
    """
    返回指定的年月日的农历日期

    :param day_datetime
    :return:
    """
    if day_datetime.year > 2100 or day_datetime.year < 1901:
        return
    if day_datetime.month > 13 or day_datetime.month < 1:
        return

    tmp = datetime(day_datetime.year, day_datetime.month, day_datetime.day)
    lu_year, ch_year, lu_month, lu_day = _show_month(tmp)
    return lu_year, ch_year, lu_month, lu_day


def _is_holiday(day_datetime: datetime.date = date.today(), ftv_type='solar') -> (bool, int):
    """
    判断是否是法定 节假日，只有法定放假的节日才返回True。
    法定假日有：
    元旦节 -> 阳历1月1日
    春节 -> 阴历1月1日，由除夕开始放假，即阴历1月1日的前一天开始放假
    清明节 -> 阳历4月4日/4月5日/4月6日，每年不确定
    劳动节 -> 阳历5月1日
    端午节 -> 阴历5月5日
    中秋节 -> 阴历8月15日
    国庆节 -> 阳历10月1日

    :param day_datetime: 需要查询的日期
    :param ftv_type: 节日类型，分为阳历节日和阴历日期，分别取值'solar', 'lunar'
    :return: 是否节假日，置信度
    """
    result = False
    confidence = 0
    md = f"{day_datetime.month:>02}{day_datetime.day:>02}"  # 右对齐，长度为2，不足则在左边补0
    ftv_spe = sFtv if ftv_type == 'solar' else lFtv
    for item in ftv_spe:
        if '*' not in item:  # 如果该节日不是假期，则直接忽略该节日
            continue
        ftv = item.split("#")[0]  # 获取节日的日期
        if '/' in ftv:  # 说明节日日期不确定，例如清明节，母亲节等，因为这些不定节日中只有清明节是法定假日，这里只需判断清明节
            ds = ftv.split('/')
            if md in ds:
                # 说明可能是假日，继续判断是否是节日，清明节的日期不定
                if item.split("#")[1] == "清明节":
                    ques = f'{day_datetime.year}年{item.split("#")[1]}是几月几号？'  # 这里直接询问百度机器人
                    ans = ask_baidu(ques)[0]
                    ans = re.findall(".*(.)月(.)日.*", ans)[0]  # 正则表达式匹配"月"和"日"之前的字符
                    print(ans)
                    if md == f"{ans[0]:>02}{ans[1]:>02}":
                        result = True
                        confidence = 0.8
                        break
            else:
                result = False
                confidence = 1
        else:
            if md == ftv:  # 日期==节日日期
                result = True
                confidence = 1
                break

    return result, confidence


def is_holiday(day_datetime: datetime.date = date.today()) -> (bool, str):
    """
    判断日期是否是国家法定假日

    :param day_datetime: 日期
    :return: (bool, str) 是否假日，判断依据-可靠度
    """
    if _is_holiday(day_datetime, 'solar')[0] or _is_holiday(day_datetime, 'lunar')[0]:
        return True
    else:
        return False


def get_qingming(year: int):
    """
    获得指定年份清明节的日期，year的取值范围为1990年到2099年，超范围本算法不准确
    """
    qm = {'1990': '5', '1991': '5', '1992': '4', '1993': '5', '1994': '5', '1995': '5', '1996': '4',
          '1997': '5', '1998': '5', '1999': '5', '2000': '4', '2001': '5', '2002': '5', '2003': '5',
          '2004': '4', '2005': '5', '2006': '5', '2007': '5', '2008': '4', '2009': '4', '2010': '5',
          '2011': '5', '2012': '4', '2013': '4', '2014': '5', '2015': '5', '2016': '4', '2017': '4',
          '2018': '5', '2019': '5', '2020': '4', '2021': '4', '2022': '5', '2023': '5', '2024': '4',
          '2025': '4', '2026': '5', '2027': '5', '2028': '4', '2029': '4', '2030': '5', '2031': '5',
          '2032': '4', '2033': '4', '2034': '5', '2035': '5', '2036': '4', '2037': '4', '2038': '5',
          '2039': '5', '2040': '4', '2041': '4', '2042': '4', '2043': '5', '2044': '4', '2045': '4',
          '2046': '4', '2047': '5', '2048': '4', '2049': '4', '2050': '4', '2051': '5', '2052': '4',
          '2053': '4', '2054': '4', '2055': '5', '2056': '4', '2057': '4', '2058': '4', '2059': '5',
          '2060': '4', '2061': '4', '2062': '4', '2063': '5', '2064': '4', '2065': '4', '2066': '4',
          '2067': '5', '2068': '4', '2069': '4', '2070': '4', '2071': '5', '2072': '4', '2073': '4',
          '2074': '4', '2075': '4', '2076': '4', '2077': '4', '2078': '4', '2079': '4', '2080': '4',
          '2081': '4', '2082': '4', '2083': '4', '2084': '4', '2085': '4', '2086': '4', '2087': '4',
          '2088': '4', '2089': '4', '2090': '4', '2091': '4', '2092': '4', '2093': '4', '2094': '4',
          '2095': '4', '2096': '4', '2097': '4', '2098': '4', '2099': '4'}
    # qm字典数据的获得方法：
    """
    import re
    qingming_dict = {}
    for year in range(1990, 2100):
        ans = ask_baidu(f'{year}年清明节是几月几号')[0]
        ans = re.findall(".*月(.)日.*", ans)
        while len(ans) == 0:
            ans = ask_baidu(f'{year}年清明节是几月几号')[0]
            ans = re.findall(".*月(.)日.*", ans)
        qingming_dict[str(year)] = ans[0]
    print(qingming_dict)  # 即qm
    """
    return datetime(year, 4, int(qm[str(year)]))


def get_solar_date(year, month, day) -> datetime:
    """
    根据农历日期获得阳历日期

    :param year:
    :param month:
    :param day:
    :return:
    """
    lunar1 = sxtwl.Lunar()
    date_solar = lunar1.getDayByLunar(year=year, month=month, day=day, isRun=False)  # isRun表示是否是闰月
    return datetime(date_solar.y, date_solar.m, date_solar.d)


def generate_stock_holiday_table(start_day=datetime(2015, 1, 1), days=7300, file='holiday.csv'):
    """
    生成股市是否开盘的csv数据表格。以下法定假日休市（2014年1月1日起施行）：
    （一）元旦，放假1天(1月1日)；
    （二）春节，放假3天(农历正月初一、初二、初三)；
    （三）清明节，放假1天(农历清明当日)；
    （四）劳动节，放假1天(5月1日)；
    （五）端午节，放假1天(农历端午当日)；
    （六）中秋节，放假1天(农历中秋当日)；
    （七）国庆节，放假3天(10月1日、2日、3日)。

    额外假期：
    2015年9月3日、9月4日，纪念抗战胜利70周年，法定休假1天调休1天，股市休市

    注：2028、2039、2047有闰五月，不知道会不会导致端午判断有问题
    下一个闰八月在2052年，暂时不会导致中秋节有问题
    下一个闰正月在2262年，与我们没有关系

    :param start_day: 从指定日期开始计算，起始日期不能早于2014年（可以等于2014），因为最新的法定放假政策从2014年开始实行
    :param days: 生成多少天的数据
    :param file: 生成的休市日期信息保存到文件file中，isOpen=1是开市，0是休市
    """
    isOpen = {}
    for i in range(days):
        day_datetime = start_day + timedelta(days=i)
        day_str = f"{day_datetime.year}/{day_datetime.month}/{day_datetime.day}"
        if day_datetime.weekday() == 5 or day_datetime.weekday() == 6:
            # 如果是星期六或者星期日，则先初始化为休市日
            isOpen[day_str] = False
        else:
            # 否则，先初始化为交易日
            isOpen[day_str] = True
    # 循环每一年
    for year in range(start_day.year, (start_day + timedelta(days=days)).year + 1):
        # 元旦节，劳动，端午，中秋，清明，均法定放假一天。这里不能算国庆节，因为国庆节放三天
        holidays = [datetime(year, 1, 1), datetime(year, 5, 1),  # datetime(year, 10, 1),
                    get_solar_date(year, 5, 5), get_solar_date(year, 8, 15),
                    get_qingming(year)]

        for select_holiday in holidays:
            weekday = select_holiday.weekday()
            # 1.如果在星期六，日，则在下一个星期一补休；
            if weekday == 5:
                holiday_datetime = [select_holiday + timedelta(days=2)]
            elif weekday == 6:
                # 例外：2015年中秋在周日，没有调休，只放假了两天
                if select_holiday == datetime(2015, 9, 27):
                    holiday_datetime = []
                else:
                    holiday_datetime = [select_holiday + timedelta(days=1)]
            # 2. 如果在星期一，五，则正常休假
            elif weekday == 0 or weekday == 4:
                holiday_datetime = [select_holiday]
            # 3. 如果在星期二，四，则分别将前一个星期六、后一个星期日调整到星期一、星期五
            elif weekday == 1:  # 因为调休的周六周日无论如何都休市，所以，这里只需要把星期一改成休市即可
                holiday_datetime = [select_holiday, select_holiday - timedelta(days=1)]
            elif weekday == 3:
                holiday_datetime = [select_holiday, select_holiday + timedelta(days=1)]
            # 4. 如果在星期三，则不调休
            # 例外：2019年劳动节是星期三，放假放的是345。
            elif weekday == 2:
                if select_holiday == datetime(2019, 5, 1):
                    holiday_datetime = [select_holiday, select_holiday + timedelta(days=1),
                                        select_holiday + timedelta(days=2)]
                else:  # 2020.1.1
                    holiday_datetime = [select_holiday]
            else:
                raise Exception("星期判断失败！")
            for day_datetime in holiday_datetime:
                day_str1 = f"{day_datetime.year}/{day_datetime.month}/{day_datetime.day}"
                isOpen[day_str1] = False
        # 国庆，将国庆所在的周从星期日到星期六放假、前后的星期六、日工作（来自百度文库，但是是错误的）
        # 根据2018、2019、2020年国庆放假规律，是10.1-10.7放假7天，多放的天数在前后两个星期内调休
        holiday_datetime = [datetime(year, 10, 1) + timedelta(days=i) for i in range(7)]
        if get_solar_date(year, 8, 15) in holiday_datetime:  # 如果中秋在国庆假期里，则10月8日再休一个天，例如2017和2020年
            holiday_datetime.append(datetime(year, 10, 8))
        for day_datetime in holiday_datetime:
            day_str2 = f"{day_datetime.year}/{day_datetime.month}/{day_datetime.day}"
            isOpen[day_str2] = False
        # 春节，百度文库的放假规律也是错误的
        # 根据2017、2018、2019年春节的放假规律，是除夕开始放假7天，2020年因为新冠疫情原因例外
        select_holiday = get_solar_date(year, 1, 1)
        if select_holiday.year == 2014:  # 2014年是从春节开始放假
            holiday_datetime = [select_holiday + timedelta(days=i) for i in range(7)]
        elif select_holiday.year >= 2015:
            holiday_datetime = [select_holiday + timedelta(days=i - 1) for i in range(7)]
        for day_datetime in holiday_datetime:
            day_str = f"{day_datetime.year}/{day_datetime.month}/{day_datetime.day}"
            isOpen[day_str] = False
    # ============================================== 例外情况 ======================================================
    # 2020年1月31日原计划正常开市，因为疫情原因休市未开，2月3日正常开市
    # 2020年5月4日和5月5日调休了两天
    if start_day.year < 2020 < (start_day + timedelta(days=days)).year + 1:
        isOpen['2020/1/31'] = False
        isOpen['2020/5/4'] = False
        isOpen['2020/5/5'] = False

    # 将holiday_dict写入csv文件
    # 将isOpen的值转为整形，方便存储
    for k, v in isOpen.items():
        if isOpen[k]:
            isOpen[k] = 1
        else:
            isOpen[k] = 0
    import pandas as pd

    df_holiday = pd.DataFrame.from_dict({"date": list(isOpen.keys()), "isOpen": list(isOpen.values())})

    df_holiday.to_csv(file, index=False)


if __name__ == '__main__':
    show_month()
    generate_stock_holiday_table()
