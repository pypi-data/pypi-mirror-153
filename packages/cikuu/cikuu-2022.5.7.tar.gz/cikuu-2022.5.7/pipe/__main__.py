# 2022.6.3  python -m pipe uvirun 7085       http://{gechost}:7085/gecv1,  json=snts =>  sntdic 
import fastapi,uvicorn, fire,json, redis, pipe

def redis_getgecs(snts:list=["She has ready.","It are ok."], xname:str='xsnts', host:str="172.17.0.1", port:int=6379, db:int=0, timeout:int=5): # put into the ufw white ip list 
	''' snts -> gecs '''
	try:
		if not hasattr(redis, 'r'): redis.r = redis.Redis(host=host,port=port, db=db, decode_responses=True)
		id  = redis.r.xadd(xname, {"snts":json.dumps(snts)})
		res	= redis.r.blpop([f"suc:{id}",f"err:{id}"], timeout=timeout)
		return {} if res is None else json.loads(res[1])
	except Exception as e:
		print ("redis_getgecs ex:", e, snts) 
		return {}

def uvirun(port): 
	''' python -m pipe uvirun 7085 '''
	app	= fastapi.FastAPI()
	@app.post('/gecv1')
	def gecv1(snts:list=["She has ready.","It are ok."] , local:bool= False
			, xname:str='xsnts', host:str="172.17.0.1", port:int=6379, db:int=0, timeout:int=5
			, max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5, model:str="/grammar_error_correcter_v1", device:int=-1):
		''' main gec api, 1. redis_gec  2. when failed , call local_gec, 2022.6.3 '''
		if not snts: return {} 
		if local: return pipe.gecsnts(snts, max_length=max_length,do_sample=do_sample, batch_size =batch_size, unchanged_ratio=unchanged_ratio, len_ratio = len_ratio, model =model, device=device)

		sntdic = redis_getgecs(snts, xname=xname, host=host, port=port, db=db, timeout=timeout ) #
		if not sntdic :  # failed , call the local version as backoff
			sntdic = pipe.gecsnts(snts, max_length=max_length,do_sample=do_sample, batch_size =batch_size, unchanged_ratio=unchanged_ratio, len_ratio = len_ratio, model =model, device=device)
		return sntdic 

	@app.get('/')
	def home():  return fastapi.responses.HTMLResponse(content=f"<h2> gecsnts,  1. redis_gec  2. when failed, local_gec as the backoff  </h2><a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br>last update: 2022.6.3")

	@app.get('/redis/test_gecv1')
	def redis_gecv1(snts:str="She has ready.|It are ok.", xname:str='xsnts', host:str="172.17.0.1", port:int=6379, db:int=0, timeout:int=5):
		''' testing only, used by the health monitor '''
		return redis_getgecs(snts.split("|"), xname = xname, host=host, port=port, db=db, timeout=timeout)

	@app.get('/local/test_gecv1')
	def local_gecv1(snts:str="She has ready.|It are ok.", max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5, model:str="/grammar_error_correcter_v1", device:int=-1):
		''' testing only, used by the health monitor '''
		return pipe.gecsnts(snts.split("|"), max_length=max_length,do_sample=do_sample, batch_size =batch_size, unchanged_ratio=unchanged_ratio, len_ratio = len_ratio, model =model, device=device)

	uvicorn.run(app, host='0.0.0.0', port=port)

if __name__ == '__main__':  #{'She has ready.': 'She is ready.', 'It are ok.': 'It is ok.'}
	fire.Fire({"uvirun":uvirun, "testredis": lambda : print(redis_getgecs()), 'testlocal': lambda: print(pipe.gecsnts())})