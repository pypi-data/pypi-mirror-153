import json
import os
import socket
import time
import zipfile

from u3driver.altElement import AltElement
from u3driver.commands import *
from u3driver.commands.record_profile import RecordProfile

BUFFER_SIZE = 1024

class AltrunUnityDriver(object):

    def __init__(self, appium_driver,  platform, TCP_IP='127.0.0.1',TCP_PORT=13000, timeout=60,request_separator=';',request_end='&',device_id="",log_flag=False):
        self.TCP_PORT = TCP_PORT
        self.request_separator=request_separator
        self.request_end=request_end
        self.log_flag=log_flag
        self.appium_driver=None
        self.connect = False
        self.pause = False
        self.debug_handler = None
        self.profiler_handler = None

        if (appium_driver != None):
            self.appium_driver = appium_driver

        while timeout > 0:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # self.socket.setb
                self.socket.connect((TCP_IP, TCP_PORT))
                self.socket.settimeout(timeout)
                # print("Get server Version")
                GetServerVersion(self.socket, self.request_separator, self.request_end).execute()
                self.connect = True
                break
            except Exception as e:
                print(e)
                print('AltUnityServer not running on port ' + str(self.TCP_PORT) +
                      ', retrying (timing out in ' + str(timeout) + ' secs)...')
                timeout -= timeout
                # time.sleep(timeout)

        if timeout <= 0:
            raise Exception('Could not connect to AltUnityServer on: '+ TCP_IP +':'+ str(self.TCP_PORT))

    def NeedPause(self):
        while self.pause:
            time.sleep(1)
            print("[Info]udriver is pausing!")
    
    def Pause(self,pause):
        self.pause = pause

    def stop(self):
        self.pause = False
        CloseConnection(self.socket,self.request_separator,self.request_end).execute()

    def find_object(self,by,value,image_url = None):
        self.NeedPause()
        return FindObject(self.socket,self.request_separator,self.request_end,self.appium_driver,by,value,image_url).execute()

    def tap_at_coordinates(self,x,y):
        self.NeedPause()
        return TapAtCoordinates(self.socket,self.request_separator,self.request_end,self.appium_driver,x,y).execute()

    def find_object_and_tap(self,by,value,camera_name='',enabled=True):
        self.NeedPause()
        return FindObjectAndTap(self.socket,self.request_separator,self.request_end,self.appium_driver,by,value,camera_name,enabled).execute()

    def object_exist(self, by,value):
        self.NeedPause()
        return ObjectExist(self.socket,self.request_separator,self.request_end,self.appium_driver,by,value).execute()

    def get_screen(self):
        self.NeedPause()
        return GetScreen(self.socket,self.request_separator,self.request_end,self.appium_driver).execute()

    def find_child(self,value):
        self.NeedPause()
        return FindChild(self.socket,self.request_separator,self.request_end,self.appium_driver,value).execute()
    
    def get_object_rect(self,value):
        self.NeedPause()
        return GetObjectRect(self.socket,self.request_separator,self.request_end,self.appium_driver,value).execute()
    
    def find_all_objects(self,value):
        self.NeedPause()
        return FindAllObjects(self.socket,self.request_separator,self.request_end,self.appium_driver,value).execute()
    
    def find_object_in_range_where_text_contains(self, name, text, range_path):
        return FindObjectInRangeWhereTextContains(self.socket, self.request_separator, self.request_end,
                                                  self.appium_driver, name, text, range_path).execute()

    def find_object_in_range_where_name_contains(self, name, range_path, camera_name='', enabled=True):
        return FindObjectInRangeWhereNameContains(self.socket, self.request_separator, self.request_end,
                                                  self.appium_driver, name, range_path, camera_name, enabled).execute()

    def find_all_objects_where_text_contains(self, text):
        return FindAllObjectWhereTextContains(self.socket, self.request_separator, self.request_end, self.appium_driver,
                                              text).execute()

    def find_objects_which_contains(self, by, value, camera_name='', enabled=True):
        return FindObjectsWhichContains(self.socket, self.request_separator, self.request_end, self.appium_driver, by,
                                        value, camera_name, enabled).execute()

    def find_object_which_contains(self, by, value, camera_name='', enabled=True):
        return FindObjectWhichContains(self.socket, self.request_separator, self.request_end, self.appium_driver, by,
                                       value, camera_name, enabled).execute()

    # 调用格式如下：组件名必须是完整的，而且要带上模块名称
    # udriver.get_value_on_component("//Canvas","Test,Assembly-CSharp","test1")
    # udriver.get_value_on_component("//Canvas","UnityEngine.UI.Text,UnityEngine.UI","text")
    def get_value_on_component(self, path, component_name, value_name):
        return GetValueOnComponent(self.socket, self.request_separator, self.request_end, self.appium_driver, path,
                                   component_name, value_name).execute()

    def debug_mode(self,file_path = None, is_async=False):
        if self.debug_handler:
            self.debug_handler.stop()
            self.debug_handler = None
        
        self.debug_handler = DebugMode(self.socket,self.request_separator,self.request_end,file_path)
        if is_async:
            return self.debug_handler.async_record()
        else:
            return self.debug_handler.sync_record()
        # return DebugMode(self.socket,self.request_separator,self.request_end,file_path).execute()
    
    def debug_mode_pause(self):
        if self.debug_handler:
            return self.debug_handler.pause()

    def debug_mode_resume(self):
        if self.debug_handler:
            return self.debug_handler.resume()
    
    def debug_mode_stop(self):
        if self.debug_handler:
            ret = self.debug_handler.stop()
        self.debug_handler = None
        return ret
    
    def is_debug_mode_record(self):
        if self.debug_handler:
            return self.debug_handler.is_record()

    def drag_object(self,path,x1,y1,x2 = None,y2 = None):
        self.NeedPause()
        return Drag(self.socket,self.request_separator,self.request_end,path,x1,y1,x2,y2).execute()

    
    def tap_by_id(self,id):
        # json.dumps({"id",id})
        self.NeedPause()
        return AltElement(CommandReturningAltElements(self.socket,self.request_separator,self.request_end,self.appium_driver),self.appium_driver,'{"name":"","id":"'+ id +'"}').tap()

    def find_text(self, keyword):
        return FindText(self.socket,self.request_separator,self.request_end,self.appium_driver,keyword).execute()

    def find_all_text(self):
        self.NeedPause()
        return FindAllText(self.socket,self.request_separator,self.request_end,self.appium_driver).execute()

    def get_hierarchy(self):
        self.NeedPause()
        return GetHierarchy(self.socket,self.request_separator,self.request_end,self.appium_driver).execute()

        
    def get_inspector(self, id):
        self.NeedPause()
        return GetInspector(self.socket,self.request_separator,self.request_end,self.appium_driver, id).execute()

    def get_server_version(self):
        return GetServerVersion(self.socket, self.request_separator, self.request_end).execute()
    
    '''
    record = 0 停止打点
    record = 1 开始打点
    '''
    def record_profile(self,record):
        RecordProfile(self.socket,self.request_separator,self.request_end,record).execute()

    def record_profile(self):
        if self.profiler_handler == None:
            self.profiler_handler = RecordProfile(self.socket,self.request_separator,self.request_end)
            self.profiler_handler.start()
        else:
            raise Exception("profiler is recording")

    def profile_stop(self):
        if self.profiler_handler != None:
            return self.profiler_handler.stop()
    
    def profile_check(self):
        if self.profiler_handler != None:
            return self.profiler_handler.check()

    def get_unity_version(self):
        return GetUnityVersion(self.socket, self.request_separator, self.request_end).execute()
        
    def del_profile(self):
        if self.profiler_handler != None:
            self.profiler_handler=None

    def profile_abandon_or_upload(self,ab_or_up):
        intab_or_up="2" if ab_or_up else "-1"
        return self.profiler_handler.abandon_or_upload(intab_or_up)

        #深度采集接口
    def profiling_memory(self,value=""):
        return ProfilingMemory(self.socket,self.request_separator,self.request_end,value).execute()

    def get_unity_version(self):
        return GetUnityVersion(self.socket, self.request_separator, self.request_end).execute()

    def get_Game_version(self):
        return GetGameVersion(self.socket, self.request_separator, self.request_end).execute()
    '''
    adb shell dumpsys window | findstr mCurrentFocus
    获取当前正在活动的app
    '''
    def get_current_app_pagename(self):
        res = os.popen(f"adb -s {self.appium_driver} shell dumpsys window | findstr mCurrentFocus").read()
        return "com" + res.split("com")[1].split("/")[0]

    # '''
    # 在app的file中获取全部性能数据
    # '''
    # def get_all_file_from_appfile(self,pagename = ''):
    #     if pagename == '':
    #         pagename = self.get_current_app_pagename()
    #     res = os.popen(f"adb -s {self.appium_driver} shell ls /sdcard/Android/data/{pagename}/files").read()
    #     res = res.split()
    #     res_list = []
    #     for i in res:
    #         if "AutoTest" in i and ".raw" in i:
    #             res_list.append(i)
    #     return res_list

    # '''
    # 由于无法获取每一个打点数据的名称，只能逐个遍历去找AutoTest开头的文件，然后上传
    # '''
    # def pull_profile_data(self,pagename = ''):
    #     res_list = self.get_all_file_from_appfile()
    #     if pagename == '':
    #         pagename = self.get_current_app_pagename()
    #     now_path = os.getcwd()
    #     new_res_list = []
    #     for i in res_list:
    #         #下载到本地
    #         res = os.popen(f"adb -s {self.appium_driver} pull /sdcard/Android/data/{pagename}/files/{i} {now_path}").read()
    #         new_res_list.append(now_path + "\\" +  i)
    #         #删除手机上的数据
    #         os.popen(f"adb -s {self.appium_driver} shell rm /sdcard/Android/data/{pagename}/files/{i}").read()
    #     return new_res_list
    
    # def files_to_zip(self,zip_name,fullname_list):
    #     z = zipfile.ZipFile(zip_name,"w",zipfile.ZIP_DEFLATED)
    #     for file in fullname_list:
    #         #记得删除本地文件
    #         z.write(file)
    #         os.remove(file)
    #     z.close()
    #     return os.getcwd() + "\\" + zip_name

    # def upload_file_to_server(self,file_path):
    #     rep = os.popen(f'curl -X POST -F "file=@{file_path}" http://10.11.164.89:8886/uploadfile').read()
    #     rep_dic = json.loads(rep)
    #     return 'http://10.11.164.89/' + rep_dic['filename:']

    def interrupt(self):
        raise "Interrupt"

    def custom_interface(self, command, *args):
        return CustomInterface(self.socket, self.request_separator, self.request_end, command, *args).execute()

    def get_project_info(self):
        return GetProjectInfo(self.socket, self.request_separator, self.request_end).execute()

    def get_static_methods(self, type_name):
        return GetStaticMethod(self.socket, self.request_separator, self.request_end, type_name).execute()

    def call_static_methods(self, type_name, method_name, parameters):
        return CallStaticMethod(self.socket, self.request_separator, self.request_end, type_name, method_name, parameters).execute()

    def get_constructors(self, type_name):
        return GetConstructor(self.socket, self.request_separator, self.request_end, type_name).execute()
