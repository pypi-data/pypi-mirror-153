import json

from u3driver.commands.command_returning_alt_elements import CommandReturningAltElements


class FindAllText(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver):
        super(FindAllText, self).__init__(socket,request_separator,request_end,appium_driver)
    
    def execute(self):
        data = self.send_data(self.create_command('findAllText'))
        res = json.loads(data)
        return res
