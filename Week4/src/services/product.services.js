import Product from "../models/Product.js";
export const getProducts = async (query) => {
  const {
    search,
    searchBy = "name",
    condition = "or", 
    sortBy = "createdAt",
    order = "desc",
    page = 1,
    limit = 10,
    includeDeleted = "false",
    minPrice,
    maxPrice,
    ...filters
  } = query;

  const mongoQuery = {};

  // Soft delete  //
  if (includeDeleted !== "true") {
     mongoQuery.deletedAt = null;


  }

  //  Search
  if (search) {
    const fields = searchBy.split(",");

    const searchConditions = fields.map((field) => ({
      [field]: { $regex: search, $options: "i" },
    }));

    mongoQuery[condition === "and" ? "$and" : "$or"] = searchConditions;
  }

  //  Price Filter
  if (minPrice || maxPrice) {
    mongoQuery.price = {};

    if (minPrice) {
      mongoQuery.price.$gte = Number(minPrice);
    }

    if (maxPrice) {
      mongoQuery.price.$lte = Number(maxPrice);
    }
  }

  //  Other Filters
  Object.keys(filters).forEach((key) => {
    mongoQuery[key] = filters[key];
  });

  //  Pagination
  const skip = (Number(page) - 1) * Number(limit);

  //  Sorting
  const sortOrder = order === "asc" ? 1 : -1;

  const [data, total] = await Promise.all([
    Product.find(mongoQuery)
      .sort({ [sortBy]: sortOrder })
      .skip(skip)
      .limit(Number(limit)),
    Product.countDocuments(mongoQuery),
  ]);

  return {
    data,
    meta: {
      total,
      page: Number(page),
      limit: Number(limit),
      totalPages: Math.ceil(total / limit),
    },
  };
};
