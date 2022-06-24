from termcolor import colored
from passlib.utils import pbkdf2
import binascii

def find_ssid_in_list(wifi_list, ssid):
    """
    找到Wifi列表中第一个相同ssid名的 dictionary
    """
    for d in wifi_list:
        print(d['ssid'])
        if d['ssid'] == ssid:
            return d
    else:
        raise Exception("ssid not found in the list!")

def validate_printer_wifi(wifi):
    if wifi['encrypted'] == "off":
        print(colored("[ OK ] 此WiFi未加密","green"))
        print(colored("可进行配置","green"))
        return True

    elif wifi['encrypted'] == "on":
        print(colored("[ OK ] 此WiFi已加密","green"))
        if wifi['psk']:
            print(colored("[ OK ] 加密方式 WPA/WPA2 - PSK","green"))

            print("可进行配置")
            return True
        else:
            print(colored("[ NG ] 特殊加密方式","red"))
            print("本配置软件不支持此加密方式")
            print("请用改斑马原装专用配置软件，进行配置")
            print("或将WiFi改用常见的WPA/WPA2 PSK加密")
            return False


def gen_wpa_psk(SSID, WPA_SECRET):
#    SSID="Ashcloud"
#    WPA_SECRET="Passw0rd@1213|0412"
    WPA_PSK_KEY = pbkdf2.pbkdf2(str.encode(WPA_SECRET), str.encode(SSID), 4096, 32)
    WPA_PSK_RAWKEY = binascii.hexlify(WPA_PSK_KEY).decode("utf-8").upper()
    #print(WPA_PSK_RAWKEY)
    return WPA_PSK_RAWKEY


def make_setting_script(ssid, psk, ip, mask, gateway):
    """
    产生zpl配置档 
    ssid, psk, ip, mask, gateway
    """
    ssid=ssid
    psk=psk
    zpl = f"""
^XA
^JUF
^WIP,{ip},{mask},{gateway}
^NC2
^NPP
^KC0,0,,
^WAD,D
^WEOFF,1,,,,,,
^WP0,0
^WR,,,,100
^WS{ssid},I,L,,,
^NBS
^WLOFF,,
^WKOFF,,,,
^WX09,{psk}
^XZ
^XA
^JUS
^XZ
! U1 setvar "wlan.country_code" "china"
! U1 setvar "wlan.international_mode" "off"
! U1 setvar "wlan.allowed_band" "all"
! U1 do "device.reset" ""
    """
    return zpl

        
if __name__ == "__main__":

    test_wifi = {
        'id': 1, 
        'ssid': 'AshCloud', 
        'frequency': '2.417', 
        'quality': '70/70', 
        'channel': '2', 
        'bssid': '08:62:66:91:66:B8',
        'encrypted': 'on', 
        'rssi': '-32', 
        'psk': False, 
        'band': '2.4 Ghz'
        }

    validate_printer_wifi(test_wifi)
