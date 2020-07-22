import json
import requests
import base64
import sounddevice as sd
from scipy.io.wavfile import write
import PIL.Image
from io import BytesIO
import numpy as np
from datetime import datetime

startTime = datetime.now()
brt = 0.07
patrick=False

if not patrick:
    import board
    import neopixel


####################
### Record Audio ###
####################

duration = 10  # seconds
fs = 44100
print('Recording...')
recorded = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()

write('output.mp3', fs, recorded)  # Save as WAV file 

print('Done Recording')

#####################
### Get Image URL ###
#####################

image_file= open('./output.mp3',"rb")
image_data_binary = image_file.read()
image_data = (base64.b64encode(image_data_binary))

data = {
    'return': 'apple_music',
    'api_token': '0295a1c0139a030849dd81359d92122a',
    'audio': image_data
}

result = requests.post('https://api.audd.io/', data=data)

response = json.loads(result.text)

try:
    print(response['result']['title'])
    print(response['result']['artist'])
    imgurl = response['result']['spotify']['album']['images'][2]['url']
except:
    print('### error 1 ###')
    print(response)
    imgurl = 'https://i.ibb.co/Q85tMW2/e1.png' # error 1


################################
### Get Image and Manipulate ###
################################

imgresp = requests.get(imgurl)
img = PIL.Image.open(BytesIO(imgresp.content))

img = img.resize((16, 16))

if patrick:
    img.show()

imgpx = np.array(img)
finalpx = []
for ri in range(len(imgpx)):
    if ri % 2 == 1:
        imgpx[ri] = imgpx[ri][::-1]  # flips every 2 rows
    for ci in range(len(imgpx[0])):
        finalpx.append((imgpx[ri][ci][0], imgpx[ri][ci][1], imgpx[ri][ci][2]))


print('Total Time: ' + str(datetime.now() - startTime))

#####################
### Update Pixels ###
#####################

if not patrick:
    pixels = neopixel.NeoPixel(board.D18, 256, brightness = brt)

    j = 0
    step = 256

    # for the life of me, i have no idea why this has to be a loop. i tried pixels = mbdtf and every time it showed funky colors, so here we are
    while j < len(pixels) + 1:
        pixels[j - step:j] = finalpx[j - step:j]
        j += step