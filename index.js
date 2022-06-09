const express = require("express");
const { pdf2TableConverter } = require("./Controller/pdf.controller");
const fs = require("fs");
const imagetoTextConverter = require("./Controller/text.controller");

const app = express();
app.use(express.json());
const PORT = 8080;

app.get("/", (req, res, next) => {
  res.status(200).send("Hello Track OS testing!");
});
// app.use("/api", apiRoutes);
app.post("/api/pdf", async (req, res, next) => {
  console.log("called", req.body);
  const response = await pdf2TableConverter(req.body.url);
  // const readFile = fs.readFile(`${__dirname}/output.json`, "utf-8");
  const parseFile = response.length ? JSON.parse(response) : [];
  // fs.writeFileSync("./Controller/output.json", JSON.stringify([]));
  res.status(200).json(parseFile);
});

app.post("/api/imagetotext", async (req, res, next) => {
  console.log(req.body);
  const response = await imagetoTextConverter(req.body.url);

  res.status(200).json({
    data: response,
    status: 200,
    message: "success",
  });
});

app.listen(PORT, () => {
  console.log(`server listening at port ${PORT}`);
});
