#!/bin/bash

# Configuration
# Adjust these paths relative to where the script runs or use absolute paths
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
CONTAINER_NAME="divorce-risk-analyzer-db-1" # Check 'docker ps' on server to confirm name, or use docker compose
DB_USER="admin"
DB_NAME="divorce_db"
KEEP_DAYS=7

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Filename
FILENAME="$BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz"

# Perform backup
# We use 'docker exec' to run pg_dump inside the container and pipe the output to a gzip file on the host
echo "Starting backup for $DB_NAME..."

if docker exec -t "$CONTAINER_NAME" pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$FILENAME"; then
    echo "Backup successful: $FILENAME"
else
    echo "Backup failed!"
    exit 1
fi

# Cleanup old backups (older than 7 days)
find "$BACKUP_DIR" -type f -name "db_backup_*.sql.gz" -mtime +$KEEP_DAYS -delete
echo "Cleaned up backups older than $KEEP_DAYS days."
