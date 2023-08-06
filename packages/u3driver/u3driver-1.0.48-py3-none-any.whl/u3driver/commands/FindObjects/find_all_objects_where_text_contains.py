from u3driver.commands.command_returning_alt_elements import CommandReturningAltElements
from u3driver.by import By
import json
class FindAllObjectWhereTextContains(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver,text):
        super(FindAllObjectWhereTextContains, self).__init__(socket,request_separator,request_end,appium_driver)
        self.text = text

    def execute(self):
        data = self.send_data(self.create_command('findAllObjectWhereTextContains' ,self.text))
        res = json.loads(data)
        return res
