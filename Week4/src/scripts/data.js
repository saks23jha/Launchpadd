import mongoose from 'mongoose';
import dotenv from 'dotenv';

import Account from '../models/Account.js';
import Order from '../models/Order.js';

dotenv.config();

const seedData = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log('MongoDB connected');

    await Account.deleteMany();
    await Order.deleteMany();

    const accounts = await Account.insertMany([
      {
        firstName: 'Sakshi',
        lastName: 'Jha',
        email: 'sakshi@example.com',
        balance: 500
      },
      {
        firstName: 'Neha',
        lastName: 'Verma',
        email: 'neha@example.com',
        balance: 1200,
        status: 'active'
      }
    ]);

    await Order.insertMany([
      {
        accountId: accounts[0]._id,
        product: 'Laptop',
        amount: 700,
        status: 'completed'
      },
      {
        accountId: accounts[1]._id,
        product: 'Headphones',
        amount: 200,
        status: 'completed'
      }
    ]);

    console.log('Data inserted successfully');
    process.exit(0);
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
};

seedData();
