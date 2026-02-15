import swaggerJsdoc from "swagger-jsdoc";
import path from "path";

const swaggerSpec = swaggerJsdoc({
  definition: {
    openapi: "3.0.0",
    info: {
      title: "Week4 Backend API",
      version: "1.0.0",
      description: "API documentation for Week 4 backend",
    },
    servers: [
      {
        url: "/api",
      },
    ],
  },

  //  FIXED PATH 
  apis: [path.join(process.cwd(), "routes/**/*.js")],
});

export default swaggerSpec;
