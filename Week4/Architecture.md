## Application Architecture

This application follows a **loader-based backend architecture** with a single entrypoint responsible for orchestrating system startup.

### Flow

* **Entry File (server.js / index.js)** loads environment configuration, initializes the logger, connects the database, creates the Express app, and starts the server.
* **Database Loader (loaders/db.js)** handles only database connection and logs the status.
* **App Loader (loaders/app.js)** initializes Express, applies core and security middlewares, mounts Swagger docs and application routes, logs route count, and registers the global error handler.
* **Routes Layer (routes/)** contains feature-based routes aggregated via `routes/index.js`.

### Key Principles

* Single entrypoint
* Clear separation of concerns
* Predictable startup order
* Centralized, structured logging

This design mirrors production-ready backend services and satisfies the exercise requirements.
