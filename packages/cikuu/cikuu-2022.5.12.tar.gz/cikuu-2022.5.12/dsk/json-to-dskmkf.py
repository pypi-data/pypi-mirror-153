# 22-5-29
import json, sys, time, fire,traceback, requests,os
import dsk,util

sample = {"id": 683598558, "essay_id": 123435663, "request_id": 2204638, "author_id": 297, "internal_idx": 0, "title": "\u7b2c2204638\u53f7 \u4f5c\u6587", "essay": "The speed of development of technology and science is beyond our imagination. Smartphones spread all over the world only take a few years. Without doubt, Smartphones have already made a big change to our daily life. On the one hand, they bring convenience to us, making us can do more things than before during the same period of time.On the other hand, we waste too much time on smartphones everyday. It does harm to not only our physical health, but also our mental health. \n In recent years, more and more people are in the charge of smartphones.They can't control themselves seeing a smartphone whenever they have nothing to do. There is no denying that more than half people are dropped in a cage called virtual world.In this cage, our mental withstand large quantities of damage inadvertently. What's worse, we can't realize the cage, not to mention fleeing it. \n Smartphones are just tools. We shouldn't be addicted in them, still less let them lead our life.", "essay_html": "", "tm": "", "user_id": 24126239, "sent_cnt": 0, "token_cnt": 0, "len": 966, "ctime": 1603093018, "stu_number": "2020210018", "stu_name": "\u5b8b\u777f", "stu_class": "A2122-2020\u79cb\u5b63\u5b66\u671f", "type": 0, "score": 76.4888, "qw_score": 75.9687, "sy_score": 0.0, "pigai": "", "pigai_time": 0, "gram_score": 0.0, "is_pigai": 1, "version": 8, "cate": 0, "src": "ajax_postSave__", "tid": 0, "fid": 0, "tag": "", "is_chang": 0, "jianyi": "", "anly_cnt": 1, "mp3": ""}

def json_to_dskmkf(infile, host='192.168.121.3',port=3306,user='root',password='cikuutest!',db='dskmkf'
				, dskhost:str='gpu120.wrask.com:7095', gechost:str='gpu120.wrask.com:8180'):  
	''' parse bupt.json -> dskmkf , 2022.5.28 | python __main__.py json_to_dskmkf  2491939.json '''
	import pymysql
	conn = pymysql.connect(host=host,port=port,user=user,password=password,db=db)
	cursor= conn.cursor()
	for line in open(infile, 'r').readlines(): #util.readline(infile) :
		try:
			start = time.time() 
			arr = json.loads(line)
			essay = arr.get("essay", "") 
			if not essay: continue 

			res = dsk.todsk(essay, dskhost=dskhost) #, gechost=gechost
			res['info'].update({"essay_id": arr.get("essay_id", 0), "rid": arr.get("request_id", 0), "uid": arr.get("user_id",0), "e_version": arr.get("version",0) })
			dsk.submit_dskmkf(res, cursor)	 
			conn.commit()

			print (type(res), " id:", arr['id'] , "  eid:", arr['essay_id'], "\t timing:" , time.time() - start , flush=True) 
		except Exception as ex: 
			print(">>line Ex:", ex, "\t|", line) #>>line Ex: 'NoneType' object is not subscriptable
			exc_type, exc_value, exc_traceback_obj = sys.exc_info()
			traceback.print_tb(exc_traceback_obj)
	print("finished parsing:", infile)
	
if __name__ == '__main__': 
	fire.Fire(json_to_dskmkf) 
