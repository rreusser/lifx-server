var net = require('net');

LifxClient = function() {
    this.port = 8080;
    return this;
};

LifxClient.prototype.connect = function( connectListener ) {
    var self = this;

    self.socket = net.Socket();
    self.socket.connect(self.port,function() {

        if(connectListener !== undefined) {
            connectListener(self.socket);
        }

        self.socket.on('data',function(data) {
            console.log(data.toString());
        });

    });
    return this;
};

LifxClient.prototype.write = function(data,callback) {
    var fNoOp = function() {};
    this.socket.write(data, callback||fNoOp );
    return this;
};


var client = new LifxClient;
client.connect(function(socket) {
    console.log(process.argv[2]);
    socket.write(process.argv[2]);
});


