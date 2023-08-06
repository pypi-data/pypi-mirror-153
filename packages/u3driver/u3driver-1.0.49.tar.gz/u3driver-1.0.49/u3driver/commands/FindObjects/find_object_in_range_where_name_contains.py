from u3driver.commands.command_returning_alt_elements import CommandReturningAltElements
class FindObjectInRangeWhereNameContains(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver,value,range_path,camera_name,enabled):
        super(FindObjectInRangeWhereNameContains, self).__init__(socket,request_separator,request_end,appium_driver)
        self.value=value
        self.range_path = range_path
        self.camera_name=camera_name
        self.enabled=enabled
    
    def execute(self):
        data = self.send_data(self.create_command('findObjectInRangeWhereNameContains', self.value ,self.range_path, self.camera_name,'true' ))
        return self.get_alt_elements(data)