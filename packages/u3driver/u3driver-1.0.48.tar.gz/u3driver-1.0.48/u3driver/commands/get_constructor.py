import json
import traceback

from u3driver.commands.base_command import BaseCommand


class GetConstructor(BaseCommand):
    def __init__(self, socket,request_separator,request_end,type_name):
        super(GetConstructor, self).__init__(socket,request_separator,request_end)
        self.type_name = type_name
    
    def execute(self):
        data=self.send_data(self.create_command('getConstructor', self.type_name))
        data = self.handle_errors(data)
        try:
            return json.loads(data)
        except Exception as e:
            traceback.print_exc()
            return {}
