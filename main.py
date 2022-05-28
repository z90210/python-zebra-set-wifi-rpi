from termcolor import colored
from wifi_scan import Wifi_scan
from ip_scan import Ip_scan

print("======================")
print("第一阶段: 获取Wifi信息")
print("======================")

print("请确认本机右上角Wifi状态显示已连结")
input("获取本机WiFi状态，按Enter开始:")
wifi = Wifi_scan()
# 查询Wifi接入名
while True:
    try:
        wifi.get_current_ssid()
    except Exception as e:
        print(colored(str(e),"yellow"))
        input("请检查Wifi后按Enter继续:")
    else:
        print("当前连接SSID: ", colored(wifi.current_ssid, "green"))
        break


# 查询此地所有Wifi及状态
input("扫描此地WiFi状态，按Enter继续:")
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
print("")
#==================



print("======================")
print("第二阶段: 获取 IP 信息")
print("======================")
#IP扫描
input("扫描本机IP状态，按Enter开始:")

ip_scan = Ip_scan()
ip_scan.interface = "wlan0"
while True:
    try:
        ip_scan.get_ifconfig()
    except Exception as e:
        print(colored(str(e),"yellow"))
        input("请检查Wifi后按Enter继续:")
    else:
        print("扫描完成")
        break


print("")
print("本机地址: ",ip_scan.my_ip)
print("子网掩码: ",ip_scan.my_mask)
print("广播地址: ",ip_scan.my_broadcast)
print("")

input("扫描本网路其他IP状态，按Enter开始:")
ip_scan.arp_scan()
#print(ip_scan.ip_occupied)
ip_scan.report()


print("======================")
print("第三阶段:   配置打印机")
print("======================")

print("当前连接SSID: ", colored(wifi.current_ssid, "green"))

