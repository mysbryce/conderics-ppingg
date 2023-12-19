import pydivert
import ctypes
import time
import os
import random
import hashlib

class App:
    hideConsole = False                                     # ซ่อนหน้าต่าง
    targetIps = ['43.229.148.226']                          # ไอพีเซิฟเวอร์ที่ต้องการใช้
    registered = False                                      # ค่าสำหรับตรวจสอบการกรอกคีย์ (ไม่ต้องปรับ)
    configFile = os.path.join(os.getcwd(), 'Wsl0s9fw')      # ตำแหน่งเก็บไฟล์คีย์
    key = None                                              # สำหรับเก็บคีย์
    keyPass = 'bryce-conderics'                             # คีย์ที่ต้องการให้ผู้ใช้งานกรอก
    
    def __init__(self) -> None:
        self.setTitle('INIT')
        time.sleep(1)
        
        self.setTitle('CHECKING REGISTRATION')
        time.sleep(0.5)
        
        # ตรวจสอบว่าเคยกรอกคีย์ไว้หรือยัง
        if os.path.isfile(self.configFile):
            # อ่านคีย์ภายในไฟล์
            reader = open(self.configFile, 'r')
            self.key = reader.read()
        else:
            # ให้ผู้ใช้งานกรอกคีย์
            self.key = input('\n :: Enter key :: ')
            self.key = hashlib.md5(self.key.encode()).hexdigest()
        
        keyPass = hashlib.md5(self.keyPass.encode()).hexdigest()
        if self.key == keyPass:
            writer = open(self.configFile, 'w')
            writer.write(keyPass)
            writer.close()
            
            self.setTitle('STARTED')
            self.registered = True
        
        # ดึง Handle ของหน้าต่าง
        hWnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hWnd and self.hideConsole:
            self.setTitle('HIDING WINDOWS')
            time.sleep(1)
            
            # ซ่อนหน้าต่าง
            ctypes.windll.user32.ShowWindow(hWnd, 0)
        
        # สามารถใช้โปรแกรมได้
        if self.registered:
            i = 0
            
            ipList = ''
            ipId = 0
            
            # เขียน Statement สำหรับ WinDivert
            for ip in self.targetIps:
                ipId += 1
                if ipId == 1:
                    ipList += ip
                else:
                    ipList += f' or ip.DstAddr = {ip}'
            
            # ใช้งาน WinDivert
            try:
                with pydivert.WinDivert(f'outbound and ip.DstAddr = {ipList}') as w:
                    for packet in w:
                        if random.randrange(1, 100) > 90 or i > 0:
                            i += 1
                            
                            if random.randrange(0, 10) > 3:
                                # หน่วง
                                time.sleep(random.uniform(0.0075, 0.0175))
                            
                            if i == 10:
                                i = 0
                                
                        w.send(packet)

            # กรณีที่ไม่สามารถใช้งาน WinDivert ได้
            except Exception as e:
                print(f'Error : Could not open WinDivert! ({e})')
                time.sleep(1)
                exit(1)
                    
        # ไม่สามารถใช้โปรแกรมได้
        else:
            print('Error : Could not use this program!')
            time.sleep(1)
            exit(1)
    
    def setTitle(self, title):
        ctypes.windll.kernel32.SetConsoleTitleW(f'Ping Loader : {title}')
        
if __name__ == '__main__':
    App() 