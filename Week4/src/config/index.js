const path = require('path');
const dotenv = require('dotenv');

dotenv.config({
  path: path.join(process.env.HOME, '.week4.env')
});

module.exports = {
  port: process.env.PORT,
  mongoUri: process.env.MONGO_URI
};

