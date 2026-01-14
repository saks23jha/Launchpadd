import express from "express";
import { MongoClient } from "mongodb";

const app = express();
const PORT = 3000;

const client = new MongoClient("mongodb://mongo:27017");
await client.connect();

const db = client.db("availability_db");
const users = db.collection("users");

// Seed users with availability
await users.deleteMany({});
await users.insertMany([
  { name: "Alice", available: true },
  { name: "Bob", available: false },
  { name: "Charlie", available: true }
]);

app.get("/api/users", async (req, res) => {
  const data = await users.find().toArray();
  res.json(data);
});
app.get("/health", (req, res) => {
  res.status(200).send("OK");
});
app.listen(PORT, () => {
  console.log("User Availability Backend running on port", PORT);
});
