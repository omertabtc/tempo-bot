# 🚀 Héberger Ton Bot en 10 Minutes (GRATUIT)

## Option la Plus Simple : Railway.app

---

## 📋 **Checklist Rapide**

### **Tu as besoin de :**
- ✅ Un compte GitHub (gratuit)
- ✅ Un compte Railway (gratuit)
- ✅ Ton bot qui fonctionne en local
- ✅ 10 minutes

---

## 🎯 **3 Étapes Simples**

### **ÉTAPE 1 : Met ton code sur GitHub** (5 min)

#### **Si tu n'as PAS de compte GitHub :**
1. Va sur https://github.com/signup
2. Crée un compte (gratuit)
3. Vérifie ton email

#### **Upload ton code :**

**Option A - Script Automatique (Windows) :**
```bash
# Double-clique sur ce fichier :
deploy/push_to_github.bat

# Suis les instructions
```

**Option B - Manuel :**
```bash
# 1. Créer un repo sur GitHub
# Va sur https://github.com/new
# Nom : tempo-contract-analyzer
# Public ou Privé : Au choix
# Clique "Create repository"

# 2. Dans ton dossier bot (PowerShell ou CMD) :
cd tempo-contract-analyzer

git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TON_USERNAME/tempo-contract-analyzer.git
git push -u origin main
```

**⚠️ Important :** Le fichier `.env` (avec ton token) **NE sera PAS** envoyé sur GitHub (il est dans `.gitignore`).

---

### **ÉTAPE 2 : Créer un compte Railway** (2 min)

1. **Va sur :** https://railway.app/
2. **Clique :** "Login"
3. **Choisis :** "Login with GitHub"
4. **Autorise :** Railway à accéder à GitHub

✅ C'est tout ! Pas besoin de carte bancaire.

---

### **ÉTAPE 3 : Déployer le bot** (3 min)

1. **Sur Railway, clique :** "New Project"

2. **Sélectionne :** "Deploy from GitHub repo"

3. **Choisis :** `tempo-contract-analyzer`

4. **Ajoute tes variables d'environnement :**
   - Clique sur le projet déployé
   - Onglet **"Variables"**
   - Clique **"New Variable"**
   
   **Ajoute :**
   ```
   DISCORD_TOKEN = ton_token_complet_ici
   TEMPO_RPC_URL = https://rpc.tempo.xyz
   TEMPO_EXPLORER_API = https://contracts.tempo.xyz/api
   TEMPO_CHAIN_ID = 42431
   ```

5. **Attends le déploiement** (1-2 minutes)
   - Regarde les logs dans "Deployments"

6. **Vérifie sur Discord :**
   - Ton bot devrait être **ONLINE** ! 🟢

---

## ✅ **C'EST TOUT !**

Ton bot tourne maintenant 24/7 **GRATUITEMENT** ! 🎉

---

## 🔧 **Commandes Utiles**

### **Mettre à jour le bot :**

Après avoir modifié le code sur ton PC :

```bash
git add .
git commit -m "Update"
git push
```

Railway redéploie automatiquement ! ✨

### **Voir les logs :**
- Dashboard Railway → Ton projet → "Deployments" → "View Logs"

### **Redémarrer le bot :**
- Dashboard → "Settings" → "Restart"

---

## 💰 **C'est Vraiment Gratuit ?**

**Oui !** Railway donne :
- ✅ **$5/mois** de crédit gratuit
- ✅ **500 heures/mois** d'exécution
- ✅ Suffisant pour un bot Discord

**Si tu dépasses :**
- Upgrade vers plan Hobby : $5/mois
- Ou passe à un VPS (voir `HEBERGEMENT_24-7.md`)

---

## 🆘 **Problèmes ?**

### **Bot offline sur Discord**
→ Vérifie les logs Railway
→ Vérifie que `DISCORD_TOKEN` est correct

### **"Application error"**
→ Toutes les variables d'env sont définies ?
→ Regarde les logs pour l'erreur exacte

### **Railway dit "out of credits"**
→ Attends le début du mois prochain (crédit se reset)
→ Ou upgrade vers Hobby plan

---

## 📚 **Guides Complets**

Pour plus d'options :
- 📄 **`HEBERGEMENT_24-7.md`** - Toutes les options (VPS, Raspberry Pi, etc.)
- 📄 **`deploy/RAILWAY_DEPLOY.md`** - Guide détaillé Railway
- 📄 **`deploy/setup_vps.sh`** - Installation VPS automatique

---

## 🎯 **Résumé Ultra-Rapide**

```bash
# 1. Code sur GitHub
git init
git add .
git commit -m "Initial"
git remote add origin https://github.com/TON_USERNAME/tempo-bot.git
git push -u origin main

# 2. Railway.app
# Login with GitHub
# New Project → Deploy from GitHub
# Choisis ton repo

# 3. Variables
# DISCORD_TOKEN = ...
# TEMPO_RPC_URL = https://rpc.tempo.xyz
# etc.

# 4. Vérifie sur Discord
# Bot = ONLINE ✅
```

---

## 💡 **Prochaines Étapes**

Une fois hébergé :

1. ✅ **Partage ton bot** avec d'autres serveurs Discord
2. ✅ **Monitor l'usage** sur Railway Dashboard
3. ✅ **Améliore le bot** et push les updates automatiquement
4. ✅ Si besoin de plus : Upgrade ou passe à VPS

---

**Besoin d'aide ?** 
- Lis `HEBERGEMENT_24-7.md` pour toutes les options
- Ou demande-moi ! 🚀
