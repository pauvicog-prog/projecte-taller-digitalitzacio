#!/bin/bash

echo "Comprobando contenedores del proyecto..."
docker compose ps

echo ""
echo "Contenedores activos:"
docker ps --filter "name=taller"

echo ""
echo "Comprobación finalizada."