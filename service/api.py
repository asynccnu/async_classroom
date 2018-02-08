from aiohttp.web import Response, json_response, Application
from . import loop
from .mongoDB import db_setup

api = Application()
weekdaydb = loop.run_until_complete(db_setup())

async def get_classroom(request) :
	"""
	获取某周某天，7号楼或8号楼的空闲教室
	:param request: 请求
	:return:
	"""
	legal = ['weekno','weekday','building']                            # 这三个是必需的参数，不能多不能少
	reqs = request.rel_url.query_string
	if reqs is None :
		return Response(body=b'{"args-error": "null"}',
		                content_type='application/json', status=502)  # 没有URL参数

	args = {'weekno':'','weekday':'','building':''}
	for item in reqs.split('&'):
		tmp = item.split('=')
		if tmp[0] not in legal:
			return Response(body=b'{"args-error":"not such args"}',
			                content_type='appllication/json', status=502)  # URL参数错误
		args[tmp[0]] = tmp[1]
		legal.remove(tmp[0])

	if len(legal) != 0 :
		return Response(body=b'{"args-error":"not enough args"}',
						content_type='appllication/json', status=502)     # URL参数不全

	day_list = ['mon', 'tue', 'wed', 'thu', 'fri']
	if args['weekday'] not in day_list :
		return Response(body=b'{"args-error":"not such weekday"}',
		                content_type='appllication/json', status=502)  # URL参数错误

	try :
		res = await weekdaydb.find_one({'weekNo':'week'+args['weekno'],'bno':args['building']})
		return json_response(res[args['weekday']])
	except :
		return Response(body=b'{"args-error":"not weekNo or building"}',
		                content_type='appllication/json', status=502)  # URL参数不全


api.router.add_route('GET','/classroom/get_classroom/',get_classroom,name='get_classroom')
