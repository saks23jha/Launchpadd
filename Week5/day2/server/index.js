const http = require("http");
const mongoose = require("mongoose");

mongoose
  .connect("mongodb://mongo:27017/day2db")
  .then(() => console.log("Connected to MongoDB"))
  .catch(err => console.error("Mongo error:", err));

http.createServer((req, res) => {
  res.end("Server connected to MongoDB");
}).listen(5000, () => console.log("Server running on port 5000"));
