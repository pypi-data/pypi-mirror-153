import json

from u3driver.commands.base_command import BaseCommand


class Drag(BaseCommand):
    def __init__(self, socket,request_separator,request_end,path,x1,y1,x2 = None,y2 = None):
        super(Drag, self).__init__(socket,request_separator,request_end)
        self.path = path
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def execute(self):
        #x1,y1:[0-1] 
        screen = self.send_data(self.create_command('getScreen'))
        screen = json.loads(screen)
        screen = {"width":int(screen["width"]), "height":int(screen['height'])}


        if self.x2 == None or self.y2 == None:
            data = self.send_data(self.create_command('dragObject', self.path,self.x1*screen["width"],self.y1*screen["height"]))
        else:
            data = self.send_data(self.create_command('dragObject', self.path,self.x1*screen["width"],self.y1*screen["height"],self.x2*screen["width"],self.y2*screen["height"]))
        return data
