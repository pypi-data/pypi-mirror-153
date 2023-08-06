from u3driver.commands.command_returning_alt_elements import CommandReturningAltElements
# from u3driver.by import By
# import json
class GetInspector(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver, id):
        super(GetInspector, self).__init__(socket,request_separator,request_end,appium_driver)
        self.id = str(id)
    
    def execute(self):
        data = self.send_data(self.create_command('getInspector', self.id))
        return data
