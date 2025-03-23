#!/bin/bash
set -e

# Variables
DB_HOST=${1}
DB_PORT=${2:-5432}
DB_NAME=${3:-fiapdb}
DB_USER=${4:-fiapuser}
DB_PASSWORD=${5}

# Check required variables
if [ -z "$DB_HOST" ] || [ -z "$DB_PASSWORD" ]; then
  echo "ERROR: DB_HOST and DB_PASSWORD are required"
  echo "Usage: $0 <db_host> [db_port] [db_name] [db_user] <db_password>"
  exit 1
fi

# Migration directory
MIGRATIONS_DIR="../migrations"

# Apply migrations
echo "Applying migrations to database $DB_NAME at $DB_HOST:$DB_PORT"

# Check if psql is installed
if ! command -v psql &> /dev/null; then
  echo "ERROR: psql is not installed"
  exit 1
fi

# Function to run SQL file
run_sql_file() {
  local file=$1
  echo "Applying migration: $file"
  PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f $file
}

# Get list of SQL files in order
SQL_FILES=$(find $MIGRATIONS_DIR -name "*.sql" | sort)

# Create migrations table if it doesn't exist
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "
  CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(255) PRIMARY KEY,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
  );
"

# Apply each migration if it hasn't been applied yet
for file in $SQL_FILES; do
  filename=$(basename "$file")
  version=${filename%%_*}
  
  # Check if migration has been applied
  applied=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "
    SELECT COUNT(*) FROM schema_migrations WHERE version = '$version';
  " | tr -d '[:space:]')
  
  if [ "$applied" -eq "0" ]; then
    # Apply migration
    run_sql_file $file
    
    # Record migration
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "
      INSERT INTO schema_migrations (version) VALUES ('$version');
    "
    echo "Migration $version applied successfully"
  else
    echo "Migration $version already applied, skipping"
  fi
done

echo "All migrations applied successfully" 