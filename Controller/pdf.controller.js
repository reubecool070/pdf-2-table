const { PythonShell } = require("python-shell");

const pdf2TableConverter = async (url) => {
  try {
    const tabletoJSON = await pythonCall(url);

    return tabletoJSON;
  } catch (error) {
    console.log(error);
    return error;
  }
};

const pythonCall = async (url) => {
  const options = {
    mode: "text",
    pythonPath: "python3",
    pythonOptions: ["-u"],
    // scriptPath: `${__dirname}`,
    scriptPath: `./Controller`,
    args: url,
  };
  try {
    const response = await new Promise((resolve, reject) => {
      PythonShell.run("gct.py", options, async function (err, results) {
        if (err) {
          reject(err);
        }
        resolve(results);
      });
    });

    return response;
  } catch (error) {
    console.log(error);
    return error;
  }
};

module.exports = {
  pdf2TableConverter,
};
