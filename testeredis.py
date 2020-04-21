import sys
import os
import gevent
import redis
from gevent import monkey

monkey.patch_socket()
# All greenlets running on system
greenlets = []

class RedisTeste(object):

    REDIS_CONFIG = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'decode_responses': True,
        }
	
    def __init__(self):
        self._publisher_ready = False
        self._subscriber_ready = False
        self._redis = redis.StrictRedis(**RedisTeste.REDIS_CONFIG)
        self._sum = 0
        self._sum2 = 0

        if not self._is_registered('system.services','probe'):
            self._redis.append('system.services','probe')

    def _is_registered(self, channel, value):
        list = self._redis.get(channel)
        if list:
            items = list.split(' ')
            for item in items:
                if item == value:
                    return True
        return False  

    def run(self):
        while True:
            print("running")
            self._sum = self._sum + 1
            self._sum2 = self._sum2 + 2
            self.publisher(str("sonda1.temperatura"),self._sum)
            self.publisher("sonda1.umidade",self._sum2)
            self.publisher(str("sonda2.umidade"),self._sum)
            self.publisher("sonda2.temperatura",self._sum2)
            gevent.sleep(10)

    def publisher(self, channel, value):
        self._redis.set(str(channel),str(value))
        self._redis.publish(str(channel),str(value))

    def subscriber(self):
        print("subscribe")
        pubsub = self._redis.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe("sonda1.temperatura") 
        pubsub.subscribe("sonda1.umidade")
        pubsub.subscribe("sonda2.temperatura") 
        pubsub.subscribe("sonda2.umidade")
        self._subscriber_ready = True
        for notification in pubsub.listen():
            if notification["channel"] == "sonda1.temperatura": #Procura o canal
                if(isinstance(notification["data"], str) == True): #verifica se o valor e uma string
                    print(notification["data"]) 
            if notification["channel"] == "sonda1.umidade": #Procura o canal
                if(isinstance(notification["data"], str) == True): #verifica se o valor e uma string
                    print(notification["data"]) 
            if notification["channel"] == "sonda2.temperatura": #Procura o canal
                if(isinstance(notification["data"], str) == True): #verifica se o valor e uma string
                    print(notification["data"]) 
            if notification["channel"] == "sonda2.umidade": #Procura o canal
                if(isinstance(notification["data"], str) == True): #verifica se o valor e uma string
                    print(notification["data"]) 

def main():
    redisTeste = RedisTeste()
    greenlets.append(gevent.spawn(redisTeste.subscriber))
    greenlets.append(gevent.spawn(redisTeste.run))
    gevent.joinall(greenlets)

if __name__ == '__main__':
    main()
