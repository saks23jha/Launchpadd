import OrderRepository from "../repositories/order.repository.js";

export const createOrder = async (req, res) => {
  const order = await OrderRepository.create(req.body);

  return res.status(201).json({
    success: true,
    data: order,
  });
};

export const getOrders = async (req, res) => {
  const orders = await OrderRepository.findAll();

  return res.status(200).json({
    success: true,
    data: orders,
  });
};
