import { randomUUID } from "crypto";
import logger from "./logger.js";

const tracingMiddleware = (req, res, next) => {
  const requestId = req.headers["x-request-id"] || randomUUID();

  req.requestId = requestId;
  res.setHeader("X-Request-ID", requestId);

  logger.info(`${req.method} ${req.originalUrl}`, { requestId });
  next();
};

export default tracingMiddleware;
