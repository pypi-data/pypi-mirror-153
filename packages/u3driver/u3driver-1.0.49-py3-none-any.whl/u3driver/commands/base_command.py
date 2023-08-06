import select
import time
from datetime import datetime

from u3driver.altUnityExceptions import *
from u3driver.by import By

BUFFER_SIZE = 1024


class BaseCommand(object):
    def __init__(self, socket, request_separator=';', request_end='&'):
        self.request_separator = request_separator
        self.request_end = request_end
        self.socket = socket

    def recvall(self, print_output=True):
        data = ''
        previousPart = ''
        self.recvalling = True
        # end = time.time() + 5

        while True:

            # r_list, w_list, e_list = select.select(self.r_inputs, self.w_inputs, self.e_inputs, 1)
            # print(str(type(self)) + "recvalling")
            part = self.socket.recv(BUFFER_SIZE)
            data += str(part.decode('utf-8', "ignore"))
            # print(f"recv data: {data}")
            partToSeeAltEnd = previousPart+str(part)
            if data.endswith("::altend"):
                break
            
            if not self.recvalling:
                # print(str(type(self)) + "finish recvall")
                return ''
            # 添加超时报错
            # if time.time() > end:
            #     raise Exception('time out!!!')
            previousPart = str(part)
        try:
            data = data.split('altstart::')[1].split('::altend')[0]
            splitted_string = data.split('::altLog::')
            self.write_to_log_file(splitted_string[1])
            data = splitted_string[0]
            self.write_to_log_file(datetime.now().strftime(
                "%m/%d/%Y %H:%M:%S")+": response received: "+data)
        except:
            print(
                'Data received from socket does not have correct start and end control strings')
            # print(str(type(self)) + "finish recvall")
            return ''
        if print_output:
            now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print(now + ' <= ' + data)
        
        # 每次接收完数据，确保缓存中没有剩余的数据
        self.clear_recv()
        
        # print(str(type(self)) + "finish recvall")
        return data

    def stop_recvall(self):
        self.recvalling = False
    
    def clear_recv(self):

        self.socket.setblocking(False)
        while True:
            try:
                data=self.socket.recvfrom(2048)
            except Exception as e:
                #print str(e)
                break
        self.socket.setblocking(True)



    def write_to_log_file(self, message):
        with open("AltUnityTesterLog.txt", "a",encoding="utf-8") as f:
            f.write(message+"\n")

    def handle_errors(self, data):
        if ('error:' in data):
            if ('error:notFound' in data):
                raise NotFoundException(data)
            elif ('error:propertyNotFound' in data):
                raise PropertyNotFoundException(data)
            elif ('error:methodNotFound' in data):
                raise MethodNotFoundException(data)
            elif ('error:componentNotFound' in data):
                raise ComponentNotFoundException(data)
            elif ('error:couldNotPerformOperation' in data):
                raise CouldNotPerformOperationException(data)
            elif ('error:couldNotParseJsonString' in data):
                raise CouldNotParseJsonStringException(data)
            elif ('error:incorrectNumberOfParameters' in data):
                raise IncorrectNumberOfParametersException(data)
            elif ('error:failedToParseMethodArguments' in data):
                raise FailedToParseArgumentsException(data)
            elif ('error:objectNotFound' in data):
                raise ObjectWasNotFoundException(data)
            elif ('error:propertyCannotBeSet' in data):
                raise PropertyNotFoundException(data)
            elif ('error:nullReferenceException' in data):
                raise NullReferenceException(data)
            elif ('error:unknownError' in data):
                raise UnknownErrorException(data)
            elif ('error:formatException' in data):
                raise FormatException(data)
            else:
                raise Exception(data)
        else:
            return data
        
    def vector_to_json_string(self, x, y, z=None):
        if z is None:
            return '{"x":' + str(x) + ', "y":' + str(y) + '}'
        else:
            return '{"x":' + str(x) + ', "y":' + str(y) +', "z":' + str(z) + '}'

    def positions_to_json_string(self, positions):
        json_positions = [self.vector_to_json_string(p[0], p[1]) for p in positions]
        return self.request_separator.join(json_positions)
    
    def send_data(self, data):
        print(f'=>{data}')
        self.socket.send(data.encode('utf-8'))
        # print("send data finish")
        if ('closeConnection' in data):
            return ''
        elif ('stopDebugMode' in data):
            return ''
        elif ('pauseDebugMode' in data):
            return ''
        # elif ('resumeDebugMode' in data):
        #     return ''
        else:
            return self.recvall()

    def create_command(self, *arguments):
        command = ''
        for argument in arguments:
            command += str(argument)+self.request_separator
        command += self.request_end
        return command

    def set_path(self, by, value):
        if by == By.TAG:
            return "//*[@tag="+str(value)+"]"
        if by == By.COMPONENT:
            return "//*[@component="+str(value)+"]"
        if by == By.LAYER:
            return "//*[@layer="+str(value)+"]"
        if by == By.NAME:
            return "//"+str(value)
        if by == By.ID:
            return "//*[@id="+str(value)+"]"
        if by == By.PATH:
            return value
        if by == By.LEVEL:
            return value

    def set_path_contains(self, by, value):
        if by == By.TAG:
            return "//*[contains(@tag,"+str(value)+")]"
        if by == By.COMPONENT:
            return "//*[contains(@component,"+str(value)+")]"
        if by == By.LAYER:
            return "//*[contains(@layer,"+str(value)+")]"
        if by == By.NAME:
            return "//*[contains(@name,"+str(value)+")]"
        if by == By.ID:
            return "//*[contains(@id,"+str(value)+")]"
        if by == By.PATH:
            return value
