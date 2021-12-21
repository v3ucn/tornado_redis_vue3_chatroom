import asyncio
import aioredis
from tornado import web, websocket
from tornado.ioloop import IOLoop
import tornado.httpserver
import async_timeout

users = []

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


class Msg(web.RequestHandler):


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


    # 发布信息
    async def post(self):

        data = self.get_argument("data",None)

        channel = self.get_argument("channel","channel_1")

        print(data)

        # 发布
        r = await aioredis.from_url("redis://localhost", decode_responses=True)

        await r.publish(channel,data)

        return self.write("ok")


async def reader(channel: aioredis.client.PubSub):
    while True:
        try:
            async with async_timeout.timeout(1):
                message = await channel.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    print(f"(Reader) Message Received: {message}")

                    for user in users:

                        if user.get_cookie("channel") == message["channel"]:

                            user.write_message(message["data"])
        
                await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            pass


async def setup():
    r = await aioredis.from_url("redis://localhost", decode_responses=True)
    pubsub = r.pubsub()

    print(pubsub)
    await pubsub.subscribe("channel_1","channel_2")

    asyncio.ensure_future(reader(pubsub))


application = web.Application([
    (r'/send/',Msg),
    (r'/wb/', WB),
],debug=True)    


if __name__ == '__main__':

    # 监听端口
    application.listen(8000)

    loop = IOLoop.current()
    loop.add_callback(setup)
    loop.start()