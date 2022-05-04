const express = require("express");
const { pdf2TableConverter } = require("./Controller/pdf.controller");
const fs = require("fs");

const app = express();
app.use(express.json());
const PORT = 8080;

app.get("/", (req, res, next) => {
  res.status(200).send("Hello Track OS testing!");
});
// app.use("/api", apiRoutes);
app.post("/api/pdf", async (req, res, next) => {
  const response = await pdf2TableConverter(req.body.url);
  // const readFile = fs.readFile("./Controller/output.json", "utf-8");
  const parseFile = JSON.parse(response);
  // fs.writeFileSync("./Controller/output.json", JSON.stringify([]));
  res.status(200).json(parseFile);
});

app.listen(PORT, () => {
  console.log(`server listening at port ${PORT}`);
});