import os
import xlrd
import asyncio
from service.mongoDB import db_setup


loop = asyncio.get_event_loop()
weekdaydb = loop.run_until_complete(db_setup())
Datafrom = os.getenv('DATAFROM') or '选课手册.xls'

# 七号楼所有的教室
ALLROOM7 = [
        u'7101',u'7102',u'7103',u'7104',u'7105',u'7106',u'7107',u'7108',u'7109',
        u'7201',u'7202',u'7203',u'7204',u'7205',u'7206',u'7207',u'7208',u'7209',u'7211',
        u'7301',u'7302',u'7303',u'7304',u'7305',u'7306',u'7307',u'7308',u'7309',u'7311',
        u'7401',u'7402',u'7403',u'7404',u'7405',u'7406',u'7407',u'7408',u'7409',u'7410',u'7411',
        u'7501',u'7503',u'7505'
        ]

# 八号楼所有的教室
ALLROOM8 = [
        u'8101',u'8102',u'8103',u'8104',u'8105',u'8106',u'8107',u'8108',u'8109',
        u'8110',u'8111',u'8112',u'8201',u'8202',u'8203',u'8204',u'8205',u'8206',
        u'8207',u'8208',u'8209',u'8210',u'8211',u'8212',u'8213',u'8214',u'8215',
        u'8216',u'8301',u'8302',u'8303',u'8304',u'8305',u'8306',u'8307',u'8308',
        u'8309',u'8310',u'8311',u'8312',u'8313',u'8314',u'8315',u'8316',u'8401',
        u'8402',u'8403',u'8404',u'8405',u'8406',u'8407',u'8408',u'8409',u'8410',
        u'8411',u'8412',u'8413',u'8414',u'8415',u'8416',u'8501',u'8502',u'8503',
        u'8504',u'8505',u'8506',u'8507',u'8508',u'8509',u'8510',u'8511',u'8512',
        u'8513',u'8514',u'8515',u'8516',u'8716',u'8717'
        ]

async def init_week() :
    """
    将这栋楼的所有的教室初始化为空间教室 '7' 或 '8'
    :return:
    """
    day_list = ['mon','tue','wed','thu','fri']
    one_week_7 = {}
    one_week_8 = {}

    for day in day_list:
        one_week_7[day] = {}
        one_week_8[day] = {}
        for i in range(1,15) :
            one_week_7[day][str(i)] = ALLROOM7
            one_week_8[day][str(i)] = ALLROOM8


    for i in range(1,19) :
        one = {
            'bno' : '7',
            'weekNo' : 'week' + str(i),
        }
        one = dict(one,**one_week_7)
        res = await weekdaydb.find_one(one)
        if res is None:
            weekdaydb.insert_one(one)

    for i in range(1,19) :
        one = {
            'bno' : '8',
            'weekNo' : 'week' + str(i),
        }
        one = dict(one, **one_week_8)
        res = await weekdaydb.find_one(one)
        if res is None:
            weekdaydb.insert_one(one)


async def remove_classroom() :
    """
    根据上课情况，删除不空闲的教室
    :return:
    """


if __name__ == '__main__' :
    loop.run_until_complete(init_week())

