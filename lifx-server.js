var lifx = require('lifx');
var net = require('net');


LifxServer = function(options) {
    this.port = options.port || 8080;
    this.lx = lifx.init();
};

LifxServer.prototype.listen = function() {
    var self = this;
    net.createServer(function(socket) {
        socket.on('data', function(data) {
            self.dispatch(socket,data.toString());
        });
    }).listen(this.port);
    return this;
};

LifxServer.prototype.dispatch = function(socket,data) {
    var self = this;
    var response = '';
    //console.log('request:',data);

    try {
        var request = JSON.parse(data);

        switch(request.operation) {
            case 'state':
                var bulb = self.lx.bulbs[request.bulb];

                switch(request.value) {
                    case 'on':
                        self.lx.lightsOn( bulb );
                        response = 'on';
                        break;
                    case 'off':
                        self.lx.lightsOff( bulb );
                        response = 'off'
                        break;
                }
                break;

            case 'color':
                var color = request.value;
                var bulb = self.lx.bulbs[request.bulb];
                console.log(color.hue)
                var hue = color.hue===undefined ? 0 : Math.floor(color.hue/360*65535)%65536;
                var saturation = color.saturation===undefined ? 0 : Math.floor(color.saturation*65535)%65536;
                var brightness = color.brightness===undefined ? 3000 : Math.floor(color.brightness*65535)%65536
                var temperature = color.temperature===undefined ?  3500 : Math.floor(color.temperature)%65536;
                var fadeTime = color.fadeTime===undefined ? 0 : color.fadeTime;

                //console.log(hue, saturation, brightness, temperature, fadeTime, bulb);
                self.lx.lightsColour( hue, saturation, brightness, temperature, fadeTime, bulb );
                response = 'success';

            case 'query':
                switch(request.value) {
                    case 'bulbs':
                        self.lx.findBulbs();
                        response = self.lx.bulbs;
                        break;
                    case 'voltage':
                        response = 'lots';
                        break;
                }

                break;
                    
            case 'setAll':
                self.lx.lightsColour(0x0000, 0xffff, Math.floor(Math.random()*1000), 0, 0);
                break;
        }
        //console.log('response is',response);
        socket.write( JSON.stringify({response: response}) );
    } catch (e) {
        console.log(data);
        socket.write(JSON.stringify({error: e.toString()}));
    } finally {
        //socket.end();
    }
};


var server = new LifxServer({
    port: 8080
});
server.listen();





