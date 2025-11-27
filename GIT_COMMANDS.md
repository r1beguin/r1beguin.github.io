# Commandes Git pour déploiement

## Initialisation du repository

```bash
# 1. Initialiser Git dans le dossier
cd C:\Users\gibso\Documents\dev\samaHelper
git init

# 2. Ajouter tous les fichiers
git add .

# 3. Premier commit
git commit -m "Initial commit: SAMA Helper - Application web pour gestion intolerance histamine

- 862 aliments extraits du guide SAMA
- Filtres avancés (catégorie, saison, digestibilité)
- Liste personnalisée avec export TXT/CSV/JSON
- Interface responsive et moderne
- Tests Selenium complets"

# 4. Créer le repository sur GitHub
# Aller sur https://github.com/new
# Nom: samaHelper
# Description: Application web pour la gestion de l'intolérance à l'histamine
# Public
# Ne pas initialiser avec README

# 5. Lier au repository distant (remplacer VOTRE-USERNAME)
git remote add origin https://github.com/VOTRE-USERNAME/samaHelper.git
git branch -M main
git push -u origin main
```

## Activer GitHub Pages

1. Sur GitHub, aller dans votre repository `samaHelper`
2. Settings > Pages
3. Source: Branch `main`, folder `/ (root)`
4. Save
5. Attendre 1-2 minutes

Votre site sera disponible à: `https://VOTRE-USERNAME.github.io/samaHelper/`

## Mises à jour futures

```bash
# Après chaque modification
git add .
git commit -m "Description de vos modifications"
git push origin main
```

## Vérification

Vérifiez que tout fonctionne :
- ✅ Page se charge
- ✅ 862 aliments affichés
- ✅ Tous les filtres fonctionnent
- ✅ Liste personnalisée fonctionne
- ✅ Exports TXT/CSV/JSON fonctionnent
- ✅ Responsive sur mobile/tablet/desktop
