# tornado_redis_vue3_chatroom
把酒言欢话聊天，基于Vue3.0+Tornado6.1+Redis发布订阅(pubsub)模式打造实时(websocket)通信聊天系统


# 前端服务

cd front

npm install

npm run serve

访问 http://localhost:8080


# 后端 tornado 服务 同步消费

cd back

pip install tornado==6.1

pip install redis

python3 main.py

# 后端 tornado 服务 异步消费

cd back

pip install tornado==6.1

pip install redis

pip install aioredis

python3 main_aioredis.py