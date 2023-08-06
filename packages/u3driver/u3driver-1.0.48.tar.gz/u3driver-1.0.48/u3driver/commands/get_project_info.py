import json
import traceback

from u3driver.commands.base_command import BaseCommand


class GetProjectInfo(BaseCommand):
    def __init__(self, socket,request_separator,request_end):
        super(GetProjectInfo, self).__init__(socket,request_separator,request_end)
    
    def execute(self):
        data=self.send_data(self.create_command('getProjectInfo'))
        try:
            return json.loads(data)
        except Exception as e:
            traceback.print_exc()
            return {}
