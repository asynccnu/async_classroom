import os
import xlrd
import asyncio
import  copy


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
        print(i,'7')
        one = {
            'bno' : '7',
            'weekNo' : 'week' + str(i),
        }
        one = dict(one,**one_week_7)
        res = await weekdaydb.find_one(one)
        if res is None:
            weekdaydb.insert_one(one)

    for i in range(1,19) :
        print(i,'8')
        one = {
            'bno' : '8',
            'weekNo' : 'week' + str(i),
        }
        one = dict(one, **one_week_8)
        res = await weekdaydb.find_one(one)
        if res is None:
            weekdaydb.insert_one(one)


async def remove_from_sheets(sheet,s,e) :
    """
    讲起始页到结束页中的课读到mongodb 中
    :param sheet: Excel表格的所有页
    :param s: 起始页
    :param e: 结束页
    :return: None
    """
    for each_sheet in sheet[s:e] :
        await remove_classroom(each_sheet)


async def remove_classroom(sheet) :
    """
    根据上课情况，在mongodb中删除不空闲的教室
    Excel表从第12列开始，分别是 时间1，地点1，时间2，地点2，时间3，地点3
    时间的格式为星期一第9-10节{1-15周(单)} 或 星期一第9-10节{1-15周} 或 星期一第9-10节{15周}
    地点只有符合 七号楼和八号楼的标准才算
    :param sheet: Excel 表格中的每个单页
    :return: None
    """
    rows = sheet.nrows
    day_dict = {'一':'mon','二':'tue','三':'wed','四':'thu','五':'fri',}
    print(rows)
    for i in range(1,rows) :
        print(i)
        val = sheet.row_values(i)
        for k in range(3) :
            if len(val[11+2*k]) == 0 :
                break
            when = val[11+2*k]
            where = val[11+2*k+1]
            # 忽略不符合要求的星期和教室
            if not isinstance(where,float) \
                    or str(int(where)) not in ALLROOM8+ALLROOM7 \
                    or day_dict.get(when[2]) is None :
                continue

            where = str(int(where))
            weekday = day_dict[when[2]]                     # 星期一到星期五
            index1 = when.index('第')
            index2 = when.index('节')
            time = when[index1+1:index2].split('-')
            for t in range(int(time[0])+1,int(time[1]))  :
                time.append(str(t))                      # time 是课的节数 如['11','12','13','14]

            week_list = list(int(i) for i in when[when.index('{') + 1:when.index(u'\u5468')].split('-'))
            week1 = week_list[0]
            if len(week_list) == 2 :
                week2 = week_list[1]
                if '单' in when :
                    weeks = list(str(item) for item in range(week1,week2+1) if item % 2 != 0 )
                elif '双' in when :
                    weeks = list(str(item) for item in range(week1,week2+1) if item % 2 == 0 )
                else :
                    weeks = list(str(item) for item in range(week1,week2+1) )
            else :                                               # 有些课是单周上的 格式为 （17周）
                weeks = list(str(item) for item in week_list)
                print(weeks)


            for week in weeks :
                for t in time :
                    res = await weekdaydb.find_one({'bno':where[0],'weekNo':'week'+week})
                    if res is not None :
                        cp = copy.deepcopy(res)
                       # print('cp',when,where,week,t,cp)
                        try :
                            cp[weekday][t].remove(where)                       # 删除这个教室
                            print(res==cp)
                            result = await weekdaydb.replace_one(res,cp)       # 代替原先的对象
                            print('matched %d, modified %d' %
                                (result.matched_count, result.modified_count))
                        except ValueError:                                     # 已经没有这个教室
                            continue


if __name__ == '__main__' :
    data = xlrd.open_workbook(Datafrom)
    data_sheets = data.sheets()
    loop.run_until_complete(init_week())
    loop.run_until_complete(remove_from_sheets(data_sheets,0,4))
