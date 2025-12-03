const os = require("os");
const { exec } = require("child_process");
 
function getHostName() {
  console.log("Host Name");
  console.log(os.hostname());
}
 
function getDiskSpace() {
  exec("df -h /", (err, stdout) => {
    console.log("Available Disk Space");
    if (err) return console.log("Error:", err.message);
    console.log(stdout);
  });
}
 
function getOpenPorts() {
  exec("ss -tuln | awk 'NR>1 {print $5}' | head -5", (err, stdout) => {
    console.log("Open Ports (Top 5)");
    if (err) return console.log("Error:", err.message);
    console.log(stdout);
  });
}

 
function getLoggedInUser() {
  console.log("Logged-in User");
  console.log(os.userInfo().username);
}
 
function getDefaultGateway() {
  exec("ip route | grep default", (err, stdout) => {
    console.log("Default Gateway");
    if (err) return console.log("Error:", err.message);
    console.log(stdout);
  });
}
 
function getNetworkInterfaces() {
  console.log("Network Interfaces");
  console.log(os.networkInterfaces());
}
 
getHostName();
getDiskSpace();
getOpenPorts();
getLoggedInUser();
getDefaultGateway();
getNetworkInterfaces();
 
 