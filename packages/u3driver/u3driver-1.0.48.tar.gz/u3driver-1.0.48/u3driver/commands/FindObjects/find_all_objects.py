import json

from u3driver.commands.command_returning_alt_elements import CommandReturningAltElements


class FindAllObjects(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver,value):
        super(FindAllObjects, self).__init__(socket,request_separator,request_end,appium_driver)
        self.value=value
    
    def execute(self):
        data = self.send_data(self.create_command('findObjectAllChildren', self.value))
        res = json.loads(data)
        return res
