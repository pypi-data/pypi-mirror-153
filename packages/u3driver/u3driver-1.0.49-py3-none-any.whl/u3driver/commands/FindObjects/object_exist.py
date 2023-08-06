from u3driver.commands.command_returning_alt_elements import CommandReturningAltElements


class ObjectExist(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver,by,value):
        super(ObjectExist, self).__init__(socket,request_separator,request_end,appium_driver)
        self.by=by
        self.value=value

    
    def execute(self, false=False):
        path = self.set_path(self.by,self.value)
        data = self.send_data(self.create_command('objectExist', path))
        if data == '1' or data == 1:
            return True
        else:
            return false