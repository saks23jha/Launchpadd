import createApp from "./loaders/app.js";
import dbLoader from "./loaders/db.js";
import { port } from "./config/index.js";

const startServer = async () => {
  try {
    await dbLoader();
    const app = await createApp();

    app.listen(port, () => {
      console.log(`Server running on port ${port}`);
    });
  } catch (err) {
    console.error("Error starting server:", err);
  }
};

startServer();
