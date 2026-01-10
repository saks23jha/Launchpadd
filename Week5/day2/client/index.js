const http = require("http");

http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/html" });
  res.end(`
    <h2>Client</h2>
    <button onclick="goToServer()">Go to Server</button>

    <script>
      function goToServer() {
        window.location.href = "http://localhost:5000";
      }
    </script>
  `);
}).listen(3000, () => console.log("Client running on port 3000"));
