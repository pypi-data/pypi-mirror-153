import json
import threading
import time

from u3driver.commands.base_command import BaseCommand


class RecordProfile(BaseCommand):
    '''
    record 项目列表
    '''
    def __init__(self, socket,request_separator,request_end,collection):
        super(RecordProfile, self).__init__(socket,request_separator,request_end)
        self.collection=collection
            
    # 开始采集
    def start(self):
        data = self.send_data(self.create_command('RecordProfile',"1",self.collection))
        return json.loads(data)
    # 结束采集
    def stop(self):
        data = self.send_data(self.create_command('RecordProfile',"0"))
        return json.loads(data)
    
    def abandon_or_upload(self,ab_or_up):
        data = self.send_data(self.create_command('RecordProfile',ab_or_up))
        return json.loads(data)

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

        