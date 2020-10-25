import tagsCountStreaming
import preHandler
import _thread
import time

if __name__ == '__main__':
    _thread.start_new_thread(tagsCountStreaming.start, ())
    time.sleep(40)
    _thread.start_new_thread(preHandler.tagCount, ("tag",))
    while 1:
        pass
