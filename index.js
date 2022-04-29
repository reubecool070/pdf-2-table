const express = require("express");
const { pdf2TableConverter } = require("./Controller/pdf.controller");
const fs = require("fs");
const output = require("./Controller/output");

const app = express();
app.use(express.json());
const PORT = 8080;

app.get("/", (req, res, next) => {
  res.status(200).send("Hello Track OS testing!");
});
// app.use("/api", apiRoutes);
app.post("/api/pdf", async (req, res, next) => {
  await pdf2TableConverter(req.body.url);
  const readFile = fs.readFileSync("./Controller/output", "utf-8");
  const parseFile = JSON.parse(readFile);
  fs.writeFileSync("./Controller/output", JSON.stringify({}));
  res.status(200).json(parseFile);
});

app.listen(PORT, () => {
  console.log(`server listening at port ${PORT}`);
});
