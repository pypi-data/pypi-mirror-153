import json
import traceback

from u3driver.commands.base_command import BaseCommand


class CallStaticMethod(BaseCommand):
    def __init__(self, socket,request_separator,request_end,type_name,method_name,parameter_data):
        super(CallStaticMethod, self).__init__(socket,request_separator,request_end)
        self.type_name = type_name
        self.method_name = method_name
        self.parameter_data = parameter_data
    
    def execute(self):
        data=self.send_data(self.create_command('callStaticMethod', self.type_name,self.method_name,self.parameter_data))
        return self.handle_errors(data)
