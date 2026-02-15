const http = require("http");
const mongoose = require("mongoose");

mongoose
  .connect("mongodb://mongo:27017/day2db")
  .then(async () => {
    console.log("Connected to MongoDB");

    const TestSchema = new mongoose.Schema({
      message: String,
    });

    const Test = mongoose.model("Test", TestSchema);

    await Test.create({ message: "Hello from Day2" });
  })
  .catch(err => console.error("Mongo error:", err));

http.createServer((req, res) => {
  res.end("Server connected to MongoDB");
}).listen(5000, () => console.log("Server running on port 5000"));
