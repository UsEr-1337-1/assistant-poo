import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import PySimpleGUI as sg

# --- Initialisation NLTK ---
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# --- Bases de données ---
# --- Knowledge Base enrichie ---
knowledge_base = {
    "classe": "Une classe est un plan pour créer des objets. Elle définit des attributs (état) et des méthodes (comportements).",
    "objet": "Un objet est une instance d'une classe, avec ses propres valeurs pour les attributs.",
    "héritage": "Mécanisme par lequel une classe dérivée hérite des attributs et méthodes d'une classe de base.",
    "encapsulation": "Protection des données internes d’un objet en limitant l’accès direct et en passant par des méthodes publiques.",
    "polymorphisme": "Capacité de traiter des objets de classes différentes via une interface commune.",
    "abstraction": "Masquage des détails complexes pour n’exposer que l’essentiel d’un composant.",
    "interface": "Déclaration d’un contrat de méthodes sans en fournir l’implémentation, à réaliser dans les classes qui l’héritent.",
    "association": "Relation structurelle entre instances, sans gestion de cycle de vie.",
    "composition": "Forme forte d’association où la vie des objets composés dépend de l’objet composite.",
    "aggregation": "Association faible où les objets agrégés peuvent exister indépendamment.",
    "couplage": "Degré de dépendance entre modules ; un couplage faible est souhaitable.",
    "cohésion": "Mesure de la cohérence interne d’un module ; une forte cohésion est souhaitable.",
    "diagramme de classes uml": "Représentation graphique des classes, de leurs attributs, méthodes et relations.",
    "singleton": "Pattern qui garantit qu’une classe n’a qu’une seule instance accessible globalement.",
    "factory method": "Pattern qui définit une interface de création d’objets, laissant les sous-classes décider de la classe concrète.",
    "observer": "Pattern d’abonnement où un sujet notifie automatiquement ses observateurs en cas de changement d’état.",
    "stratégie": "Pattern qui permet de définir une famille d’algorithmes interchangeables à chaud.",
    "adaptateur": "Pattern qui rend compatibles deux interfaces incompatibles par un wrapper.",
    "decorateur": "Pattern qui ajoute dynamiquement des responsabilités à un objet sans modifier sa classe.",
    "facade": "Pattern qui fournit une interface simplifiée à un ensemble de sous-systèmes complexes.",
    "srp": "Single Responsibility Principle : une classe ne doit avoir qu’une seule raison de changer.",
    "ocp": "Open/Closed Principle : les entités doivent être ouvertes à l’extension, fermées à la modification.",
    "lsp": "Liskov Substitution Principle : une sous-classe doit pouvoir remplacer sa super-classe sans altérer le comportement.",
    "isp": "Interface Segregation Principle : privilégier plusieurs interfaces spécifiques plutôt qu’une interface générale.",
    "dip": "Dependency Inversion Principle : dépendre d’abstractions plutôt que de classes concrètes."
}

# --- Exemple Base enrichie ---
example_base = {
    "classe": """class Voiture:
    def __init__(self, marque):
        self.marque = marque
    def klaxonner(self):
        print("Bip Bip!")""",

    "objet": """voiture1 = Voiture("Toyota")
voiture1.klaxonner()  # Instanciation et appel d'une méthode""",

    "héritage": """class Animal:
    def parler(self):
        print("Je fais un bruit.")

class Chien(Animal):
    def parler(self):
        print("Wouf Wouf!")

chien = Chien()
chien.parler()  # Wouf Wouf!""",

    "encapsulation": """class CompteBancaire:
    def __init__(self, solde):
        self.__solde = solde  # attribut privé
    def deposer(self, montant):
        self.__solde += montant
    def afficher_solde(self):
        print(f"Solde: {self.__solde}")""",

    "polymorphisme": """class Oiseau:
    def voler(self):
        print("Je vole dans le ciel.")

class Avion:
    def voler(self):
        print("Je vole avec un moteur.")

for obj in (Oiseau(), Avion()):
    obj.voler()""",

    "abstraction": """from abc import ABC, abstractmethod

class Forme(ABC):
    @abstractmethod
    def aire(self):
        pass

class Cercle(Forme):
    def __init__(self, rayon):
        self.rayon = rayon
    def aire(self):
        return 3.14 * self.rayon ** 2""",

    "interface": """from abc import ABC, abstractmethod

class Volant(ABC):
    @abstractmethod
    def voler(self):
        pass

class Avion(Volant):
    def voler(self):
        print("Je vole!")""",

    "association": """class Moteur:
    pass

class Voiture:
    def __init__(self, moteur):
        self.moteur = moteur  # Voiture et Moteur associés

m = Moteur()
v = Voiture(m)""",

    "composition": """class Pneu:
    pass

class Voiture:
    def __init__(self):
        self.pneus = [Pneu() for _ in range(4)]  # relation de composition""",

    "aggregation": """class Livre:
    def __init__(self, titre):
        self.titre = titre

class Bibliotheque:
    def __init__(self, livres):
        self.livres = livres  # agrégation de livres existants

l1 = Livre("1984")
l2 = Livre("Le Meilleur des Mondes")
b = Bibliotheque([l1, l2])""",

    "couplage": """class MoteurInterface:
    def demarrer(self):
        raise NotImplementedError

class MoteurEssence(MoteurInterface):
    def demarrer(self):
        print("Démarrage essence")

class Voiture:
    def __init__(self, moteur: MoteurInterface):
        self.moteur = moteur  # couplage faible

v = Voiture(MoteurEssence())
v.moteur.demarrer()""",

    "cohésion": """class CompteBancaire:
    def __init__(self, solde=0):
        self._solde = solde
    def deposer(self, montant):
        self._solde += montant
    def retirer(self, montant):
        self._solde -= montant
    def afficher_solde(self):
        print(f"Solde: {self._solde}")  # haute cohésion""",

    "diagramme de classes uml": """\"\"\"  
+--------------+          +----------+  
|   Voiture    |<>--------|  Moteur  |  
+--------------+          +----------+  
| - marque     |          | - type   |  
+--------------+          +----------+  
| + klaxonner()|  
+--------------+  
\"\"\"""",

    "singleton": """class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

s1 = Singleton()
s2 = Singleton()
print(s1 is s2)  # True""",

    "factory method": """class Animal:
    def parler(self): pass

class Chien(Animal):
    def parler(self): print("Wouf")

class Chat(Animal):
    def parler(self): print("Miaou")

class AnimalFactory:
    @staticmethod
    def creer(type_animal):
        if type_animal == "chien": return Chien()
        if type_animal == "chat":  return Chat()
        raise ValueError("Type inconnu")

a = AnimalFactory.creer("chat")
a.parler()""",

    "observer": """class Sujet:
    def __init__(self):
        self._obs = []
    def ajouter(self, o):
        self._obs.append(o)
    def notifier(self, msg):
        for o in self._obs:
            o.mettre_a_jour(msg)

class Observateur:
    def mettre_a_jour(self, msg):
        print("Notif:", msg)

s = Sujet()
o = Observateur()
s.ajouter(o)
s.notifier("Nouvelle donnée")""",

    "stratégie": """class StrategieTri:
    def trier(self, data): pass

class TriBulle(StrategieTri):
    def trier(self, data):
        return data.sort()  # tri à bulles

class Contexte:
    def __init__(self, strategie: StrategieTri):
        self._strategie = strategie
    def executer(self, data):
        return self._strategie.trier(data)

ctx = Contexte(TriBulle())
ctx.executer([3,1,2])""",

    "adaptateur": """class ServiceExistant:
    def obtenir(self): return "données brutes"

class Adaptateur:
    def __init__(self, svc):
        self.svc = svc
    def requete(self):
        return self.svc.obtenir()

adapt = Adaptateur(ServiceExistant())
print(adapt.requete())""",

    "decorateur": """def decorateur(f):
    def inner(*args, **kw):
        print("Avant")
        res = f(*args, **kw)
        print("Après")
        return res
    return inner

@decorateur
def bonjour():
    print("Bonjour!")

bonjour()""",

    "facade": """class A:
    def opA(self): print("A")
class B:
    def opB(self): print("B")

class Facade:
    def __init__(self):
        self.a = A(); self.b = B()
    def op_simple(self):
        self.a.opA(); self.b.opB()

fac = Facade()
fac.op_simple()""",

    "srp": """# SRP : chaque classe a une seule responsabilité
class GestionnaireFichier:
    def lire(self, path): return open(path).read()

class Analyseur:
    def analyser(self, contenu): pass""",

    "ocp": """from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def calculer(self, a, b): pass

class Addition(Operation):
    def calculer(self, a, b): return a + b

class Multiplication(Operation):
    def calculer(self, a, b): return a * b

# Ajout facile d'une nouvelle opération sans modifier les existantes""",

    "lsp": """class Oiseau:
    def voler(self): print("Je vole")

class Autruche(Oiseau):
    def voler(self):
        raise NotImplementedError  # viole LSP""",

    "isp": """from abc import ABC, abstractmethod

class Imprimante(ABC):
    @abstractmethod
    def imprimer(self, doc): pass

class Scanner(ABC):
    @abstractmethod
    def scanner(self, doc): pass

class ToutEnUn(Imprimante, Scanner):
    def imprimer(self, doc): print("Impression")
    def scanner(self,  doc): print("Scan")""",

    "dip": """from abc import ABC, abstractmethod

class Moteur(ABC):
    @abstractmethod
    def demarrer(self): pass

class Electrique(Moteur):
    def demarrer(self): print("Démarrage électrique")

class Voiture:
    def __init__(self, moteur: Moteur):
        self.moteur = moteur

v = Voiture(Electrique())
v.moteur.demarrer()"""
}

# --- Fonctions de traitement ---

def get_concepts_list():
    """Retourne la liste des concepts disponibles."""
    return "Concepts disponibles :\n" + "\n".join(f"- {k}" for k in knowledge_base)

def handle_multiple_definitions(text):
    """Définitions de tous les concepts séparés par 'et'."""
    items = [c.strip() for c in re.split(r"\s+et\s+", text)]
    resp = []
    for c in items:
        if c in knowledge_base:
            resp.append(f"**{c}** : {knowledge_base[c]}")
        else:
            resp.append(f"**{c}** : Concept non reconnu.")
    return "\n\n".join(resp)

def handle_multiple_examples(text):
    """Exemples de code pour tous les concepts séparés par 'et'."""
    items = [c.strip() for c in re.split(r"\s+et\s+", text)]
    resp = []
    for c in items:
        if c in example_base:
            resp.append(f"**Exemple de {c}** :\n{example_base[c]}")
        else:
            resp.append(f"**{c}** : Pas d'exemple disponible.")
    return "\n\n".join(resp)

def compare_concepts(c1, c2):
    """Calcule intersection et différences de vocabulaire entre deux définitions."""
    stop = set(stopwords.words("french"))
    def tokenize_def(c):
        words = word_tokenize(knowledge_base[c].lower())
        return {w for w in words if w.isalpha() and w not in stop}

    if c1 not in knowledge_base or c2 not in knowledge_base:
        return "Un des concepts n'est pas reconnu."

    t1, t2 = tokenize_def(c1), tokenize_def(c2)
    comm, only1, only2 = t1 & t2, t1 - t2, t2 - t1

    return (
        f"**Points communs** : {', '.join(sorted(comm)) or 'aucun'}\n\n"
        f"**Spécificités de {c1}** : {', '.join(sorted(only1)) or 'aucune'}\n\n"
        f"**Spécificités de {c2}** : {', '.join(sorted(only2)) or 'aucune'}"
    )


# --- Construction de l'interface ---

sg.theme('DarkTeal9')  # Choix de thème

layout = [
    [ sg.Input(key='-IN-', size=(50,1)),
      sg.Button('Envoyer',    button_color=('white','green')),
      sg.Button('Exemple',    button_color=('white','blue')),
      sg.Button('Définition', button_color=('white','#1E90FF')),
      sg.Button('Lister Concepts', button_color=('white','#00CED1')),
      sg.Button('Comparer',   button_color=('white','orange')),
      sg.Button('Quitter',    button_color=('white','red'))
    ],
    [ sg.Multiline(key='-OUT-', size=(80,20), disabled=True) ]
]

window = sg.Window("Assistant POO", layout, finalize=True)


# --- Boucle d'événements ---

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Quitter'):
        break

    text = values['-IN-'].lower().strip()
    if event == 'Lister Concepts':
        result = get_concepts_list()

    elif event == 'Envoyer':
        # reprend la logique simple : définitions ou exemples selon mot-clé
        if "exemple" in text:
            # on retire le mot 'exemple' avant parsing
            result = handle_multiple_examples(text.replace("exemple", "").strip())
        else:
            # on veut juste la définition d'un seul concept
            result = handle_multiple_definitions(text)

    elif event == 'Définition':
        result = handle_multiple_definitions(text)

    elif event == 'Exemple':
        result = handle_multiple_examples(text)

    elif event == 'Comparer':
        if ' et ' in text:
            c1, c2 = [c.strip() for c in text.split(' et ', 1)]
            result = compare_concepts(c1, c2)
        else:
            result = "Veuillez indiquer deux concepts séparés par 'et'."

    else:
        result = "Action non reconnue."

    window['-OUT-'].update(result)

window.close()
