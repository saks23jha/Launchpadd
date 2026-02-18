import AccountRepository from "../repositories/account.repository.js";

export const createAccount = async (req, res) => {
  const account = await AccountRepository.create(req.body);

  return res.status(201).json({
    success: true,
    data: account,
  });
};

export const getAccounts = async (req, res) => {
  const accounts = await AccountRepository.findPaginated({});

  return res.status(200).json({
    success: true,
    data: accounts,
  });
};
export const updateAccount = async (req, res) => {
  const account = await AccountRepository.updateById(req.params.id, req.body);

  if (!account) {
    return res.status(404).json({
      success: false,
      message: "Account not found",
    });
  }

  return res.status(200).json({
    success: true,
    data: account,
  });
};


