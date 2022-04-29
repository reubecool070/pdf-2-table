const { PythonShell } = require("python-shell");
const path = require("path");

const pythonCall = async (url) => {
  const options = {
    mode: "text",
    pythonPath: "python3",
    pythonOptions: ["-u"],
    scriptPath: "./node_modules/pdf2table-json",
    args: url,
  };

  try {
    const response = await new Promise((resolve, reject) => {
      PythonShell.run("gct.py", options, async function (err, results) {
        if (err) {
          reject(err);
        }
        console.log(results);
        resolve(results);
      });
    });

    return response;
  } catch (error) {
    return error;
  }
};

const pdf2TableConverter = async (url) => {
  try {
    console.log("running");
    const tabletoJSON = await pythonCall(url);
    return tabletoJSON;
  } catch (error) {
    return error;
  }
};

module.exports = pdf2TableConverter;
