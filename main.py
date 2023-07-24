from m5stack import *
import urequests
import blocky18b20
from uiflow import *
import wifiCfg


ssid = ''
key = ''

node_name = 'm5stack-1'
api_key = ''
base_url = 'http://emoncms.org'

print("Connecting to {} wifi network".format(ssid), end='')
wifiCfg.doConnect(ssid, key)

while not wifiCfg.wlan_sta.isconnected():
        elapsed_time += 1
        print('.', end='')
        time.sleep(1)
        
print()
print(wifiCfg.wlan_sta.ifconfig())

def send_emoncms_data(timer):   
    blocky18b20.convert(32)
    temperature = blocky18b20.read(32)

    # Define the data to be sent in the POST request
    data = {
        "node": node_name,
        "data": {
            "temperature": temperature
        },
        "apikey": api_key
    }

    # Convert the data to a URL-encoded string
    data_str = "&".join(["{}={}".format(key, value) for key, value in data.items()])


    # Specify the URL
    url = "http://emoncms.fr/input/post"

    # Set the content type header
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }


    if wifiCfg.wlan_sta.isconnected():
        # Send the HTTP POST request
        response = urequests.post(url, data=data_str, headers=headers)

        # Print the response content (optional)
        print(response.text)
        if 'ok' in response.text:
            rgb.setColorAll(0x33cc00)
        else:
            rgb.setColorAll(0xcc0000)
            

        # Close the response to release resources (important in MicroPython)
        response.close()
    else:
        rgb.setColorAll(0xcc0000)
        wifiCfg.reconnect()


blocky18b20.init(32)
send_emoncms_data(None)

timerSch.timer.init(period=10000, mode=timerSch.timer.PERIODIC, callback=send_emoncms_data)