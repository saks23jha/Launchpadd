import helmet from "helmet";
import cors from "cors";
import rateLimit from "express-rate-limit";

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,
  message: "Too many requests, please try again later",
  skip: (req) => req.path.startsWith("/docs"),
});

const securityMiddleware = (app) => {
  app.use(helmet());

  app.use(
    cors({
      origin: "http://localhost:3000",
      methods: ["GET", "POST", "PUT", "DELETE"],
      credentials: true,
    })
  );

  app.use(limiter);
};

export default securityMiddleware;
