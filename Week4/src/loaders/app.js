const express = require('express');
const routes = require('../routes');

module.exports = async () => {
  const app = express();

  app.use(express.json());
  console.log('Middlewares loaded');

  app.use('/api', routes);
  console.log(`Routes mounted: ${routes.routeCount}`);

  return app;
};
