# Readify-Backend FastAPI



## Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
    - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL 
    database.
    - [Redis](https://redis.io/) as in memory caching
    
    - [SQLELECTRON](https://sqlectron.github.io) A simple and  lightweight SQL client desktop/terminal with cross database and platform support

    -[Postman](https://www.postman.com/) Postman is an API platform for building and using APIs. It offers a set of tools, a repository, workspaces, and governance to simplify and streamline the API lifecycle.


- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default.
- 🔑 JWT (JSON Web Token) authentication.
- 📫 Email based password recovery.
- ✅ Tests with [Pytest](https://pytest.org).

- 🚢 Deployment instructions using Docker Compose, including how to set up a frontend Traefik proxy to handle automatic HTTPS certificates.
- 🏭 CI (continuous integration) and CD (continuous deployment) based on GitHub Actions.
