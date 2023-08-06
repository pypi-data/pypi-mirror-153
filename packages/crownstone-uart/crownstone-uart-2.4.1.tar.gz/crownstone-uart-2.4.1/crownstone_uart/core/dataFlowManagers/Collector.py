import asyncio
import time

from crownstone_uart.core.UartEventBus import UartEventBus

class Collector:
    
    def __init__(self, topic= None, timeout = 10, interval = 0.05):
        self.response = None
        self.timeout = timeout
        self.interval = interval

        self.cleanupId = None
        if topic is not None:
            self.cleanupId = UartEventBus.subscribe(topic, self.collect)

    def __del__(self):
        UartEventBus.unsubscribe(self.cleanupId)

    def clear(self):
        self.response = None

    async def receive(self):
        counter = 0
        while counter < self.timeout:
            if self.response is not None:
                # cleanup the listener(s)
                UartEventBus.unsubscribe(self.cleanupId)
                return self.response

            await asyncio.sleep(self.interval)
            counter += self.interval

        UartEventBus.unsubscribe(self.cleanupId)
        return None
    
    def receive_sync(self):
        counter = 0
        while counter < self.timeout:
            if self.response is not None:
                # cleanup the listener(s)
                UartEventBus.unsubscribe(self.cleanupId)
                return self.response

            time.sleep(self.interval)
            counter += self.interval

        UartEventBus.unsubscribe(self.cleanupId)
        return None

    def collect(self, data):
        self.response = data

