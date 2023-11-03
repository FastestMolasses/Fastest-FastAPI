<p align="center">
  <h1 align="center">⚡️ Fastest FastAPI</h1>

  <div align="center">

  ![Build](https://github.com/FastestMolasses/Fast-Python-Server-Template/actions/workflows/main.yaml/badge.svg)&nbsp;[![GitHub license](https://badgen.net/github/license/FastestMolasses/Fast-Python-Server-Template)](https://github.com/FastestMolasses/Fast-Python-Server-Template/blob/main/LICENSE)

  </div>

  <p align="center">
    A production-ready FastAPI server template, emphasizing performance and type safety. It includes a configurable set of features and options, allowing customization to retain or exclude components.
    <br />
    <br />
    Built with FastAPI, Pydantic, Ruff, and MyPy.
    <br />
    <a href="https://github.com/FastestMolasses/Fast-Python-Server-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/FastestMolasses/Fast-Python-Server-Template/issues">Request Feature</a>
  </p>
</p>

## Features

* ⚡ Async and type safety by default
* 🛠️ CI/CD and tooling setup
* 🚀 High performance libraries integrated ([orjson](https://github.com/ijl/orjson), [uvloop](https://github.com/MagicStack/uvloop), [pydantic2](https://github.com/pydantic/pydantic))
* 📝 [Loguru](https://github.com/Delgan/loguru) + [picologging](https://github.com/microsoft/picologging) for simplified and performant logging
* 🐳 Dockerized and includes AWS deployment flow
* 🗃️ Several database implementations with sample ORM models (MySQL, Postgres, Timescale) & migrations
* 🔐 JWT authentication and authorization
* 🌐 AWS Lambda functions support
* 🧩 Modularized features
* 📊 Prometheus metrics
* 📜 Makefile commands
* 🗺️ Route profiling

## Table of Contents

* [Requirements](#requirements)
* [Installation](#installation)
* [Environment Specific Configuration](#environment-specific-configuration)
* [Upgrading Dependencies](#upgrading-dependencies)
* [Databases](#databases)
    * [Shell](#shell)
    * [Migrations](#migrations)
    * [Downgrade Migration](#downgrade-migration)
* [Project Structure](#project-structure)
* [Makefile Commands](#makefile-commands)
* [Contributing](#contributing)

## Requirements

* [Python 3.11+](https://www.python.org/downloads/)
* [Docker](https://www.docker.com/get-started/)

## Installation

1. Fork this repo ([How to create a private fork](https://gist.github.com/0xjac/85097472043b697ab57ba1b1c7530274))

2. Install depedenencies

    Poetry
    ```bash
    poetry install
    ```

    Pip
    ```bash
    python -m venv env

    # Enter environment
    source env/bin/activate # macOS
    .\env\Scripts\activate.ps1 # windows (powershell)

    pip install -r requirements.txt
    ```

3. Enter the environment if you haven't already

    Poetry
    ```bash
    # macOS
    source $(poetry env info --path)/bin/activate

    # windows (powershell)
    & ((poetry env info --path) + "\Scripts\activate.ps1")
    ```
    ```bash
    # Alternatively, you can use this command
    poetry shell
    ```

    Pip
    ```bash
    # macOS
    source env/bin/activate

    # windows (powershell)
    .\env\Scripts\activate.ps1
    ```

4. Install [Docker](https://www.docker.com/get-started/)

5. Start your Docker services

    ```bash
    docker compose up
    ```

6. Clone `.env.example` to `.env` and update the values

    ```bash
    # macOS
    cp .env.example .env

    # windows (powershell)
    copy .env.example .env
    ```

    You can use this command to generate secret keys
    ```bash
    # macOS
    openssl rand -hex 128

    # windows (powershell)
    $bytes = New-Object byte[] 128; (New-Object Security.Cryptography.RNGCryptoServiceProvider).GetBytes($bytes); [System.BitConverter]::ToString($bytes) -Replace '-'
    ```

7. Run the server

    ```bash
    uvicorn main:server --reload
    ```

## Environment Specific Configuration
This project uses environment-specific configuration files and symbolic links to manage different environments such as development, production, and staging. Follow the steps below for your operating system to set up the desired environment.

```bash
# macOS, linux
ln -s <TARGET>.env .env
# example: ln -s prod.env .env

# windows
mklink .env <TARGET>.env
# example: mklink .env prod.env
```

## Upgrading Dependencies

Make sure that Poetry has this `poetry-plugin-up` plugin installed.

```bash
poetry self add poetry-plugin-up
```

Then you can update the latest versions of the dependencies by running this command.

```bash
poetry up
```

You can update dev dependencies by running this command. You can modify this to update other groups as well.

```bash
poetry up --only=dev --latest
```

[More info](https://github.com/MousaZeidBaker/poetry-plugin-up)

## Databases

### Shell

To access the database shell, run this command

```bash
python -i shell.py
```

The `shell.py` script will be loaded including the database session and models.

### Migrations

To do a database migration, follow the steps below.

1. Update `database/models.py` with the changes you want
2. Run this command to generate the migration file in `migrations/versions`

    ```bash
    alembic revision --autogenerate -m "Describe your migration"
    ```

3. Check the newly generated migration file and verify that it generated correctly.
4. Run this command to apply the migration
    ```bash
    alembic upgrade head
    ```

⛔️ Autogenerated migrations cannot detect these changes:

- Changes of table name
- Changes of column name
- Anonymously named constraints
- Special SQLAlchemy types such as Enum when generated on a backend which doesn’t support ENUM directly

[Reference](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect)

These changes will need to be migrated manually by creating an empty migration file and then writing the code to create the changes.

```bash
# Manual creation of empty migration file
alembic revision -m "Describe your migration"
```

### Downgrade Migration

Run this command to revert every migration back to the beginning.

```bash
alembic downgrade base
```

## Project Structure

```
📄 main.py                  - Server entry point
📁 .github/                 - Github specific files
📁 app/                     - Application code
   ├── 📁 api               - API endpoints and middleware
   ├── 📁 auth              - Authentication / authorization
   ├── 📁 cache             - Redis code and caching functions
   ├── 📁 core              - Core configuration
   ├── 📁 db                - Database connections
   ├── 📁 discord           - Discord library for auth (optional)
   ├── 📁 lmbd              - Holds AWS lambda functions
   ├── 📁 migrations        - Database migrations
   ├── 📁 models            - Database ORM models
   ├── 📁 types             - Type definitions
   └── 📁 util              - Helper functions
```

## Makefile Commands

Make files are used to run common commands. You can find the list of commands in the `Makefile` file.
To use these commands, first copy `make-env-example.sh` to `make-env.sh` and update the values.

```bash
# macOS
cp make-env-example.sh make-env.sh

# windows (powershell)
copy make-env-example.sh make-env.sh
```

Remember to make the file executable

```bash
chmod +x make-env.sh
```

Then you can run the commands like this

```bash
./make-env.sh <command>
```

Try it with the help command, which will list all the available commands.

```bash
./make-env.sh help
```

## Contributing

1. **Fork the Repository**: Start by forking the repository to your own GitHub account.
2. **Clone the Forked Repository**: Clone the fork to your local machine.
3. **Create a New Branch**: Always create a new branch for your changes.
4. **Make Your Changes**: Implement your changes.
5. **Run Tests**: Make sure to test your changes locally.
6. **Submit a Pull Request**: Commit and push your changes, then create a pull request against the main branch.
