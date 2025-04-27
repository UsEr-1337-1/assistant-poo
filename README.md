Assistant POO - Interface Graphique en Python 🐍

  
    Un assistant interactif pour apprendre et explorer les concepts de Programmation Orientée Objet (POO) en Python.

📋 Description

L'Assistant POO est une application en Python avec une interface graphique permettant de :

    Consulter les définitions des concepts majeurs de la POO.

    Visualiser des exemples de code pour chaque concept.

    Comparer deux concepts pour en voir les points communs et différences.

    Lister tous les concepts disponibles.

L’interface est simple et conviviale, adaptée aux étudiants, formateurs ou toute personne souhaitant renforcer sa compréhension de la POO.
🛠️ Fonctionnalités principales

    Lister Concepts : Affiche tous les concepts enregistrés.

    Définir : Retourne la définition d'un ou plusieurs concepts.

    Exemples : Génère des snippets de code Python pour illustrer les concepts.

    Comparer : Affiche les points communs et les différences entre deux concepts.

    Saisie libre : Détection automatique d'une demande de définition ou d'exemple.

🚀 Installation
Prérequis

    Python 3.7+

    Connexion Internet (pour télécharger les ressources NLTK)

Étapes

    Cloner le projet

git clone https://github.com/ton-profil/assistant-poo.git
cd assistant-poo

    Créer un environnement virtuel (optionnel mais recommandé)

python -m venv venv
# Activer l'environnement :
# Sous Windows
venv\Scripts\activate
# Sous macOS/Linux
source venv/bin/activate

    Installer les dépendances

pip install -r requirements.txt

    Télécharger les ressources NLTK nécessaires

import nltk
nltk.download('punkt')
nltk.download('stopwords')

    Lancer l'application

python app.py

🗂️ Structure du projet

assistant-poo/
│
├── app.py               # Script principal (interface graphique)
├── knowledge_base.txt   # Base de définitions POO
├── example_base.txt     # Base d'exemples de code
├── requirements.txt     # Dépendances du projet

📚 Concepts couverts

    Classe, Objet, Héritage, Encapsulation, Polymorphisme, Abstraction

    Association, Composition, Agrégation

    Patterns de conception : Singleton, Factory Method, Observer, Stratégie, Adaptateur, Décorateur, Façade

    Principes SOLID : SRP, OCP, LSP, ISP, DIP

    Diagrammes UML

