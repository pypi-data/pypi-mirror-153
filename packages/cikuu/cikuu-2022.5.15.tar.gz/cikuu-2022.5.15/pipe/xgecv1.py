# 2022.6.3  python -m pipe.xgecv1 gecv1 || cp from pypi/dsk/xgecv1.py   # 2022.4.5 upgrade of xsnt-gecv1.py 
import json, time, fire,sys, redis, socket, os,math, torch,traceback, pipe
now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))

def local_gecsnts(snts:list=["She has ready.","It are ok."],  arr:dict={}):
	return pipe.gecsnts(snts, max_length=arr.get('max_length', 128),do_sample=arr.get('do_sample', False), 
				batch_size = arr.get('batch_size', 64), unchanged_ratio=arr.get('unchanged_ratio', 0.45), 
				len_ratio = arr.get('len_ratio', 0.5), model=arr.get('model',"/grammar_error_correcter_v1"), device=redis.cuda)

def process_xsnt(messages): #[('1648947215933-0', {'snt': 'hello'}), ('1648947215933-1', {'2': '2'}),
	''' to prefill the cache  '''
	try:
		snts	= [arr.get('snt','') for id,arr in messages] #[['xsnt', [('1648947215933-0', {'snt': '1'}), ('1648947215933-1', {'2': '2'}), ('1648947215934-0', {'3': '3'}), ('1648947215934-1', {'4': '4'}), ('1648947215934-2', {'5': '5'}), ('1648947215935-0', {'6': '6'}), ('1648947215935-1', {'7': '7'}), ('1648947215935-2', {'8': '8'}), ('1648947215936-0', {'9': '9'})]]]
		newsnts = [snt for snt in snts if snt and not redis.r.exists(f"gec:{snt}") ]
		if newsnts: 
			sntdic	= local_gecsnts(newsnts)   # arr
			[redis.r.setex(f"gec:{snt}", redis.ttl, gec) for snt, gec in sntdic.items()]
	except Exception as e:
		print(">>[process_xsnt ex]", e, "\t|", messages, "\t|",  now())
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)

def process_xsnts(messages): #[('1648947215933-0', {'snts': '1'}), ('1648947215933-1', {'2': '2'}),
	''' id = xadd('xsnts',  {"snts":["hello"]}),  blpop(id) , 2022.4.3'''
	for id,arr in messages:
		try:
			snts	= json.loads(arr.get('snts','[]'))
			gecs	= redis.r.mget([ f"gec:{snt}" for snt in snts])
			newsnts = [snt for snt, gec in zip(snts, gecs) if snt and gec is None ]
			sntdic	= local_gecsnts(newsnts, arr) if newsnts else {}
			res		= { snt: gec if gec is not None else sntdic.get(snt,snt) for snt, gec in zip(snts, gecs)}
			redis.r.lpush(f"suc:{id}", json.dumps(res) )
			redis.r.expire(f"suc:{id}", redis.ttl) 
		except Exception as e:
			print ("parse err:", e, id, arr) 
			redis.r.lpush(f"err:{id}", json.dumps(arr))
			redis.r.expire(f"err:{id}", redis.ttl) 
			redis.r.setex(f"exception:{id}", redis.ttl, str(e))

def xcreate(stream, group):
	try:
		redis.r.xgroup_create(stream, group,  mkstream=True)
	except Exception as e:
		print(e, stream, group)

def consume(group, xsnt="xsnt", xsnts="xsnts", host='172.17.0.1', port=6379, db=0, cuda:int=-1, maxlen=100000, waitms=3600000, ttl=27200, precount=64, debug=False):
	''' python xgecv1.py gecv1  | python -m pipe.xgecv1 gecv1 '''
	redis.r		= redis.Redis(host=host, port=port, db=db, decode_responses=True) 
	redis.ttl	= ttl
	redis.cuda	= cuda

	[ xcreate(name, group) for name in (xsnt, xsnts) ]
	[ redis.r.xtrim(name, maxlen) for name in (xsnt, xsnts) ]

	consumer_name = f'consumer_{socket.gethostname()}_{os.getpid()}'
	print(f"Redis consumer started: {consumer_name}|{group}| ", redis.r, "\n", now(), flush=True)
	while True:
		item = redis.r.xreadgroup(group, consumer_name, {xsnt: '>', xsnts: '>'}, count=precount, noack=True, block= waitms )
		if not item: break #[['xsnt', [('1648947215933-0', {'snt': '1'}), ('1648947215933-1', {'2': '2'}), ('1648947215934-0', {'3': '3'}), ('1648947215934-1', {'4': '4'}), ('1648947215934-2', {'5': '5'}), ('1648947215935-0', {'6': '6'}), ('1648947215935-1', {'7': '7'}), ('1648947215935-2', {'8': '8'}), ('1648947215936-0', {'9': '9'})]]]
		if debug: print( item, "\t", now(), flush=True) 
		for arr in item:  #['xsnt', [('1648947215933-0', {'snt': '1'}),
			if arr[0] == xsnt : 
				process_xsnt(arr[1]) 
			elif arr[0] == xsnts : 
				process_xsnts(arr[1]) 

	redis.r.xgroup_delconsumer(xsnt, group, consumer_name)
	redis.r.xgroup_delconsumer(xsnts, group, consumer_name)
	redis.r.close()
	print ("Quitted:", consumer_name, "\t",now())

def test_xsnt(snt:str="She has ready.", host='172.17.0.1', port=6379, db=0, span:int=5): 
	''' test xsnt/ prefill cache , snt -> gec:{snt} '''
	r	= redis.Redis(host=host, port=port, db=db, decode_responses=True) 
	r.delete(f"gec:{snt}") 
	id = r.xadd("xsnt", {"snt": snt})
	time.sleep(span) 
	print (id, "\t|", r.get(f"gec:{snt}") )

def test_xsnts(snts:list=["She has ready.","It are ok."], host='172.17.0.1', port=6379, db=0, timeout:int=3): 
	''' test xsnts /blpop,   snts -> sntdic {src:tgt} '''
	r	= redis.Redis(host=host, port=port, db=db, decode_responses=True) 
	start = time.time()
	id = r.xadd("xsnts", {"snts": json.dumps(snts)})
	res = r.blpop(f"suc:{id}")
	print (id, "\t|blpop:", res , "\ttiming:", time.time() - start)

if __name__ == '__main__':
	fire.Fire({"consume":consume, "test_xsnt": test_xsnt, "test_xsnts":test_xsnts})

'''
>>> id = r.xadd('xsnts', {"snts":json.dumps(["She has ready."])})
>>> id
'1648958192091-0'
>>> r.blpop(["suc:1648958192091-0"])
('suc:1648958192091-0', '{"She has ready.": "She is ready."}')

ubuntu@essaydm:/data/cikuu/pypi/pipe$ python xgecv1.py  test_xsnts
1654330680117-0 	|blpop: ('suc:1654330680117-0', '{"She has ready.": "She is ready.", "It are ok.": "It is ok."}') 	timing: 2.0551092624664307
ubuntu@essaydm:/data/cikuu/pypi/pipe$ python xgecv1.py  test_xsnts
1654330684961-0 	|blpop: ('suc:1654330684961-0', '{"She has ready.": "She is ready.", "It are ok.": "It is ok."}') 	timing: 2.0699944496154785
ubuntu@essaydm:/data/cikuu/pypi/pipe$ python xgecv1.py  test_xsnt
1654330690136-0 	| She is ready.
ubuntu@essaydm:/data/cikuu/pypi/pipe$ python xgecv1.py  test_xsnt
1654330703268-0 	| She is ready.
ubuntu@essaydm:/data/cikuu/pypi/pipe$ python xgecv1.py  test_xsnt --span 3
1654330715306-0 	| She is ready.
ubuntu@essaydm:/data/cikuu/pypi/pipe$ python xgecv1.py  test_xsnt --span 2
1654330775146-0 	| She is ready.
ubuntu@essaydm:/data/cikuu/pypi/pipe$ python xgecv1.py  test_xsnt --span 1
1654330779258-0 	| None

setup : 
1. pip install cikuu --upgrade
2. python3 -m pipe.xgecv1 consume gecv1 --port 6311  --debug true (put into xgecv1.conf, or docker ) 
3. 
python3 -m pipe.xgecv1 test_xsnt --port 6311
python3 -m pipe.xgecv1 test_xsnts --port 6311

4. start redisgec8180.py 
python3 -m pipe.redisgec8180 8181 --port 6311
sudo ufw allow 8180 

5. gears-cli run xsntbytes.py --host 172.17.0.1 --port 6311

'''