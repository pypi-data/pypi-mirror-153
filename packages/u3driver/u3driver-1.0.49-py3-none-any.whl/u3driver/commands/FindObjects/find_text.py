import json

from u3driver.commands.command_returning_alt_elements import \
    CommandReturningAltElements


class FindText(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver,keyword):
        super(FindText, self).__init__(socket,request_separator,request_end,appium_driver)
        self.keyword = keyword
    
    def execute(self):
        data = self.send_data(self.create_command('findText',self.keyword))
        return data
