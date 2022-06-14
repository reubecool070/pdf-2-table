const { spawn } = require("child_process");
const path = require("path");

const pythonPromise = async (url) => {
  return new Promise(function (resolve, reject) {
    let data1 = [];
    const py = spawn("python3", [path.join(__dirname, "pyfile/apm.py"), url]);
    py.stdout.on("data", function (data) {
      if (Object.keys(data).length > 1) {
        data1 = data.toString();
      }
    });
    py.on("close", (code) => {
      console.log("closed text detection", new Date().toLocaleString());
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
    const image_url = url.split("?")[0];
    console.log(image_url);
    // await download_image(url, `empty-1.jpg`).then(async () => {
    // });
    imageJSON = await pythonPromise(image_url);

    if (typeof imageJSON === "string") {
      console.log(typeof imageJSON, "type");
      return JSON.parse(imageJSON);
    }
    return [];
  } catch (error) {
    return error;
  }
};

module.exports = imagetoTextConverter;
