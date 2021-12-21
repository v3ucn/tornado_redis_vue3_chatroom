import tornado.httpserver
import tornado.websocket

import tornado.ioloop

import tornado.web

import redis

import threading

import asyncio

# 用户列表
users = []

# 频道列表
channels = ["channel_1","channel_2"]


# websocket协议
class WB(tornado.websocket.WebSocketHandler):


	# 跨域支持
	def check_origin(self,origin):

		return True

	# 开启链接
	def open(self):


		users.append(self)


	# 接收消息
	def on_message(self,message):

		self.write_message(message['data'])

	# 断开
	def on_close(self):

		users.remove(self)






# 基于redis监听发布者发布消息
def redis_listener(loop):

	asyncio.set_event_loop(loop)

	async def listen(): 

		r = redis.Redis(decode_responses=True)

		# 声明pubsb实例
		ps = r.pubsub()

		# 订阅聊天室频道

		ps.subscribe(["channel_1","channel_2"])


		# 监听消息
		for message in ps.listen():

			print(message)

			# 遍历链接上的用户
			for user in users:

				print(user)

				if message["type"] == "message" and message["channel"] == user.get_cookie("channel"):


					user.write_message(message["data"])

	future = asyncio.gather(listen())
	loop.run_until_complete(future)


#导入装饰方法
from functools import wraps
r = redis.Redis(decode_responses=True)


# 装饰器
def pass_window(func):

	@wraps(func)
	def wrapper(self,*args,**kwargs):

		uid = 3

		time_zone = 2
		times = 50

		# 获取计数器
		count = r.get(uid)

		if not count:

			count = 1

			r.setex(uid,time_zone,count)

		print(count)

		if int(count) < times:

			r.incr(uid)

			print("继续执行")
			response = func(self,*args,**kwargs)
			return response
		else:

			print("您的访问过于频繁")
	return wrapper




# 接口  发布信息
class Msg(tornado.web.RequestHandler):


	# 重写父类方法
	def set_default_headers(self):

		# 设置请求头信息
		print("开始设置")
		# 域名信息
		self.set_header("Access-Control-Allow-Origin","*")
		# 请求信息
		self.set_header("Access-Control-Allow-Headers","x-requested-with")
		# 请求方式
		self.set_header("Access-Control-Allow-Methods","POST,GET,PUT,DELETE")

	#@pass_window
	async def get(self):

		data = self.get_argument("data",None)
		id = self.get_argument("id",None)

		print(data)

		# 发布
		r = redis.Redis()

		r.publish("chat",data)

		return self.write("ok")

	# 发布信息
	async def post(self):

		data = self.get_argument("data",None)

		channel = self.get_argument("channel","channel_1")

		print(data)

		# 发布
		r = redis.Redis()

		r.publish(channel,data)

		return self.write("ok")


# 建立torando实例

app = tornado.web.Application(

	[

	(r'/send/',Msg),
	(r'/wb/',WB)

	],debug=True

)

if __name__ == '__main__':


	loop = asyncio.new_event_loop()

	# 单线程启动订阅者服务
	threading.Thread(target=redis_listener,args=(loop,)).start()


	# 声明服务器
	http_server_1 = tornado.httpserver.HTTPServer(app)

	# 监听端口
	http_server_1.listen(8000)

	# 开启事件循环
	tornado.ioloop.IOLoop.instance().start()
	



