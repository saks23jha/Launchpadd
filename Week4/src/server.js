const { port } = require('./config');
const createApp = require('./loaders/app');
const connectDB = require('./loaders/db');

const startServer = async () => {
  await connectDB(); // FIRST connect DB

  const app = await createApp();

  app.listen(port, () => {
    // console.log('Database connected');
    console.log(`Server running on port ${port}`);
  });
};

startServer();
