const http = require("http");

const PORT = 3000;
const INSTANCE = process.env.INSTANCE_NAME;

http.createServer((req, res) => {
  res.end(`Response from ${INSTANCE}`);
}).listen(PORT, () => {
  console.log(`Backend ${INSTANCE} running on port ${PORT}`);
});
