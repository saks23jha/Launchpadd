module.exports = {
  apps: [
    {
      name: "week4-backend",
      script: "server.js",
      cwd: "./src",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "300M",
      env: {
        NODE_ENV: "production",
        PORT: 3000
      }
    }
  ]
};
