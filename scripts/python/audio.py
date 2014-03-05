import matplotlib.pyplot as pl
import socket, time, sys, traceback, math, json, random, string, numpy as np
try:
  import audiodev, audiospeex
except:
  print 'cannot load audiodev.so and audiospeex.so, please set the PYTHONPATH'
  traceback.print_exc()
  sys.exit(-1)
  


def getTerminalSize():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])


# Connect to LIFX:

lifx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lifx.connect(('localhost', 8080))

def send(command):
  lifx.send(json.dumps(command)+'\n')


last_update = 0
last_hue_change = 0


levels = [0,0,0,0]
slow_level = 1.0
fast_level = 1.0
slow_fade = 0.985
fast_fade = 0.8
variance = 0.1
hue = random.random()*360
hue_index = 1


def colorwheel(hue):
  if hue < 30:
    return 1 # red
  elif hue < 80:
    return 3 # yellow
  elif hue < 150:
    return 2 # green
  elif hue < 200:
    return 6 # cyan
  elif hue < 260:
    return 4 # blue
  elif hue < 330:
    return 5
  else:
    return 1



def inout(fragment, timestamp, userdata):
  global f, d, slow_level, slow_fade, fast_level, fast_fade, variance, std, n, levels, last_update, last_hue_change, hue, hue_index
  try:
    data = np.fromstring(fragment, dtype='int16')
    f = data
    lev = np.std(data)
    d = np.fft.rfft(data)
    l = np.linalg.norm(d)

    fast_level *= fast_fade
    fast_level += (1.0-fast_fade)*l

    slow_level *= slow_fade
    slow_level += (1.0-slow_fade)*l

    error2 = (fast_level - slow_level)**2
    variance *= slow_fade
    variance += (1-slow_fade)*error2

    std = math.sqrt(variance)

    # Clip to prevent instability when quiet:
    std = np.max([std,8000])

    level_offset = (fast_level-slow_level)/std
    bigness = 0.5 + 0.5*level_offset

    levels.append(bigness)

    hueChange = False
    if level_offset > 1.5 and time.time() - last_hue_change > 0.3 and levels[-1] > levels[-2] and levels[-2] > levels[-3]:
      last_hue_change = time.time()
      hue += (60+120*random.random())
      hue %= 360
      hueChange = True


    hue_index = colorwheel(hue)

    (width, height) = getTerminalSize()
    width_factor = 0.1

    o = int(np.clip(np.exp(level_offset*0.6-1.5)*width_factor,-0.5,0.5)*width)
    if o < 0:
      print '[0;3'+str(hue_index)+'m' + ' '*int(width//2+o) + u'\u2588'*(-o)*2
    else:
      print '[0;3'+str(hue_index)+'m' + ' '*int(width//2-o) + u'\u2588'*o*2






    if time.time() - last_update > 0.25:
      last_update = time.time()
      avg = np.clip(np.mean(levels),0,1)
      levels = levels[-2:]

      if True:
        send({
          'operation': 'color',
          'value': {
            'hue': hue,
            'brightness': 0.05 + 0.05 * avg*0.2,
            'saturation': 0.4,
            'fadeTime': 0 if hueChange else 300
          }
        })
      

    #print '*'*int(bigness*10)

    return np.chararray.tostring(data*0)

  except KeyboardInterrupt:
    pass
  except:
    print traceback.print_exc()
    return ""


audiodev.open(output="default", input="default",
          format="l16", sample_rate=44100, frame_duration=20,
          output_channels=2, input_channels=1, flags=0x01, callback=inout)

try:
  while True:
    time.sleep(10)
except KeyboardInterrupt:
  audiodev.close()


#pl.plot(levels)
#pl.show()
