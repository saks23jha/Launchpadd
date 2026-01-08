/**
 * GET /users
 */
export const getUsers = async (req, res, next) => {
  try {
    // dummy data for now
    res.status(200).json({
      success: true,
      data: [],
    });
  } catch (error) {
    next(error);
  }
};

/**
 * POST /users
 */
export const createUser = async (req, res, next) => {
  try {
    res.status(201).json({
      success: true,
      message: "User created successfully",
      data: req.body,
    });
  } catch (error) {
    next(error);
  }
};
