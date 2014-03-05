import socket
import time
import json
import random
import math

lifx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lifx.connect(('localhost', 8080))

def send(command):
  lifx.send(json.dumps(command)+'\n')

def fadefunc(t):
  return math.exp((math.floor(t)-t)*1)
  

h = 0.0      # hue
s = 1.0      # saturation
b = 0.0      # brightness
pb = 0.0     # previous brightness
jump = 87.3  # hue jump per beat
bpm = 60.0  # beats per minute
pd = 60.0/bpm
t0 = time.time()
update_freq = 4.0 # Hz
update_pd = 1.0/update_freq

while True:
  t = time.time() - t0
  b = fadefunc( t*bpm/60.0 )
  h = math.floor(t/pd)*jump % 360
  f = 0 if b-pb > 0 else 200
  pb = b

  send({
    'operation': 'color',
    'value': {
      'hue': h,
      'brightness': b,
      'saturation': 1.0,
      'fadeTime': f
    }
  })
  
  time.sleep( update_pd - t%update_pd )
