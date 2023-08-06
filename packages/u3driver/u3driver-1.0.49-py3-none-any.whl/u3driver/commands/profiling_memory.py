import json

from u3driver.commands.command_returning_alt_elements import BaseCommand


class ProfilingMemory(BaseCommand):
    def __init__(self, socket,request_separator,request_end,value):
        super(ProfilingMemory, self).__init__(socket,request_separator,request_end)
        self.value=value
    
    def execute(self):
        data = self.send_data(self.create_command('ProfilingMemory', self.value))
        res = json.loads(data)
        return res