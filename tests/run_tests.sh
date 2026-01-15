#!/bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
PYTHON_TEST_FILE="$SCRIPT_DIR/test_global.py"

if [ -f "$PYTHON_TEST_FILE" ]; then
    echo " Lancement de l'audit Python..."
    python3 "$PYTHON_TEST_FILE"
else
    echo " Erreur : Le fichier $PYTHON_TEST_FILE est introuvable."
    exit 1
fi
