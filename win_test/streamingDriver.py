import typeCountStreaming
import preHandler
import _thread
import time

if __name__ == '__main__':
    _thread.start_new_thread(typeCountStreaming.start, ())
    time.sleep(10)
    _thread.start_new_thread(preHandler.typeCount, ())
    while(1):
        pass