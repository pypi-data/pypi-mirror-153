from u3driver.commands.base_command import BaseCommand


class GetComponent(BaseCommand):
    def __init__(self, socket,request_separator,request_end,alt_object):
        super(GetComponent, self).__init__(socket,request_separator,request_end)
        self.alt_object=alt_object

    def execute(self):
        data = self.send_data(self.create_command('getAllComponents', self.alt_object))
        return self.handle_errors(data)
