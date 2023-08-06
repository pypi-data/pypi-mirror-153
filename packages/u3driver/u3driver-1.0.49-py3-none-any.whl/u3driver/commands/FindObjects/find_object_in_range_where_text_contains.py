from u3driver.commands.command_returning_alt_elements import CommandReturningAltElements
import json
class FindObjectInRangeWhereTextContains(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver,value,text,range_path):
        super(FindObjectInRangeWhereTextContains, self).__init__(socket,request_separator,request_end,appium_driver)
        self.value=value
        self.text = text
        self.range_path = range_path

    
    def execute(self):
        data = self.send_data(self.create_command('findObjectInRangeWhereTextContains', self.value,self.text,self.range_path))
        return json.loads(data)['name']
    