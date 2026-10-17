#!/bin/bash

# $1 correspond au texte envoyé par votre application Python
TEXTE_PARAMETRE="$1"

# Vérifier si le paramètre n'est pas vide
if [ -z "$TEXTE_PARAMETRE" ]; then
    echo "Erreur : Aucun texte fourni en paramètre."
    exit 1
fi

# Exemple d'action : transformer le texte en MAJUSCULES
TEXTE_MAJUSCULE=$(echo "$TEXTE_PARAMETRE" | tr '[:lower:]' '[:upper:]')

# On écrit le résultat dans un fichier sur le Bureau pour vérifier que ça marche
echo "Texte traité le $(date) : $TEXTE_MAJUSCULE" >> ~/Desktop/log_pytext.txt

echo "Le script Bash a traité le texte avec succès !"
exit 0

