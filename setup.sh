#!/bin/bash
set -e  # Stop on first error

# Supprimer l'ancien environnement si présent
echo "Removing old virtual environment if it exists..."
rm -rf hr_env

# Créer un nouvel environnement virtuel Python 3.10
echo "Creating new virtual environment..."
python3.10 -m venv hr_env

# Activer l'environnement

source hr_env/bin/activate

# Mettre à jour pip
echo "Upgrading pip..."
pip install --upgrade pip

# Installer les dépendances
echo "Installing dependencies..."
pip install -r requirements.txt

# Télécharger les ressources NLTK nécessaires
echo "Downloading NLTK models..."
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

echo "Setup complete! Run the app with: source hr_env/bin/activate && streamlit run test_app_novoice/app.py"
