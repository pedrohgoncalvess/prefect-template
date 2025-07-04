# Prefect Project Template

This repository provides a structured template for building data pipelines using [Prefect](https://www.prefect.io/). It includes task and flow definitions, logging, testing, database connectivity, and containerized services with Docker Compose.

---

## Requirements

- Docker & Docker Compose
- Make

---

## Project Structure

```
.
├── tasks/                        # Modular task definitions
├── flows/                        # Flow orchestration scripts
├── tests/                        # Unit tests for connections and flows
├── log/                          # Logging configuration and output logs
│   └── config.py                 # Log format, handlers, and levels
├── docker-compose.yaml           # Prefect server and agent services
├── docker-compose.ext-services.yaml  # External services (PostgreSQL, MinIO)
├── requirements.prefect.txt      # Prefect-related dependencies
├── database/                     # DB connection and migration scripts
│   ├── connection.py
│   └── migrations/
└── README.md
```

---

## Features

- **Modular Design:** Easily scalable with separate directories for tasks and flows.
- **Logging:** Centralized configuration and persistent log storage.
- **Testing:** Includes flow and connection tests for improved reliability.
- **Dockerized:** All services are containerized for fast setup and consistent environments.
- **External Services:**
  - PostgreSQL for persistent storage.
  - MinIO for object storage (S3-compatible).
- **Database Module:** Handles connection setup and migration control.

---

## Running the Project with Docker Compose

### 1. Start Prefect Infrastructure. 
#### Obs: external services (Pg and MinIO) are included in docker-compose.yaml.

```bash
docker-compose up -d
```

This will start Prefect-related containers (e.g., Prefect server, agent).

---

## Running Tests

To execute connection and flow tests:

```bash
pytest tests/
```

---

## Installing Dependencies

To install dependencies for the Prefect executor environment:

```bash
pip install -r requirements.prefect.txt
```

---

## Configuration

- **Logging:** Controlled via `log/config.py`.
- **Environment Variables:** You may define a `.env` file or inject variables using Docker Compose.

---

## Notes

- The `database/` module includes everything you need to establish a PostgreSQL connection and manage schema migrations (e.g., using Alembic).
- MinIO can be accessed via its web UI or via any S3-compatible client using the credentials and endpoint configured in the compose file.

---

## Contributions

Feel free to fork, extend, or contribute back to this template to help others build robust data workflows faster.

---

## Development Environment Setup

This project uses [uv](https://github.com/astral-sh/uv) for managing the Python environment and dependencies. A `Makefile` is included to simplify the setup process across Windows and Unix-based systems.

### Prerequisites

- Python 3.12.6 must be installed.
- `make` must be available on your system.

### Available Makefile Targets

- `make setup`: Creates a virtual environment using UV and installs all dependencies.
- `make run`: Sets up the environment and runs the main script (`main.py`).
- `make clean`: Removes the virtual environment.
- `make check-uv`: Checks if UV is installed; installs it if missing.
- `make install-uv`: Installs UV manually.
- `make create-venv`: Creates or recreates the `.venv` virtual environment.

### Example Usage

```bash
make setup      # Sets up everything from scratch
make run        # Runs the main application
make clean      # Deletes the virtual environment
```

The Makefile detects the operating system and adjusts the commands accordingly. It ensures UV is installed before creating the virtual environment and syncing dependencies.

---

## License

This project is open source and available under the [MIT License](LICENSE).