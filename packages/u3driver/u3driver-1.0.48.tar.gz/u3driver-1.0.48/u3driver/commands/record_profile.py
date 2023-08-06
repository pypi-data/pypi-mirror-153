import json
import threading
import time

from u3driver.commands.base_command import BaseCommand


class RecordProfileThread(threading.Thread):
    def __init__(self, target_func,  *args, **kwargs):
        super(RecordProfileThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.target_func = target_func
        self.is_record = True

    def run(self):
        data = self.target_func()
        if data == "record profile stop":
            self.is_record = False
            self.stop()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class RecordProfile(BaseCommand):
    '''
    record = 0 停止打点
    record = 1 开始打点
    '''
    def __init__(self, socket,request_separator,request_end,record = "1"):
        super(RecordProfile, self).__init__(socket,request_separator,request_end)
        self.record = record
        self.stop_record = False
        self.record_files = []




    def get_data(self):
        while True:
            if self.stop_record:
                time.sleep(0.1)
                return

            data = self.recvall()
            
            if data == "record profile stop":
                time.sleep(0.1)
                return data
            
            if data == "":
                time.sleep(0.1)
                continue
            
            data = json.loads(data)
            self.record_files.append(data)
            

    def start(self):
        data = self.send_data(self.create_command('RecordProfile','1'))
        
        # self.thread = RecordProfileThread(target_func=self.get_data)
        # self.thread.start()
        # print(data)
        return data
    
    def stop(self):
        self.stop_recvall()
        self.stop_record = True
        # self.thread.stop()
        data = self.send_data(self.create_command('RecordProfile','0'))

        while data != "record profile stop":
            data = json.loads(data)
            self.record_files.append(data)
            data = self.recvall()

        time.sleep(0.5)
        self.clear_recv()
        # print(data)
        return data
    
    def check(self):

        data = self.send_data(self.create_command('checkProfile'))

        try:
            return json.loads(data)
        except Exception as e:
            return []

        # if len(self.record_files) > 0:
        #     ret = self.record_files[::]
        #     self.record_files = []
        #     return ret
        # return []

        