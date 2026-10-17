#!/bin/bash

# 1. Se déplacer automatiquement dans le bon dossier du projet
cd /home/joao/Desktop/xProg/Python/Apprentissage_GTK4/gtkText/ || exit 1

# 2. Récupérer le message de commit écrit après le script
MESSAGE_COMMIT="$1"

# 3. Sécurité : Si vous oubliez d'écrire un message, on en met un par défaut
if [ -z "$MESSAGE_COMMIT" ]; then
    MESSAGE_COMMIT="Mise à jour automatique du projet gtkText"
fi

# 4. Enchaînement des commandes Git
echo "Création de la sauvegarde..."
git add .

echo "Validation du commit..."
git commit -m "$MESSAGE_COMMIT"

echo "Envoi vers GitHub..."
git push

echo "Terminé ! Votre projet est à jour sur GitHub."

