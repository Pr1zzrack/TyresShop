#!/bin/bash

source /app/.env

BACKUP_DIR=$BACKUP_DIR
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
MEDIA_DIR=$MEDIA_DIR

tar -czf "$BACKUP_DIR/media_backup_$DATE.tar.gz" -C $MEDIA_DIR .

find $BACKUP_DIR -type f -name "*.tar.gz" -mtime +7 -exec rm {} \;

echo "Media backup completed: $BACKUP_DIR/media_backup_$DATE.tar.gz"
