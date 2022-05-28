from termcolor import colored
from wifi_scan import Wifi_scan

wifi = Wifi_scan()
# 查询Wifi接入名
while True:
    try:
        wifi.get_current_ssid()
    except Exception as e:
        print(colored(str(e),"yellow"))
        input("请检查Wifi后按Enter继续:")
    else:
        print("当前连接SSID: ", wifi.current_ssid)
        break


# 查询此地所有Wifi及状态
input("扫描WiFi状态，按Enter继续:")
#print("开始扫描中，请稍候...")

while True:
    try:
        wifi.iwlist_scan()
        wifi.wifi_list_to_dict()
    except Exception as e:
        print(colored(str(e),"yellow"))
        input("请检查Wifi后按Enter继续:")
    else:
        print("扫描完成")
        break

# 显示扫描结果

wifi.print_wifi_table()
