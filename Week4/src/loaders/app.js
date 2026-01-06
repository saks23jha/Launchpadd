import express from "express";
import routes from "../routes/index.js";
import securityMiddleware from "../middlewares/security.js";
import errorMiddleware from "../middlewares/errors.middlewares.js";

const createApp = async () => {
  const app = express();

  // Global middlewares
  app.use(express.json({ limit: "10kb" }));
  console.log("Middlewares loaded");

  // Security middlewares
  securityMiddleware(app);

  // Routes
  app.use("/api", routes);
  console.log("Routes mounted");

  // Global error handler (MUST be last)
  app.use(errorMiddleware);

  return app;
};

export default createApp;
