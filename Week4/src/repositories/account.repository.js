import Account from "../models/Account.js";

class AccountRepository {
  static async create(data) {
    return Account.create(data);
  }

  static async findById(id) {
    return Account.findById(id);
  }

  static async findPaginated({ status, limit = 10, cursor }) {
    const query = {};

    if (status) {
      query.status = status;
    }

    if (cursor) {
      query.createdAt = { $lt: new Date(cursor) };
    }

    return Account.find(query)
      .sort({ createdAt: -1 })
      .limit(Number(limit));
  }

  static async updateById(id, data) {
    return Account.findByIdAndUpdate(id, data, {
      new: true,
      runValidators: true,
    });
  }

  static async deleteById(id) {
    return Account.findByIdAndDelete(id);
  }
}

export default AccountRepository;
