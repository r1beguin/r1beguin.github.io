# Guide de déploiement GitHub Pages

## Étape 1 : Initialiser le repository Git

```bash
cd samaHelper
git init
git add .
git commit -m "Initial commit - SAMA Helper application"
```

## Étape 2 : Créer le repository sur GitHub

1. Allez sur [GitHub](https://github.com)
2. Cliquez sur **"New repository"**
3. Nom du repository : `samaHelper`
4. Description : `Application web pour la gestion de l'intolérance à l'histamine`
5. **Public** (pour GitHub Pages gratuit)
6. **Ne pas** cocher "Initialize with README" (on en a déjà un)
7. Cliquez sur **"Create repository"**

## Étape 3 : Lier le repository local à GitHub

```bash
git remote add origin https://github.com/VOTRE-USERNAME/samaHelper.git
git branch -M main
git push -u origin main
```

## Étape 4 : Activer GitHub Pages

1. Sur GitHub, allez dans votre repository `samaHelper`
2. Cliquez sur **"Settings"** (⚙️)
3. Dans le menu latéral, cliquez sur **"Pages"**
4. Sous **"Source"** :
   - Branch : `main`
   - Folder : `/ (root)`
5. Cliquez sur **"Save"**

## Étape 5 : Attendre le déploiement

- GitHub va automatiquement déployer votre site
- Cela prend généralement 1-2 minutes
- Vous verrez un message : **"Your site is published at..."**

## Étape 6 : Accéder à votre application

Votre application sera disponible à :
```
https://VOTRE-USERNAME.github.io/samaHelper/
```

## Mise à jour de l'application

Pour mettre à jour l'application après des modifications :

```bash
git add .
git commit -m "Description des modifications"
git push origin main
```

GitHub Pages se mettra automatiquement à jour en 1-2 minutes.

## Vérifications post-déploiement

- [ ] L'application se charge correctement
- [ ] Les 862 aliments sont affichés
- [ ] Tous les filtres fonctionnent
- [ ] La liste personnalisée fonctionne
- [ ] Les exports (TXT/CSV/JSON) marchent
- [ ] Le design est responsive (mobile/tablet/desktop)

## Problèmes courants

### La page ne se charge pas
- Vérifiez que GitHub Pages est activé dans Settings > Pages
- Attendez 5 minutes pour la première publication
- Videz le cache de votre navigateur (Ctrl+F5)

### Les CSS/JS ne se chargent pas
- Vérifiez les chemins dans `index.html` :
  - `<link rel="stylesheet" href="assets/style.css">`
  - `<script src="assets/app.js"></script>`

### Les aliments ne s'affichent pas
- Vérifiez que `foods.json` est bien à la racine
- Ouvrez la console du navigateur (F12) pour voir les erreurs

## Personnalisation du domaine (optionnel)

Pour utiliser votre propre domaine :

1. Ajoutez un fichier `CNAME` à la racine :
   ```
   votre-domaine.com
   ```

2. Configurez les DNS de votre domaine :
   ```
   Type: CNAME
   Name: www
   Value: VOTRE-USERNAME.github.io
   ```

## Support

Si vous rencontrez des problèmes :
- Consultez la [documentation GitHub Pages](https://docs.github.com/pages)
- Créez une issue sur le repository
