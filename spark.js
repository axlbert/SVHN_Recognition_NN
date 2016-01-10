var Cylon = require('./node_modules/cylon');

Cylon.api('socketio',
{
  host: '0.0.0.0',
  port: '3000'
});


// Initialize the robot
Cylon.robot({
  connections: {
    spark: { adaptor: 'spark', accessToken: '6d70190ba1f56ddce1e3616bd20442b8b859a808', deviceId: '250026000d47343233323032' }
  },

  devices: {
    led: { driver: 'led', pin: 'D0'}
  },

  work: function(my) {
    every((1).second(), function() {my.led.toggle()});
  }
}).start();

