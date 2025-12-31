const logger = require('../utils/logger');

const dbLoader = async () => {
  logger.info('Database connected');
};

module.exports = dbLoader;
