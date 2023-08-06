import json

from u3driver.commands.command_returning_alt_elements import CommandReturningAltElements


class FindChild(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver,value):
        super(FindChild, self).__init__(socket,request_separator,request_end,appium_driver)
        self.value=value
    
    def execute(self):
        data = self.send_data(self.create_command('findChild', self.value))
        res = json.loads(data)
        ret = []
        
        for item in res:
            ret.append(item['name'])
        
        return ret
