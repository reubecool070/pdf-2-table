const http = require("https");
const fs = require("fs");

const download_image = async (url, dest) => {
  const file = fs.createWriteStream(dest);
  http.get(url, function (response) {
    response.pipe(file);

    // after download completed close filestream
    file.on("finish", () => {
      file.close();
      console.log("Download Completed");
    });
  });
};

module.exports = download_image;
