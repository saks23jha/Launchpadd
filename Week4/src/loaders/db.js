import mongoose from "mongoose";
import logger from "../utils/logger.js";
import Account from "../models/Account.js";

const dbLoader = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI);
     await Account.syncIndexes();
    logger.info("Database connected");
  } catch (error) {
    logger.error("Database connection failed", error);
    process.exit(1);
  }
};

export default dbLoader;
