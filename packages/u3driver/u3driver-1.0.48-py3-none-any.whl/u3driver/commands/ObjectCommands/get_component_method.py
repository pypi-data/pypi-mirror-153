import json

from u3driver.commands.base_command import BaseCommand


class GetComponentMethod(BaseCommand):
    def __init__(self, socket,request_separator,request_end,alt_object,component_name):
        super(GetComponentMethod, self).__init__(socket,request_separator,request_end)
        self.alt_object=alt_object
        self.component_name = component_name

    def execute(self):
        data = self.send_data(self.create_command('getComponentMethods', self.alt_object, self.component_name))
        return self.handle_errors(data)
