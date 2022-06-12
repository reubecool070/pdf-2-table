const http = require("https");
const fs = require("fs");

const download_image = function (url, dest) {
  const file = fs.createWriteStream(dest);
  try {
    http.get(url, function (response) {
      response.pipe(file);
      file.on("finish", function () {
        console.log("downloaded");
        // file.close(cb);
      });
    });
  } catch (error) {
    console.log(error);
  }
};

module.exports = download_image;
