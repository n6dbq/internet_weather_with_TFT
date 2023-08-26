import network
import urequests
import secrets #separate file to store SSID & PASSWORD
import glcdfont
from ili934xnew import ILI9341, color565
import tt24
import time
from machine  import Pin,SPI,ADC
redPin=2
greenPin=3
bluePin=4
redLed=Pin(redPin,Pin.OUT)
greenLed=Pin(greenPin,Pin.OUT)
blueLed=Pin(bluePin,Pin.OUT)

SCR_WIDTH = const(320)
SCR_HEIGHT = const(240) 
SCR_ROT = const(3)
CENTER_Y = int(SCR_WIDTH/2)
CENTER_X = int(SCR_HEIGHT/2)
TFT_CLK_PIN = const(6)
TFT_MOSI_PIN = const(7)
TFT_MISO_PIN = const(4)
TFT_CS_PIN = const(13)
TFT_RST_PIN = const(14)
TFT_DC_PIN = const(15)              
fonts = [glcdfont,tt24]
spi = SPI(0,baudrate=40000000,miso=Pin(TFT_MISO_PIN)
      ,mosi=Pin(TFT_MOSI_PIN),sck=Pin(TFT_CLK_PIN))
display = ILI9341(spi,cs=Pin(TFT_CS_PIN),dc=Pin(TFT_DC_PIN)
            ,rst=Pin(TFT_RST_PIN),w=SCR_WIDTH,h=SCR_HEIGHT,r=SCR_ROT)
wlan=network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID,secrets.PASSWORD)
try:    
    while wlan.isconnected==False:     
        display.set_font(tt24)
        display.set_color(color565(0, 0, 0), color565(150, 150, 150))
        display.set_pos(20,0)
        display.print('..... Connecting')
    display.set_font(tt24)
    display.set_color(color565(0, 0, 0), color565(150, 150, 150))
    display.set_pos(20,0)    
    display.print('... Connected')
    #weatherData=urequests.get("https://api.openweathermap.org/data/2.5/weather?lat={Latatude}&lon={longitude}&appid={openweathermap id}f&units=imperial").json()   
    #Testing Data
    weatherData={'timezone': -25200, 'sys': {'type': 2, 'sunrise': 1692708777, 'country': 'US', 'id': 2044020, 'sunset': 1692756106}, 'base': 'stations', 'main': {'temp_min': 97.2, 'pressure': 1013, 'feels_like': 103.64, 'humidity': 28, 'temp_max': 103.00, 'temp': 101.48}, 'visibility': 10000, 'id': 5288661, 'clouds': {'all': 4}, 'coord': {'lon': -111.06, 'lat': 32.34}, 'name': 'Casas Adobes', 'cod': 200, 'weather': [{'id': 800, 'icon': '01d', 'main': 'Clear', 'description': 'clear sky'}], 'dt': 1692738013, 'wind': {'gust': 10, 'speed': 4, 'deg': 143}}
    print(weatherData)
    
    t=((weatherData['main']['temp']))
    hum=(weatherData['main']['humidity'])
    maxT=((weatherData['main']['temp_max']))
    minT=((weatherData['main']['temp_min']))
    pressure=(weatherData['main']['pressure']*0.0009869233)
    wind=(weatherData['wind']['speed'])
    desc=(weatherData['weather'][0]['description'])
    adc = machine.ADC(4) 
    ADC_voltage = adc.read_u16() * (3.3 / (65536))
    time.sleep(.25)
    temperature_celcius = round(27 - (ADC_voltage - 0.706)/0.001721)
    temp_fahrenheit=round(32+(1.8*temperature_celcius))    
    print("Temperature: {}°C {}°F".format(temperature_celcius,temp_fahrenheit))
    
    while True:
        if maxT>110 or t>110:
            redLed.value(True)
            greenLed.value(False)
            blueLed.value(False)
            alarm=1
        else:
            redLed.value(False)
            greenLed.value(True)           
            blueLed.value(False)
            alarm=0
        display.set_font(tt24)
        display.set_color(color565(0, 0, 0), color565(150, 150, 150))
        display.set_pos(20,0)
        display.print("Location text      ")
        display.print("Temp: {} deg F".format(round(t)))
        display.print("Humidity: {} %".format(round(hum)))
        display.print("Max Temp: {} deg F".format(round(maxT)))
        display.print("Min Temp: {} deg F".format(round(minT)))
        display.print("Pressure: {} ATM".format(pressure))
        display.print('Wind Speed: {} MPH'.format(wind))
        display.print('Local: {}'.format(desc))
        display.print("Indoor Temp: {} F".format(temp_fahrenheit))
        if alarm==1:
            display.print('Excessive Heat')
        
except KeyboardInterrupt:
    print('Done')
    display.erase()
