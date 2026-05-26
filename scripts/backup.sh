#!/bin/bash

FECHA=$(date +%Y-%m-%d_%H-%M-%S)

mkdir -p backups

docker exec taller_db mariadb-dump -u root -proot taller > backups/backup_taller_$FECHA.sql

echo "Backup creado correctamente en la carpeta backups"