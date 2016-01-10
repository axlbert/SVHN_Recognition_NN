

var ViewModel = function(){

  var self = this;

 self.CurrentDist = ko.observable('');
 self.PartCounter = ko.observable();

  self.getMeasure = function() {

    requestURL = "https://api.particle.io/v1/devices/320045000b47343138333038/cm?access_token=6d70190ba1f56ddce1e3616bd20442b8b859a808";
    $.getJSON(requestURL, function(json) {
      //self.CurrentDist.push(json.result);
      //self.CurrentDist.push(json.result);
      self.CurrentDist(json.result);
      self.countItems(json.result);

                 //document.getElementById("tstamp").innerHTML = json.coreInfo.last_heard;

});

};

var counter = 0;
var partlog =[];

self.countItems = function(input){
  if (input < 100){
  partlog.push("1 Piece");
  }
  self.PartCounter(partlog.length);
};


setInterval(function(){ self.getMeasure(); }, 1000);



};




ko.applyBindings(new ViewModel());