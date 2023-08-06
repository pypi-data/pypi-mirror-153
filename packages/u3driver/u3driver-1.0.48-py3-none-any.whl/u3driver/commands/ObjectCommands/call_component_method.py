from u3driver.commands.base_command import BaseCommand


class CallComponentMethod(BaseCommand):
    def __init__(self, socket,request_separator,request_end,alt_object,component_name,method_name,parameter_data):
        super(CallComponentMethod, self).__init__(socket,request_separator,request_end)
        self.alt_object=alt_object
        self.component_name = component_name
        self.method_name = method_name
        self.parameter_data = parameter_data

    def execute(self):
        data = self.send_data(self.create_command('callComponentMethod', self.alt_object, self.component_name,self.method_name,self.parameter_data))
        return self.handle_errors(data)
