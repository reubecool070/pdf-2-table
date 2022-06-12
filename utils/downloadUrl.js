var http = require("https");
var fs = require("fs");

var download_image = function (url, dest) {
  var file = fs.createWriteStream(dest);
  http.get(url, function (response) {
    response.pipe(file);
    file.on("finish", function () {
      console.log("downloaded");
      // file.close(cb);
    });
  });
};

module.exports = download_image;
