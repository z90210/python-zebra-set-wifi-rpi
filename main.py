import subprocess, re, time
from termcolor import colored
from datetime import datetime

from wifi_scan import Wifi_scan
from ip_scan import Ip_scan
from printer_tools import validate_printer_wifi, find_ssid_in_list, gen_wpa_psk, make_setting_script



print("======================")
print("第一阶段: 获取Wifi信息")
print("======================")

print("先将本机连接上打印机要使用的WiFi")
print("确认本机右上角WiFi状态显示已连结")
input("现在开始获取本机WiFi状态，按Enter开始:")
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
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("请将本画面拍照保存，方便日后除错")
input("按Enter继续:")
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
        ip_scan.get_gateway()
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
print("    网关: ",ip_scan.my_gateway)
print("")

input("扫描本网路其他IP状态，按Enter开始:")
ip_scan.arp_scan()
#print(ip_scan.ip_occupied)
ip_scan.report()


print("======================")
print("第三阶段:   配置打印机")
print("======================")

print("当前连接SSID: ", colored(wifi.current_ssid, "green"))

printer_wifi = find_ssid_in_list(wifi.wifi_dicts, wifi.current_ssid)
print(printer_wifi)
print()

printer_ok = validate_printer_wifi(printer_wifi)
print("从上面可用IP列表,复制或输入绿色的可用IP")
print("尽量从连续绿色、无占用的范围挑选IP，避免日后IP重复问题")

while True:
    ip_raw = input("输入或贴上IP后按Enter: ")
    ip_regexed = re.search(r"((\d+\.){3}\d+)",ip_raw)

    if ip_regexed:
        printer_ip = ip_regexed.group(1)
        print("IP格式正确:",printer_ip)
        
        if printer_ip in ip_scan.ip_available:
            print("此IP在可用列表中")
            break
        else:
            print("此IP不在可用列表中，请重新挑选上方列表内绿色IP")

print()
wifi_password = input(f"输入{wifi.current_ssid}的WiFi密码: ")
psk = gen_wpa_psk(wifi.current_ssid, wifi_password)
print("PSK_RAW: ",psk)


zpl = make_setting_script(
            wifi.current_ssid, 
            psk, 
            printer_ip, 
            ip_scan.my_mask, 
            ip_scan.my_gateway)
print()
print("打印机配置内容:")
print("======================")
print(zpl)
print("======================")

f = open("wifi.zpl", "w")
f.write(zpl)
f.close()


print('准备写入Printer,请确认USB线已连接好本电脑与打印机')
print('打印机己开机，并且已在待机状态')

input('确认完成，请按Enter开始写入配置档到打印机')

print()

while True:
    w=subprocess.run("echo wifi.zpl > /dev/usb/lp0",
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 text=True)

    if w.stderr:
        input("写入错误，检查打印机待机/USB连线,重试请按Enter")
        break
    else:
        break


print('写入完成')
print(colored(f'请将打印机固定IP: {printer_ip} 标记在打印机上',"green"))

time.sleep(5)
print('随后启动浏览器，查看打印机IP')
print('如能在浏览器看到打印机内置网页')
print('即表示配置成功')
print()
print('等待10秒，打印机重启中...')

timer =10
while (timer>=0):
    print(f"\r 等待 {timer}秒   ", end="")
    timer -= 1
    time.sleep(1)

print()


printer_ip="192.168.50.1"
command = f"export DISPLAY=:0.0; firefox-esr http://{printer_ip}"
p=subprocess.Popen(command, shell=True, text=True)
