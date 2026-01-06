import express from "express";
import routes from "../routes/index.js";
import errorMiddleware from "../middlewares/errors.middlewares.js";

const createApp = async () => {
  const app = express();

  // Global middlewares
  app.use(express.json());
  console.log("Middlewares loaded");

  // Routes
  app.use("/api", routes);
  console.log(`Routes mounted: ${routes.routeCount}`);

  // Global error handler (MUST be last)
  app.use(errorMiddleware);

  return app;
};

export default createApp;
