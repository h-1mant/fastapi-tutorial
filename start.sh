#!/bin/bash
set -e

# If schema already exists but alembic_version doesn't, stamp head to sync
# tracking without re-running migrations. On a fresh DB, skip stamp so
# upgrade head creates everything normally.
python - <<'EOF'
import os, sqlalchemy as sa
engine = sa.create_engine(os.environ["CONN_STRING"])
insp = sa.inspect(engine)
if not insp.has_table("alembic_version") and insp.has_table("posts"):
    print("Schema exists without Alembic tracking — stamping head")
    import subprocess
    subprocess.run(["alembic", "stamp", "head"], check=True)
EOF

alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
