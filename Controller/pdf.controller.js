// const { PythonShell } = require("python-shell");
let { spawnSync, spawn } = require("child_process");
const path = require("path");


const pdf2TableConverter = async (url) => {
  try {
    const tabletoJSON = await pythonCall(url);

    return tabletoJSON;
  } catch (error) {
    return error;
  }
};

const pythonPromise = (url) =>{
 return new Promise(function(resolve, reject) {
    let data1 = []
    const py = spawn("python3", [
      path.join(__dirname, "gct.py"),
      url,
    ]);
   py.stdout.on('data', function(data) {
     if (Object.keys(data).length > 1) {
       data1 = data.toString()
       console.log("data============", data1);
      }
      console.log(typeof data);
    //  data1 =  data.toString()
   })
   py.on('close', (code) => {
     console.log("closed");
     resolve(data1)
     if (!data1) reject([])
   })
  })
} 

const pythonCall = async (url) => {
  // const options = {
  //   mode: "text",
  //   pythonPath: "python3",
  //   pythonOptions: ["-u"],
  //   scriptPath: `${__dirname}`,
  //   // args: url,
  // };
  
  
const response = await pythonPromise(url)
return response;
 
};

module.exports = {
  pdf2TableConverter,
};
