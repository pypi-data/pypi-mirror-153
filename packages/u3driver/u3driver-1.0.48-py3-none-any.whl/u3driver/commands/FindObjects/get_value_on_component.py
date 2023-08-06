from u3driver.commands.command_returning_alt_elements import CommandReturningAltElements


class GetValueOnComponent(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver,path,componetName,valueName):
        super(GetValueOnComponent, self).__init__(socket,request_separator,request_end,appium_driver)
        self.path=path
        self.componetName = componetName
        self.valueName = valueName
    
    def execute(self):
        data = self.send_data(self.create_command('getValueOnComponent', self.path,self.componetName,self.valueName))
        return data
