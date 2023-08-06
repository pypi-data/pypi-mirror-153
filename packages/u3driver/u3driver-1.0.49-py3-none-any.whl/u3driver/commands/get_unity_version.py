from u3driver.commands.base_command import BaseCommand


class GetUnityVersion(BaseCommand):
    def __init__(self, socket,request_separator,request_end):
        super(GetUnityVersion, self).__init__(socket,request_separator,request_end)
    
    def execute(self):
        data=self.send_data(self.create_command('getUnityVersion'))
        return data
