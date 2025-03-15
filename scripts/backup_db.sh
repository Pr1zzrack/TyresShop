#!/bin/bash

source /app/.env

BACKUP_DIR=$BACKUP_DIR
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
DB_NAME=$POSTGRES_DB
DB_USER=$POSTGRES_USER
DB_PASSWORD=$POSTGRES_PASSWORD
DB_HOST=$POSTGRES_HOST

export PGPASSWORD=$DB_PASSWORD
pg_dump -h $DB_HOST -U $DB_USER -F c -b -v -f "$BACKUP_DIR/db_backup_$DATE.dump" $DB_NAME

find $BACKUP_DIR -type f -name "*.dump" -mtime +7 -exec rm {} \;

echo "Backup completed: $BACKUP_DIR/db_backup_$DATE.dump"
