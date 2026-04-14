# 🚂 Déploiement sur Railway.app (GRATUIT)

## Setup Ultra-Rapide (10 minutes)

### **Étape 1 : Prépare ton Code**

1. **Crée un compte GitHub** (si pas déjà fait)
   - https://github.com/signup

2. **Crée un nouveau repository**
   - Nom : `tempo-contract-analyzer`
   - Public ou Privé : Au choix
   - **N'ajoute RIEN** (pas de README, .gitignore, etc.)

3. **Upload ton code sur GitHub**

Depuis ton dossier `tempo-contract-analyzer` :

```bash
# Initialise Git
git init

# Ajoute tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit - Tempo Contract Analyzer Bot"

# Connecte à GitHub (remplace TON_USERNAME)
git remote add origin https://github.com/TON_USERNAME/tempo-contract-analyzer.git

# Push
git branch -M main
git push -u origin main
```

**⚠️ IMPORTANT:** Ne push PAS ton fichier `.env` ! Il est déjà dans `.gitignore`.

---

### **Étape 2 : Déploie sur Railway**

1. **Créer un compte Railway**
   - Va sur : https://railway.app/
   - Clique **"Login"**
   - **"Login with GitHub"**
   - Autorise Railway à accéder à GitHub

2. **Nouveau Projet**
   - Clique **"New Project"**
   - Sélectionne **"Deploy from GitHub repo"**
   - Choisis `tempo-contract-analyzer`

3. **Ajoute les Variables d'Environnement**
   - Dans Railway, clique sur ton projet
   - Onglet **"Variables"**
   - Clique **"New Variable"**
   
   Ajoute ces variables une par une :

   ```
   DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
   TEMPO_RPC_URL=https://rpc.tempo.xyz
   TEMPO_EXPLORER_API=https://contracts.tempo.xyz/api
   TEMPO_CHAIN_ID=42431
   ```

4. **Deploy!**
   - Railway va automatiquement :
     - ✓ Détecter Python
     - ✓ Installer les dépendances
     - ✓ Démarrer le bot
   
   - Regarde les logs dans l'onglet **"Deployments"**

5. **Vérifie sur Discord**
   - Ton bot devrait être **ONLINE** ! 🟢

---

### **Étape 3 : Gestion**

#### **Voir les Logs**
- Dashboard Railway → Ton projet → **"Deployments"** → **"View Logs"**

#### **Redémarrer le Bot**
- Dashboard → **"Settings"** → **"Restart"**

#### **Mettre à Jour le Bot**

Depuis ton PC :
```bash
# Fais tes modifications
# Puis :
git add .
git commit -m "Update bot"
git push

# Railway redéploie automatiquement !
```

---

## 💰 **Limites Gratuites Railway**

- ✅ **$5 de crédit/mois** gratuit
- ✅ **500 heures/mois** d'exécution
- ✅ **100 GB de bande passante**

**C'est largement suffisant pour un bot Discord !**

Si tu dépasses :
- Upgrade vers **Hobby Plan** : $5/mois pour usage illimité

---

## 🔧 **Troubleshooting**

### **Bot ne démarre pas**
→ Vérifie les logs dans Railway
→ Vérifie que `DISCORD_TOKEN` est correct

### **"Application error"**
→ Vérifie que toutes les variables d'env sont définies
→ Vérifie les logs pour l'erreur exacte

### **Bot offline après quelques heures**
→ Vérifie ton crédit Railway (Dashboard → **"Usage"**)
→ Si crédit épuisé, upgrade ou attends le mois prochain

---

## 📊 **Alternative : Render.com**

Si Railway ne marche pas, essaye **Render.com** (aussi gratuit) :

1. **Compte Render :** https://render.com/
2. **New → Web Service**
3. **Connect GitHub repo**
4. **Settings :**
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `python bot.py`
5. **Environment Variables :**
   - Ajoute `DISCORD_TOKEN`, etc.
6. **Create Web Service**

**Note :** Sur Render gratuit, le bot s'endort après 15 min d'inactivité.

---

## ✅ **Checklist**

- [ ] Code sur GitHub (sans .env)
- [ ] Compte Railway créé
- [ ] Projet déployé depuis GitHub
- [ ] Variables d'environnement ajoutées
- [ ] Bot ONLINE sur Discord
- [ ] Logs vérifiés (pas d'erreurs)

---

## 🎯 **Prochaines Étapes**

Une fois que ça marche sur Railway :

1. **Monitor l'usage**
   - Dashboard Railway → **"Usage"**
   - Si tu dépasses $5/mois, considère un VPS

2. **Automatise les updates**
   - Chaque `git push` = redéploiement auto
   - Pratique pour les améliorations !

3. **Backup ton code**
   - GitHub = backup automatique
   - Clone sur plusieurs machines si besoin

---

**Questions ?** Vérifie `HEBERGEMENT_24-7.md` pour d'autres options !
