
import { createLogger, format, transports } from 'winston';

const logger = createLogger({
  level: 'info',
  format: format.combine(
    format.timestamp(),
    format.printf(
      ({ level, message, timestamp , requestId}) =>
        `${timestamp} [${level.toUpperCase()}]: ${message} ${requestId ? '[reqId :'+ requestId + ']' : ""}`
    )
  ),
  transports: [
    new transports.Console(),
    // new transports.File({ filename: 'src/logs/app.log' }),
    new transports.File({ filename: 'logs/app.log' }),

  ],
});

export default logger;