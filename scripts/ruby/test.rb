require 'json'
require 'socket'

lifx = TCPSocket.new 'localhost', 8080

def fade_func(t)
  Math.exp((t.floor-t)*1)
end

lifx.print({
  operation: 'state',
  value: 'on'
})

h = 0.0      # hue
s = 1.0      # saturation
b = 0.0      # brightness
pb = 0.0     # previous brightness
jump = 87.3  # hue jump per beat
bpm = 60.0  # beats per minute
pd = 60.0/bpm
t0 = Time.now.to_f
update_freq = 4.0 # Hz
update_pd = 1.0/update_freq

loop do
  t = Time.now.to_f - t0
  b = fade_func( t*bpm/60.0 )
  h = (t/pd).floor*jump % 360
  f = b-pb > 0 ? 0 : 200
  pb = b

  puts h

  lifx.print({
    operation: 'color',
    value: {
      hue: h,
      brightness: b,
      saturation: 1.0,
      fadeTime: f
    }
  }.to_json)
  
  sleep( update_pd - t%update_pd )
end

