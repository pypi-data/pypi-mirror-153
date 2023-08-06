# 22-6-4 
import pika,json, sys, fire, time, dsk,requests, pipe
		
def consume(queue_name,  dst_exchange, routing_key='',  host='172.17.0.1', port=5672, user='root', pwd='', heartbeat=120, durable=True
		, gechost=None, dskhost='172.17.0.1:7095'): 
	''' gpu120.wrask.com:8180 2022.6.4 '''
	credentials = pika.PlainCredentials(user, pwd)  
	connection	= pika.BlockingConnection(pika.ConnectionParameters(host = host,port = port,virtual_host = '/',credentials = credentials))
	channel		= connection.channel()
	result		= channel.queue_declare(queue = queue_name, durable=durable) 
	gec_func	= pipe.gecsnts
	if gechost: gec_func = lambda snts: requests.post(f"http://{gechost}/redis/getgecs", json=snts).json ()
	print("queue is :", queue_name,  gec_func, flush=True)

	def callback(ch, method, properties, body):
		try:
			ch.basic_ack(delivery_tag = method.delivery_tag)
			arr = json.loads(body.decode())
			res = dsk.todsk( arr.get('essay_or_snts', ''), arr.get('asdsk',True), arr.get('dskhost',dskhost), gec_func=gec_func )
			# check formula 
			channel.basic_publish(exchange=dst_exchange,routing_key=routing_key, body=json.dumps(res)) 
		except Exception as ex:
			print(">>callback Ex:", ex, time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())), body.decode()[0:10])
			channel.close()
			connection.close()

	channel.basic_consume(queue_name, callback)
	channel.start_consuming()
	#connection.close()

if __name__ == '__main__': 
	fire.Fire(consume) 