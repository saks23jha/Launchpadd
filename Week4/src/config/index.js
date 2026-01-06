import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";

// __dirname equivalent in ES Modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env file
dotenv.config({
  path: path.resolve(__dirname, "../.env") // assumes .env is in src/ or adjust path
});

// Named exports
export const mongoUri = process.env.MONGO_URI;
export const port = process.env.PORT || 3000;
