// const { PythonShell } = require("python-shell");
let { spawn } = require("child_process");
const path = require("path");

const pdf2TableConverter = async (url) => {
  try {
    const tabletoJSON = await pythonPromise(url);

    return tabletoJSON;
  } catch (error) {
    return error;
  }
};

const pythonPromise = (url) => {
  return new Promise(function (resolve, reject) {
    let data1 = [];
    const py = spawn("python3", [path.join(__dirname, "pyfile/gct.py"), url]);
    py.stdout.on("data", function (data) {
      if (Object.keys(data).length > 1) {
        data1 = data.toString();
      }
      console.log("python", data);
      console.log(typeof data);
      //  data1 =  data.toString()
    });
    py.on("close", (code) => {
      console.log("closed", new Date().toLocaleString());
      resolve(data1);
      if (!data1) reject([]);
    });
  });
};

module.exports = {
  pdf2TableConverter,
};
