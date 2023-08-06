# 2022.6.3  python -m pipe uvirun 8180       http://{gechost}:8180/gecv1,  json=snts =>  sntdic 
import fastapi,uvicorn, fire,json

def redis_getgecs(snts:list=["She has ready.","It are ok."], xname:str='xsnts', host:str="172.17.0.1", port:int=6379, db:int=0, timeout:int=5): # put into the ufw white ip list 
	''' snts -> gecs '''
	import redis
	try:
		if not hasattr(redis, 'r'): redis.r = redis.Redis(host=host,port=port, db=db, decode_responses=True)
		id  = redis.r.xadd(xname, {"snts":json.dumps(snts)})
		res	= redis.r.blpop([f"suc:{id}",f"err:{id}"], timeout=timeout)
		return {} if res is None else json.loads(res[1])
	except Exception as e:
		print ("redis_getgecs ex:", e, snts) 
		return {}

def uvirun(port): 
	''' python -m pipe uvirun 8180 '''
	import pipe
	app	= fastapi.FastAPI()

	@app.get('/')
	def home():  return fastapi.responses.HTMLResponse(content=f"<h2> localgec  </h2><a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br>last update: 2022.6.3")

	@app.post('/gecv1')
	def gecv1(snts:list=["She has ready.","It are ok."] , xname:str='xsnts', host:str="172.17.0.1", port:int=6379, db:int=0, timeout:int=5
			,  max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5, model:str="/grammar_error_correcter_v1", device:int=-1):
		''' a simple wrapper of gecsnt, 2022.6.3 '''
		if not snts: return {} 
		sntdic = redis_getgecs(snts, xname=xname, host=host, port=port, db=db, timeout=timeout )
		if not sntdic :  # failed , call the local version as backoff
			return pipe.gecsnts(snts, max_length=max_length,do_sample=do_sample, batch_size =batch_size, unchanged_ratio=unchanged_ratio, len_ratio = len_ratio, model =model, device=device)

	uvicorn.run(app, host='0.0.0.0', port=port)

if __name__ == '__main__':  #{'She has ready.': 'She is ready.', 'It are ok.': 'It is ok.'}
	fire.Fire({"uvirun":uvirun, "testredis": lambda : print(redis_getgecs()), 'testlocal': lambda: print(pipe.gecsnts())}) 

'''
			return pipe.gecsnts(snts, max_length=arr.get('max_length', 128),do_sample=arr.get('do_sample', False), 
				batch_size = arr.get('batch_size', 64), unchanged_ratio=arr.get('unchanged_ratio', 0.45), 
				len_ratio = arr.get('len_ratio', 0.5), model=arr.get('model',"/grammar_error_correcter_v1"), device=arr.get('device',-1))
'''