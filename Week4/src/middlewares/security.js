import helmet from "helmet";
import cors from "cors";
import rateLimit from "express-rate-limit";
import express from "express"; // Needed for express.json()

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 3,
  message: "Too many requests, please try again later"
});

const securityMiddleware = (app) => {
  // Security headers
  app.use(helmet());

  // CORS
  app.use(cors({
    origin: "http://localhost:3000",
    methods: ["GET", "POST", "PUT", "DELETE"],
    credentials: true
  }));

  // Rate limiting
  app.use(limiter);

  // Payload limit (10KB)
  app.use(express.json({ limit: "10kb" }));
};

export default securityMiddleware;
