from u3driver.commands.command_returning_alt_elements import CommandReturningAltElements


class FindObjectAndTap(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver,by,value,camera_name,enabled):
        super(FindObjectAndTap, self).__init__(socket,request_separator,request_end,appium_driver)
        self.by=by
        self.value=value
        self.camera_name=camera_name
        self.enabled=enabled
    
    def execute(self):
        path=self.set_path(self.by,self.value)
        data = self.send_data(self.create_command('findObjectAndTap', path , self.camera_name ,'true'))
        return self.get_alt_element(data)