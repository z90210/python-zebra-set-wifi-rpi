import subprocess
import re
from prettytable import PrettyTable

class Wifi_scan:

    interface = "wlan0"
    current_ssid = ""
    wifi_list = []
    wifi_dicts = []

    def get_group1(self, matched):
        """
        return the group(1) of regex obj or N/A if not matched
        """
        if matched:
            return matched.group(1)
        else:
            return "N/A"

    def wifi_list_to_dict(self):
        """
        传入iwlist列表
        正则转换 dict
        """
        if self.wifi_list:
            print("self.wifi_list已存在,开始转换")
        else: 
            print("self.wifi_list为空，请先运行 iwlist_scan()")
            raise Exception("wifi_list为空")
        essid_pattern = r'ESSID:\"(.*)"'
        freq_pattern = r"Frequency:(\d.\d+)"
        quality_pattern = r"Quality=(\d+/\d+)"
        channel_pattern = r"Channel:(\d+)"
        address_pattern = r"(([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))"
        encrypted_pattern = r"Encryption key:(\w+)"
        rssi_pattern = r"Signal level=(-\d+)"
        
        wifi_dicts = []

        for w in range(len(self.wifi_list)):

            ssid = re.search(essid_pattern, self.wifi_list[w])
            frequency = re.search(freq_pattern, self.wifi_list[w])
            quality = re.search(quality_pattern, self.wifi_list[w])
            channel = re.search(channel_pattern, self.wifi_list[w])
            address = re.search(address_pattern, self.wifi_list[w])
            encrypted = re.search(encrypted_pattern, self.wifi_list[w])
            rssi = re.search(rssi_pattern, self.wifi_list[w])
            psk = "PSK" in self.wifi_list[w]

            freq = self.get_group1(frequency)[0:1]
            if freq == '2':
                band = '2.4 Ghz'
            elif freq == '5':
                band = '5 Ghz'
            else:
                band = 'N/A'

            wifi_dicts.append({
                "id" : w+1,
                "ssid" : self.get_group1(ssid),
                "frequency" : self.get_group1(frequency),
                "quality" : self.get_group1(quality),
                "channel" : self.get_group1(channel),
                "bssid" : self.get_group1(address),
                "encrypted" : self.get_group1(encrypted),
                "rssi" : self.get_group1(rssi),
                "psk" : psk,
                "band" : band
            })
        self.wifi_dicts = wifi_dicts
        return wifi_dicts
# print(wifi_dicts)

    def iwlist_scan(self):
        """
        扫描 Wifi 信息，
        返回Wifi信息列表
        """
        print("开始扫描WiFi...请稍候")
        wireless=subprocess.run("sudo iwlist wlan0 scan", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #    wireless=subprocess.run("ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # print("stderr: ", wireless.stderr)
        # print("stdout: ", wireless.stdout)
        
        #如果stderr有值，发生异常，raise error
        if wireless.stderr:
            raise Exception(wireless.stderr)
        
        # 切割返回内容进 list
        self.wifi_list=wireless.stdout.split('Cell ')[1:]


        # 切割成功返回list ,如内容为空
        if self.wifi_list:
            return self.wifi_list
        else:
            raise Exception("iwlist返回内容格式不符!")

    def get_current_ssid(self, interface="wlan0"):
        """
        取得当前SSID
        interface 选需取值的网卡接口，默认wlan0
        """
        raw=subprocess.run('sudo iwgetid '+interface, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 如果iwgetid取值异常，stderr有值，raise error
        if raw.stderr:
            raise Exception(raw.stderr)
        # print(raw.stdout)
        
        # 正则式取值
        essid_pattern = r'ESSID:\"(.*)"'
        current_ssid_re = re.search(essid_pattern, raw.stdout)
        
        # 正则如果返回空值即报错
        if current_ssid_re:
            current_ssid = self.get_group1(current_ssid_re)
        else:
            raise Exception("取值失败")
            
        self.current_ssid = current_ssid
        
        if current_ssid == "":
            raise Exception("本机未连上任何 WiFi")
        
        return current_ssid


    def print_wifi_table(self):
        """
        Wifi信息，表格显示出来
        """

        if self.wifi_dicts:
            print("self.wifi_dicts已存在, 开始转换")
        else: 
            print("self.wifi_dicts为空，请先运行 wifi_list_to_dict()")
            raise Exception("wifi_list为空")


        t = PrettyTable(['ID','SSID', 'RSSI', 'BAND', 'Ch.', 'Enc.', 'PSK', 'BSSID'])
        for row in self.wifi_dicts:
            t.add_row([row['id'],
                       row['ssid'],
                       row['rssi'],
                       row['band'],
                       row['channel'],
                       row['encrypted'],
                       row['psk'],
                       row['bssid']
                      ])

        t.align["ID"] = "r"    
        t.align["SSID"] = "l"
        t.align["BAND"] = "r"
        t.align['Ch.'] = "r"

        print(t)


if __name__ == '__main__':

    wifi = Wifi_scan()
    wifi.interface = "wlan0"
    
    wifi.get_current_ssid()
    print(wifi.current_ssid)

    wifi_list = wifi.iwlist_scan()

    wifi.wifi_list_to_dict()
    
    # while True:
        # 
        # try:
            # wifi_list = wifi.iwlist_scan()
            # 
        # except Exception as e:
            # 
            # print(type(e))
            # print(e)
# 
            # if "Network is down" in str(e):
                # print("网路没有打开？")
                # 
            # input("请检查Wifi,完成后按Enter继续:")
            # 
        # else:
            # print("成功扫描")
            # break
# 
    # print(wifi.wifi_list)
