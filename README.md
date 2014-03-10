# lifx-server

This is a very minimal server built on the NodeJS client at https://www.npmjs.org/package/lifx. I want to do so many cool things with my lightbulbs, but I don't know how to do most of them in Javascript (hardware in particular!), so I wanted an abstraction layer. My solution was to create a thin server layer that receives simple JSON requests via TCP and dispatches the results via the NodeJS client. I'm sure someone can do a million times better; I just want to talk to my bulbs!

Demo (source code in scripts/python/audio.py): http://instagram.com/p/lJf0z7GZ1w/
## Install

The server is just a thin shell around the (outstanding!) LIFX nodejs package at https://www.npmjs.org/package/lifx, so you obviously need to have that installed:

  $ npm install lifx

## Run

To start the server and connect to your bulbs:

    $ node lifx-server.js

To run the sample programs:

    $ python scripts/python/test.py
    $ ruby scripts/ruby/test.py

## License

License? Do what you want. Let me know. Give credit to the guy who reverse-engineered the protocol. MIT? Sure. Yeah, that sounds like a thing people do. MIT.
