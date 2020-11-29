import tagsCountStreaming
import nameCountStreaming
import typeCountStreaming
import preHandler
import _thread
import time

if __name__ == '__main__':
    # _thread.start_new_thread(tagsCountStreaming.start, ())
    _thread.start_new_thread(nameCountStreaming.start, ())
    # _thread.start_new_thread(typeCountStreaming.start, ())
    time.sleep(10)
    # _thread.start_new_thread(preHandler.tagCount, ("tag",))
    # _thread.start_new_thread(preHandler.typeCount, ("type",))
    _thread.start_new_thread(preHandler.nameCount, ("name",))
    while 1:
        pass
