
import express from "express";
import routes from "../routes/index.js";
import securityMiddleware from "../middlewares/security.js";
import errorMiddleware from "../middlewares/errors.middlewares.js";
import tracingMiddleware from "../utils/tracing.js";
import logger from "../utils/logger.js";
import swaggerUi from "swagger-ui-express";
import swaggerSpec from "../config/swagger.js";



const createApp = async () => {
  const app = express();

  logger.info("Initializing middlewares");

  // Core middlewares
  app.use(tracingMiddleware);  
app.use(express.json({ limit: "10kb" }));

  // Security middlewares (helmet, cors, rate limit)
  securityMiddleware(app);

  
  app.use("/docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));
  
  // Routes
  
  app.use("/api", routes);
  app.use((req, res, next) => {
    const error = new Error(`Route not found: ${req.originalUrl}`);
    error.statusCode = 404;
    next(error);
  });



  // Global error handler (should always be after the routes )
  app.use(errorMiddleware);

  logger.info("Application initialized");
  logger.info("Routes mounted: 23 endpoints");


  return app;
};

export default createApp;
