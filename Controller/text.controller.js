const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");
const download_image = require("../utils/downloadUrl");

const pythonPromise = async () => {
  return new Promise(function (resolve, reject) {
    let data1 = [];
    const py = spawn("python3", [path.join(__dirname, "pyfile/apm.py")]);
    py.stdout.on("data", function (data) {
      if (Object.keys(data).length > 1) {
        data1 = data.toString();
      }
    });
    py.on("close", (code) => {
      console.log("closed", new Date().toLocaleString());
      resolve(data1);
      if (!data1) reject([]);
    });
  });
};

// const readFile = async () => {
//   return new Promise(function (resolve, reject) {
//     fs.readFile(__dirname + "/pyfile/text_detection.json", "utf-8", (err, text) => {
//       if (err) reject(err);
//       if (text) resolve(JSON.parse(text));
//     });
//   });
// };

const imagetoTextConverter = async (url) => {
  let imageJSON;
  try {
    console.log(__dirname + "/pyfile/images/empty-1.jpg");
    await download_image(url, `${__dirname}/pyfile/images/empty-1.jpg`).then(async () => {
      imageJSON = await pythonPromise();
    });

    if (typeof imageJSON === "string") {
      return JSON.parse(imageJSON);
    }
    return [];
  } catch (error) {
    return error;
  }
};

module.exports = imagetoTextConverter;
