# SAMA Helper

Application web pour la gestion de l'intolérance à l'histamine - Base de données de 862 aliments avec filtres avancés et liste personnalisée.

## 🚀 Démo en ligne

[Voir l'application](https://VOTRE-USERNAME.github.io/samaHelper)

## 📋 Fonctionnalités

### 🔍 Recherche et filtrage
- **Recherche en temps réel** : Trouvez rapidement un aliment par son nom
- **Filtres rapides** : Histamine élevée, libérateur, inhibiteur
- **Filtre par catégorie** : 25 catégories d'aliments (Fruits, Légumes, Viandes, etc.)
- **Filtre saisonnier** : 99 aliments avec données de saison (Printemps, Été, Automne, Hiver)
- **Filtre digestibilité** : 5 niveaux (0 à 3 + inconnu)

### 📝 Liste personnalisée
- **Ajout rapide** : Cliquez sur le bouton `+` pour ajouter un aliment à votre liste
- **Gestion intuitive** : Sidebar avec vue d'ensemble de votre liste
- **Persistance** : Votre liste est sauvegardée automatiquement (localStorage)
- **Export multiple** : 
  - **TXT** : Liste simple des noms
  - **CSV** : Tableau complet pour Excel
  - **JSON** : Données structurées

### 📊 Base de données complète
- **862 aliments** extraits du guide SAMA
- **Informations détaillées** :
  - Niveau d'histamine (0, 1, 2)
  - Libérateur d'histamine (L)
  - Inhibiteur de DAO (I)
  - Digestibilité (0-3)
  - Autres amines
  - Remarques spécifiques
  - Saison (fruits et légumes)

## 🏗️ Structure du projet

```
samaHelper/
├── index.html              # Page principale
├── foods.json              # Base de données (862 aliments)
├── assets/
│   ├── app.js             # Logique de l'application
│   └── style.css          # Styles CSS
├── scripts/
│   ├── extract_sama_pdf.py       # Extraction depuis PDF
│   ├── process_foods.py          # Traitement des données
│   ├── add_seasonality.py        # Ajout données saisonnières
│   └── debug_table.py            # Utilitaire de debug
├── tests/
│   ├── test_complete.py          # Tests complets
│   ├── test_advanced_filters.py  # Tests filtres avancés
│   ├── test_digestibility.py     # Tests digestibilité
│   └── test_list_functionality.py # Tests liste personnalisée
├── data/
│   ├── SAMA.pdf                  # PDF source
│   └── sama_data.json            # Données brutes
└── docs/
    └── GUIDE_FILTRES.md          # Documentation filtres
```

## 🛠️ Installation locale

### Prérequis
- Python 3.8+
- Navigateur web moderne

### Installation

1. **Cloner le repository**
```bash
git clone https://github.com/VOTRE-USERNAME/samaHelper.git
cd samaHelper
```

2. **Installer les dépendances (pour les tests)**
```bash
pip install selenium
```

3. **Lancer un serveur local**
```bash
# Avec Python
python -m http.server 8000

# Ou simplement ouvrir index.html dans votre navigateur
```

4. **Accéder à l'application**
```
http://localhost:8000
```

## 📖 Guide d'utilisation

### Rechercher un aliment
1. Tapez le nom dans la barre de recherche
2. Les résultats s'affichent en temps réel

### Filtrer les aliments
1. **Filtres rapides** : Cliquez sur "Histamine élevée", "Libérateur" ou "Inhibiteur"
2. **Catégorie** : Sélectionnez une catégorie dans le menu déroulant
3. **Saison** : Cliquez sur une saison pour voir les aliments de saison
4. **Digestibilité** : Filtrez par niveau de digestibilité (0-3)
5. **Réinitialiser** : Cliquez sur "Réinitialiser tous les filtres"

### Créer votre liste personnalisée
1. Cliquez sur le bouton **`+`** vert sur une carte d'aliment
2. Le compteur du bouton flottant 📋 s'incrémente
3. Cliquez sur le **bouton flottant 📋** pour ouvrir votre liste
4. Dans la sidebar :
   - Voir tous vos aliments
   - Retirer un aliment avec **×**
   - Exporter en TXT/CSV/JSON
   - Vider toute la liste

### Exporter votre liste
1. Ouvrez la sidebar (bouton 📋)
2. Choisissez le format :
   - **TXT** : Liste simple pour notes
   - **CSV** : Tableau pour Excel/Sheets
   - **JSON** : Données pour développeurs
3. Le fichier est téléchargé automatiquement

## 🧪 Tests

### Lancer les tests
```bash
# Tests complets
python tests/test_complete.py

# Tests filtres avancés
python tests/test_advanced_filters.py

# Tests digestibilité
python tests/test_digestibility.py

# Tests liste personnalisée
python tests/test_list_functionality.py
```

### Résultats attendus
- ✅ 862 aliments chargés
- ✅ Tous les filtres fonctionnels
- ✅ Liste personnalisée opérationnelle
- ✅ Export dans tous les formats

## 🔧 Développement

### Extraire les données du PDF

```bash
# 1. Extraction brute depuis le PDF
python scripts/extract_sama_pdf.py

# 2. Traitement et nettoyage
python scripts/process_foods.py

# 3. Ajout des données de saison
python scripts/add_seasonality.py
```

### Technologies utilisées
- **HTML5** : Structure sémantique
- **CSS3** : Design moderne et responsive
- **JavaScript vanilla** : Logique côté client
- **localStorage** : Persistance des données
- **Python** : Scripts d'extraction et tests (Selenium)

## 📱 Responsive Design

L'application est entièrement responsive :
- 📱 Mobile : Interface adaptée, sidebar plein écran
- 💻 Tablet : Grid optimisée
- 🖥️ Desktop : Vue complète avec sidebar latérale

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- **SAMA** pour le guide original des aliments
- Tous les contributeurs et testeurs

## 📞 Contact

Pour toute question ou suggestion :
- Créez une [issue](https://github.com/VOTRE-USERNAME/samaHelper/issues)
- Email : votre.email@example.com

---

**Note** : Cette application est un outil d'information. Consultez toujours un professionnel de santé pour des conseils médicaux personnalisés.
