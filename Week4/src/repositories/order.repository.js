import Order from "../models/Order.js";

class OrderRepository {
  static async create(data) {
    return Order.create(data);
  }
static async findAll() {
    return Order.find().sort({ createdAt: -1 });
  }
  static async findByAccountId(accountId, { limit = 10, cursor }) {
    const query = { accountId };

    if (cursor) {
      query.createdAt = { $lt: new Date(cursor) };
    }

    return Order.find(query)
      .sort({ createdAt: -1 })
      .limit(Number(limit));
  }

  static async findDelivered() {
    return Order.find({ deliveredAt: { $ne: null } });
  }
}

export default OrderRepository;
