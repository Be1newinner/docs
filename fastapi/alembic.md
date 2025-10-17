# FastAPI + SQLAlchemy + Alembic + PostgreSQL: Migrations README

This README documents a production-ready workflow to initialize, manage, and deploy database schema changes using Alembic for a FastAPI project that uses SQLAlchemy and PostgreSQL. It covers initial setup, autogeneration, applying and reverting migrations locally and in other environments, and common commands and tips. 

### Quick start

- Initialize Alembic, wire `env.py` to your SQLAlchemy metadata, and configure the PostgreSQL URL via environment variables. 
- Generate migrations from model changes with `alembic revision --autogenerate -m "..."` and apply with `alembic upgrade head`. 
- Point `alembic` at any environment using `-x` or `ALEMBIC_CONFIG`/`sqlalchemy.url` to deploy migrations to local, staging, or production PostgreSQL. 

---

### Prerequisites

- FastAPI app with SQLAlchemy models and a `Base = declarative_base()` or SQLAlchemy 2.0 registry. 
- PostgreSQL reachable via a DSN like `postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DBNAME`. 
- Packages: `alembic`, `SQLAlchemy`, `psycopg2-binary` (or `psycopg` 3 driver) installed in your environment. 

---

### Install dependencies
```

pip install alembic

```

- Use the psycopg2-binary driver for simplicity in local/dev; use `psycopg[binary]` or system-compiled drivers in production if required. 

---

### Project structure (example)

```

.
├─ app/
│ ├─ db/
│ │ ├─ base.py # Base metadata export
│ │ ├─ session.py # Engine/session creation
│ │ └─ models/ # SQLAlchemy models
│ └─ main.py # FastAPI entrypoint
├─ alembic/ # Created by alembic init
│ ├─ env.py
│ ├─ script.py.mako
│ └─ versions/ # Migration files live here
├─ alembic.ini
└─ .env # DATABASE_URL

```

- Organize models into `app/db/models` and export metadata via `app/db/base.py` so Alembic can discover it. 

---

### Configure environment variables

```

# .env

DATABASE_URL="postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/mydb"

```

- Keep secrets out of VCS; use `.env` for local and secure secret managers in CI/CD for remote environments. 

---

### Initialize Alembic

```

alembic init alembic

```

- This creates `alembic/` and `alembic.ini`. You’ll customize `alembic/env.py` to load `DATABASE_URL` and your `Base.metadata`. 

---

### Wire env.py to your project

Edit `alembic/env.py`:

```

# alembic/env.py

from logging.config import fileConfig

from app.db.session import engine
from alembic import context

from app.core.config import settings
from app.db.base import BaseModel

# import all your models
from app.models import course as _course

from asyncio import run as run_async

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = BaseModel.metadata


def get_url() -> str:
    return settings.DATABASE_URL


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_async(run_migrations_online())

```

- Setting `sqlalchemy.url` from `DATABASE_URL` avoids hardcoding environment-specific DSNs in `alembic.ini`. 
- `compare_type` and `compare_server_default` improve autogeneration fidelity. Always review generated scripts. 

---

### Create the first migration

```

# generate from models

alembic revision --autogenerate -m "create initial schema"

# apply to database

alembic upgrade head

```

- `--autogenerate` scans `target_metadata` versus the current DB to propose operations; edit the revision file to finalize. 
- `upgrade head` applies all unapplied migrations to the latest. [web:9]

---

### Common migration commands

```

# Create new revision (empty)

alembic revision -m "add feature X tables"

# Autogenerate from model diffs

alembic revision --autogenerate -m "sync models: add users idx"

# Apply upgrades

alembic upgrade head # to latest
alembic upgrade +1 # one step up
alembic upgrade <revision_id> # to a specific revision

# Downgrade (use cautiously)

alembic downgrade -1 # one step down
alembic downgrade base # all the way down
alembic downgrade <revision_id> # to a specific revision

# Show current database revision

alembic current

# Show revision history

alembic history --verbose

# Stamp database without running migrations (sync state manually)

alembic stamp head
alembic stamp <revision_id>

# Verify if new ops exist without generating a file (useful in CI)

alembic check

# Render SQL instead of executing (dry-run)

alembic upgrade head --sql
alembic downgrade -1 --sql

```

- `alembic check` fails CI if changes would create a non-empty autogen; integrate to enforce migration hygiene. [web:9]
- `--sql` emits SQL scripts for DBAs or change management processes. [web:9]

---

### Local PostgreSQL options

- Docker example:

```

docker run --rm --name pg \
 -e POSTGRES_PASSWORD=postgres \
 -e POSTGRES_DB=mydb \
 -p 5432:5432 -d postgres:16

```

- Then set:

```

export DATABASE_URL="postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/mydb"

```

- This is convenient for local dev and aligns with Alembic `sqlalchemy.url` expectations. 

---

### Deploying migrations to other environments

- Point Alembic to the target database using environment variables or explicit config:

```

# Staging

export DATABASE_URL="postgresql+psycopg2://user:pass@staging-host:5432/appdb"
alembic upgrade head

# Production (example via inline, not recommended to expose in shell history)

DATABASE_URL="postgresql+psycopg2://user:pass@prod-host:5432/appdb" alembic upgrade head

# With custom alembic.ini

ALEMBIC_CONFIG=alembic.ini alembic -x db_url="$DATABASE_URL" upgrade head

```

- Prefer environment variables/secrets in CI pipelines to avoid hardcoding DSNs in `alembic.ini`. 
- Always backup and have rollback plans; verify `downgrade` paths for critical changes. [web:15]

---

### Running migrations on app startup (optional)

- It’s common to run migrations during deployment rather than at app boot; if you choose startup execution, consider a dedicated init container or a guarded startup hook to avoid race conditions across replicas. [web:14][web:15]

---

### Troubleshooting

- Autogenerate empty file:
  - Ensure imports load all model modules before `target_metadata` assignment. [web:12]
  - Ensure the DB has been stamped/upgraded so Alembic can diff from a known revision. [web:12]
- Types/defaults not detected:
  - Set `compare_type=True`, `compare_server_default=True` in `env.py`. 
- Using an existing database:
  - Reverse-engineer models, then `alembic revision --autogenerate` to create a baseline; carefully review and possibly `stamp` to set starting point. [web:13]

---

### CI/CD recommendations

- Add a “model drift” check:

```

alembic check

```

- Fail the pipeline if new operations are detected but no migration was committed. [web:9]
- Run `alembic upgrade head` with the environment’s `DATABASE_URL` in a deploy step or via an init job. [web:15]

---

### References

- Alembic Tutorial and Commands for full usage and advanced scenarios. [web:9]
- Autogenerate behavior and CI `alembic check`. 
- End-to-end FastAPI + SQLAlchemy + Alembic examples. 
- PostgreSQL DSN patterns and local Docker recipe. 