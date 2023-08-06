import json

from u3driver.commands.command_returning_alt_elements import CommandReturningAltElements


class GetScreen(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver):
        super(GetScreen, self).__init__(socket,request_separator,request_end,appium_driver)
    
    def execute(self):
        json_data = self.send_data(self.create_command('getScreen'))
        data = json.loads(json_data)
        return data['width'], data['height']