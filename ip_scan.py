import subprocess, time, re
from termcolor import colored
from netaddr import IPAddress
import ipaddress

class Ip_scan:
    interface = "wlan0"
    my_ip = ""
    my_mask = ""
    my_broadcast = ""
    my_gateway = ""

    ip_occupied = []
    ip_available = []

    def get_gateway(self):
    
        """
        返回本机ip信息到class my_ip, my_mask, my_broadcast
        """
        gateway_info=subprocess.run(f"ip route | grep default | grep {self.interface}",
                                     shell=True, 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE, 
                                     text=True)

        if gateway_info.stderr:
            raise Exception(gateway_info.stderr)

        ip_pattern = r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b"
        gateway_match = re.search(ip_pattern, gateway_info.stdout)
        if gateway_match:
            self.my_gateway = gateway_match.group(1)
            

    def get_ifconfig(self):
        """
        返回本机ip信息到class my_ip, my_mask, my_broadcast
        """

        ip_info=subprocess.run(f"sudo ifconfig {self.interface}",
                             shell=True, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE, 
                             text=True)
                             
 

        # print(ip_info.stdout)

        if ip_info.stderr:
            raise Exception(ip_info.stderr)

        ip_pattern = r'inet\s+((\d+\.){3}\d+)\s+'
        mask_pattern = r'netmask\s+((\d+\.){3}\d+)\s+'
        broadcast_pattern = r'broadcast\s+((\d+\.){3}\d+)'
        ip_match = re.search(ip_pattern, ip_info.stdout)
        mask_match = re.search(mask_pattern, ip_info.stdout)
        broadcast_match = re.search(broadcast_pattern, ip_info.stdout)
        if ip_match and mask_match and broadcast_match:
            self.my_ip = ip_match.group(1)
            self.my_mask = mask_match.group(1)
            self.my_broadcast = broadcast_match.group(1)

        else:
            raise Exception("正则表达式错误 regex error")

    def arp_scan(self):
        print("开始扫描网路所有IP，需时10~60秒，请耐心等待...")
        start_time = time.time()
        arp_info=subprocess.run(f'sudo arp-scan -l --interface={self.interface}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        end_time = time.time()
        print("cost time: ",end_time - start_time)
        
        if arp_info.stderr:
            raise Exception(arp_info.stderr)

        ip_pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
        
        #只取ip填入列表的方法
        ip_occupied = re.findall(ip_pattern, arp_info.stdout)
        self.ip_occupied = ip_occupied
        
    def report(self):
        """
        生成扫描报告：
        列出所有ip的 可用/占用 状态
        生成可用列表 self.ip_available
        """
        print("生成扫描报告")
        print("")

        # 用ip及mask，生成CIDR格式网段
        cidr = IPAddress(self.my_mask).netmask_bits()
        ip_cidr = self.my_ip + '/' + str(cidr)
        local_net = ipaddress.ip_network(ip_cidr, strict=False)
        print("本网段: ", local_net)
        
        ip_count = 2**(32-cidr)-2
        print("此网段总IP数量:", ip_count)
        print("")

        # 列出所有ip的 可用/占用 状态
        # 生成可用列表 self.ip_available
        ip_available = []
        n = range(1,ip_count+1)
        for i in n:
            if str(local_net[i]) in self.ip_occupied:
                text= '已占用: ' + str(local_net[i])
                print(colored(text,'red'))
            else:
                text= '可选用: ' + str(local_net[i])
                print(colored(text,'green'))
                ip_available.append(str(local_net[i]))
        self.ip_available = ip_available

if __name__ == "__main__":
    ip_scan = Ip_scan()
    ip_scan.get_ifconfig()
    print("本机地址: ",ip_scan.my_ip)
    print("子网掩码: ",ip_scan.my_mask)
    print("广播地址: ",ip_scan.my_broadcast)

    ip_scan.arp_scan()
    print(ip_scan.ip_occupied)
    ip_scan.report()

    ip_scan.get_gateway()
    print("gateway: ", ip_scan.my_gateway)
    
