import json
import threading
import time

from u3driver.commands.base_command import BaseCommand


class DebugModeThread(threading.Thread):
    def __init__(self, target_func,  *args, **kwargs):
        super(DebugModeThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.target_func = target_func
        self.is_record = True

    def run(self):
        data = self.target_func()
        if data == "Close Debug Mode":
            self.is_record = False
            # print("Debug Mode Closed!!!!!!!!!")
            self.stop()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class DebugMode(BaseCommand):

    def __init__(self, socket,request_separator,request_end,file_path = None):
        self.stop_record = False
        self.pause_record = False
        print("DebugMode.init")
        super().__init__(socket,request_separator,request_end)
        self.file_path = file_path

    def get_record(self):
        # self.stop_record = False
        # self.pause_record = False
        count = 0
        while True:
            if self.stop_record:
                # print("stop_record")
                time.sleep(0.1)
                return
            if self.pause_record:
                # print("pause_record")
                time.sleep(0.1)
                continue
            # print("get_record")
            data = self.recvall()
            self.data_str = ''
            if data == "Close Debug Mode":
                # print("Close Debug Mode")
                time.sleep(0.1)
                return data
            if data == "200":
                # print("200")
                time.sleep(0.1)
                continue
            if data == '':
                # print("empty")
                time.sleep(0.1)
                continue

            # print(f'data = {data}')
            count += 1
            json_data = json.loads(data)
            self.time = 2
            if "time" in json_data:
                self.time = float(json_data['time'])
            if "start position" in json_data:
                self.start_position = tuple(eval(json_data['start position']))
            elif "end position" in json_data:
                self.end_position = tuple(eval(json_data['end position']))
                if self.start_position != None and self.end_position != None:
                    self.data_str += '\t' * self.tap_count + f'time.sleep({self.time})\n'
                    self.data_str += '\t' * self.tap_count + 'udriver.drag_object("'+json_data['name'].replace("/","//")+f'",{self.start_position[0] / self.screen["width"]},{self.start_position[1] / self.screen["height"]},{self.end_position[0] / self.screen["width"]},{self.end_position[1] / self.screen["height"]})\n'
                    self.start_position = None
                    self.end_position = None
            elif "value" in json_data:
                self.data_str += '\t' * self.tap_count + f'time.sleep({self.time})\n'
                self.data_str += '\t' * self.tap_count + 'udriver.find_object(By.PATH,"'+json_data['name'].replace("/","//")+'")'
                self.data_str += '.set_text("' + json_data['value'] + '")\n'
            elif "name" in json_data:
                self.data_str += '\t' * self.tap_count + f'time.sleep({self.time})\n'
                self.data_str += '\t' * self.tap_count + 'udriver.find_object(By.PATH,"'+json_data['name'].replace("/","//")+'")'
                self.data_str += '.tap()\n'
            if self.file_path != None:
                    all_str = '' 
                    with open(file=self.file_path, mode='r+', encoding='utf-8') as f:
                        all_str = f.read()

                    all_str = all_str.replace(self.end_str,"")
                    all_str += self.data_str
                    all_str += self.end_str

                    with open(file=self.file_path, mode='w+', encoding='utf-8') as f:
                        
                        f.write(all_str)


    def is_record(self):
        return self.thread.is_record
    
    def stop(self):
        # 停掉线程后清空
        self.stop_recvall()
        self.stop_record = True
        self.thread.stop()
        self.send_data(self.create_command('stopDebugMode'))
        time.sleep(0.5)
        self.clear_recv()
        # time.sleep(0.5)
        # self.recvall()
        

    
    def pause(self):
        self.pause_record = True
        # self.thread.stop()
        # time.sleep(0.5)
        self.send_data(self.create_command('pauseDebugMode'))
        time.sleep(0.5)
        self.clear_recv()
        # self.recvall()
        # time.sleep(0.5)
        # self.stop_recvall()
    
    def resume(self):
        # self.clear_recv()
        self.pause_record = False
        # time.sleep(0.5)
        self.send_data(self.create_command('resumeDebugMode'))
        # self.recvall()
        # time.sleep(0.5)
        # self.stop_recvall()
        # self.thread.start()

    def sync_record(self):
        self.screen = self.send_data(self.create_command('getScreen'))
        print(self.screen)
        self.screen = json.loads(self.screen)
        self.screen = {"width":int(self.screen["width"]), "height":int(self.screen['height'])}

        response = self.send_data(self.create_command('debugMode', '0'))
        if response == "Open Debug Mode" or response == "Debug Already Opened":
            ##结束行有17行
            self.end_str = """\texcept Exception as e:\n\t\tprint(f'{e}')\n\t\traise e\n\nif __name__ == '__main__':\n\tparser = argparse.ArgumentParser()\n\tparser.add_argument('-s', help="device serial")\n\tparser.add_argument('-i', help="ip address")\n\tparser.add_argument('-port', help="ip address")\n\targs = parser.parse_args()\n\tdevice_s = args.s\n\tip = args.i\n\tport = int(args.port)\n\tudriver = AltrunUnityDriver(device_s,"", ip, TCP_PORT=port,timeout=60, log_flag=True)\n\tAutoRun(udriver)\n\tudriver.stop()"""
            self.tap_count = 0
            if self.file_path != None:
                self.data_str = ''
                self.data_str += 'from u3driver import AltrunUnityDriver\n'
                self.data_str += 'from u3driver import By\n'
                self.data_str += 'import time\n'
                self.data_str += 'import argparse\n\n'
                self.data_str += 'def AutoRun(udriver):\n'
                self.tap_count += 1
                self.data_str += '\t' * self.tap_count + 'try:\n'
                self.tap_count += 1
                
                if self.file_path != None:
                        with open(file=self.file_path, mode='w+', encoding='utf-8') as self.f:
                            self.f.write(self.data_str)
            self.start_position = None
            self.end_position = None
            while True:
                data = self.recvall()
                self.data_str = ''
                if data == "Close Debug Mode":
                    return data
                json_data = json.loads(data)
                time = 2
                if "time" in json_data:
                    time = float(json_data['time'])
                if "start position" in json_data:
                    self.start_position = tuple(eval(json_data['start position']))
                elif "end position" in json_data:
                    self.end_position = tuple(eval(json_data['end position']))
                    if self.start_position != None and self.end_position != None:
                        self.data_str += '\t' * self.tap_count + f'time.sleep({time})\n'
                        self.data_str += '\t' * self.tap_count + 'udriver.drag_object("'+json_data['name'].replace("/","//")+f'",{self.start_position[0] / self.screen["width"]},{self.start_position[1] / self.screen["height"]},{self.end_position[0] / self.screen["width"]},{self.end_position[1] / self.screen["height"]})\n'
                        self.start_position = None
                        self.end_position = None
                elif "value" in json_data:
                    self.data_str += '\t' * self.tap_count + f'time.sleep({time})\n'
                    self.data_str += '\t' * self.tap_count + 'udriver.find_object(By.PATH,"'+json_data['name'].replace("/","//")+'")'
                    self.data_str += '.set_text("' + json_data['value'] + '")\n'
                elif "name" in json_data:
                    self.data_str += '\t' * self.tap_count + f'time.sleep({time})\n'
                    self.data_str += '\t' * self.tap_count + 'udriver.find_object(By.PATH,"'+json_data['name'].replace("/","//")+'")'
                    self.data_str += '.tap()\n'
                if self.file_path != None:
                        all_str = '' 
                        with open(file=self.file_path, mode='r+', encoding='utf-8') as f:
                            all_str = f.read()

                        all_str = all_str.replace(self.end_str,"")
                        all_str += self.data_str
                        all_str += self.end_str

                        with open(file=self.file_path, mode='w+', encoding='utf-8') as f:
                            
                            f.write(all_str)
        return response
    
    def async_record(self):
        self.screen = self.send_data(self.create_command('getScreen'))
        print(self.screen)
        self.screen = json.loads(self.screen)
        self.screen = {"width":int(self.screen["width"]), "height":int(self.screen['height'])}

        response = self.send_data(self.create_command('debugMode', '0'))
        if response == "Open Debug Mode" or response == "Debug Already Opened":
            ##结束行有17行
            self.end_str = """\texcept Exception as e:\n\t\tprint(f'{e}')\n\t\traise e\n\nif __name__ == '__main__':\n\tparser = argparse.ArgumentParser()\n\tparser.add_argument('-s', help="device serial")\n\tparser.add_argument('-i', help="ip address")\n\tparser.add_argument('-port', help="ip address")\n\targs = parser.parse_args()\n\tdevice_s = args.s\n\tip = args.i\n\tport = int(args.port)\n\tudriver = AltrunUnityDriver(device_s,"", ip, TCP_PORT=port,timeout=60, log_flag=True)\n\tAutoRun(udriver)\n\tudriver.stop()"""
            self.tap_count = 0
            if self.file_path != None:
                self.data_str = ''
                self.data_str += 'from u3driver import AltrunUnityDriver\n'
                self.data_str += 'from u3driver import By\n'
                self.data_str += 'import time\n'
                self.data_str += 'import argparse\n\n'
                self.data_str += 'def AutoRun(udriver):\n'
                self.tap_count += 1
                self.data_str += '\t' * self.tap_count + 'try:\n'
                self.tap_count += 1
                
                if self.file_path != None:
                        with open(file=self.file_path, mode='w+', encoding='utf-8') as self.f:
                            self.f.write(self.data_str)
            self.start_position = None
            self.end_position = None

            self.thread = DebugModeThread(target_func=self.get_record)
            # self.thread = threading.Thread(target=self.get_record)
            self.thread.start()

                
        return response
