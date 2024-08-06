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

-   ⚡ Async and type safety by default
-   🛠️ CI/CD and tooling setup
-   🚀 High performance libraries integrated ([orjson](https://github.com/ijl/orjson), [uvloop](https://github.com/MagicStack/uvloop), [pydantic2](https://github.com/pydantic/pydantic))
-   📝 [Loguru](https://github.com/Delgan/loguru) + [picologging](https://github.com/microsoft/picologging) for simplified and performant logging
-   🐳 Dockerized and includes AWS deployment flow
-   🗃️ Several database implementations with sample ORM models (MySQL, Postgres, Timescale) & migrations
-   🔐 Optional JWT authentication and authorization
-   🌐 AWS Lambda functions support
-   🧩 Modularized features
-   📊 Prometheus metrics
-   📜 Makefile commands
-   🗺️ Route profiling

## Table of Contents

-   [Requirements](#requirements)
-   [Installation](#installation)
-   [Environment Specific Configuration](#environment-specific-configuration)
-   [Upgrading Dependencies](#upgrading-dependencies)
-   [Databases](#databases)
    -   [Shell](#shell)
    -   [Migrations](#migrations)
    -   [Downgrade Migration](#downgrade-migration)
-   [JWT Auth](#jwt-auth)
    -   [JWT Overview](#jwt-overview)
    -   [Modifying JWT Payload Fields](#modifying-jwt-payload-fields)
-   [Project Structure](#project-structure)
-   [Makefile Commands](#makefile-commands)
-   [Contributing](#contributing)

## Requirements

-   [Python 3.11+](https://www.python.org/downloads/)
-   [Docker](https://www.docker.com/get-started/)

## Installation

1. Fork this repo ([How to create a private fork](https://gist.github.com/0xjac/85097472043b697ab57ba1b1c7530274))

2. Install UV Package Manager:
   Follow the installation instructions at https://github.com/astral-sh/uv

3. Set up the virtual environment and install dependencies:

    ```bash
    uv venv

    # On macOS and Linux
    source .venv/bin/activate

    # On Windows
    .venv\Scripts\activate

    # Install main dependencies
    uv pip install -r requirements.txt

    # Install development dependencies (optional)
    uv pip install -r dev-requirements.txt
    ```

4. Install [Docker](https://www.docker.com/get-started/)

5. Start your Docker services:

    ```bash
    docker compose up
    ```

6. Clone `.env.example` to `.env` and update the values:

    ```bash
    # macOS and Linux
    cp .env.example .env

    # Windows (PowerShell)
    Copy-Item .env.example .env
    ```

    You can use this command to generate secret keys:

    ```bash
    # macOS and Linux
    openssl rand -hex 128

    # Windows (PowerShell)
    $bytes = New-Object byte[] 128; (New-Object Security.Cryptography.RNGCryptoServiceProvider).GetBytes($bytes); [System.BitConverter]::ToString($bytes) -Replace '-'
    ```

7. Run the server:

    ```bash
    uvicorn main:server --reload
    ```

Note: If you need to update dependencies, you can modify the `requirements.txt` or `dev-requirements.txt` files directly and then run `uv pip install -r requirements.txt` or `uv pip install -r dev-requirements.txt` respectively.

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

-   Changes of table name
-   Changes of column name
-   Anonymously named constraints
-   Special SQLAlchemy types such as Enum when generated on a backend which doesn’t support ENUM directly

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

## JWT Implementation

In this FastAPI template, JSON Web Tokens (JWT) can be optionally utilized for authentication. This documentation section elucidates the JWT implementation and related functionalities.

### JWT Overview

The JWT implementation can be found in the module: app/auth/jwt.py. The primary functions include:

-   Creating access and refresh JWT tokens.
-   Verifying and decoding a given JWT token.
-   Handling JWT-based authentication for FastAPI routes.

#### User Management

If a user associated with a JWT token is not found in the database, a new user will be created. This is managed by the get_or_create_user function. When a token is decoded and the corresponding user ID (sub field in the token) is not found, the system will attempt to create a new user with that ID.

#### Nonce Usage

A nonce is an arbitrary number that can be used just once. It's an optional field in the JWT token to ensure additional security. If a nonce is used:

-   It is stored in Redis for the duration of the refresh token's validity.
-   It must match between access and refresh tokens to ensure their pairing.
-   Its presence in Redis is verified before the token is considered valid.

Enabling nonce usage provides an additional layer of security against token reuse, but requires Redis to function.

### Modifying JWT Payload Fields

The JWT token payload structure is defined in `app/types/jwt.py`` under the JWTPayload class. If you wish to add more fields to the JWT token payload:

1. Update the TokenData and JWTPayload class in `app/types/jwt.py`` by adding the desired fields.

    ```python
    class JWTPayload(BaseModel):
        # ... existing fields ...
        new_field: Type

    class TokenData(BaseModel):
        # ... existing fields ...
        new_field: Type
    ```

    TokenData is separated from JWTPayload to make it clear what is automatically filled in and what is manually added. Both classes must be updated to include the new fields.

2. Wherever the token is created, update the payload to include the new fields.

    ```python
    from app.auth.jwt import create_jwt
    from app.types.jwt import TokenData

    payload = TokenData(
        sub='user_id_1',
        field1='value1',
        # ... all fields ...
    )
    access_token, refresh_token = create_jwt(payload)
    ```

Remember, the JWT token has a size limit. The more data you include, the bigger your token becomes, so ensure that you only include essential data in the token payload.

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
