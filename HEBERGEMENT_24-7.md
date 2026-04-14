# 🚀 Hébergement 24/7 du Bot Discord

## Options d'Hébergement

Tu as **4 options** principales pour héberger ton bot :

---

## ✅ **OPTION 1 : VPS (RECOMMANDÉ)** ⭐

Un **VPS** (Virtual Private Server) = serveur Linux dans le cloud qui tourne 24/7.

### **Meilleurs Fournisseurs :**

#### **1. Contabo** (Le moins cher)
- **Prix :** ~4-5€/mois
- **RAM :** 4GB minimum
- **Site :** https://contabo.com/en/vps/
- ✅ Très bon rapport qualité/prix
- ✅ Parfait pour bot Discord

#### **2. DigitalOcean**
- **Prix :** $6/mois (Basic Droplet)
- **RAM :** 1GB
- **Site :** https://www.digitalocean.com/
- ✅ Interface facile
- ✅ Bon support
- 💵 $200 de crédit gratuit pour nouveaux users

#### **3. Vultr**
- **Prix :** $6/mois
- **RAM :** 1GB
- **Site :** https://www.vultr.com/
- ✅ Déploiement rapide
- ✅ Plusieurs datacenters

#### **4. Hetzner**
- **Prix :** 4€/mois
- **RAM :** 2GB
- **Site :** https://www.hetzner.com/
- ✅ Européen (bon pour RGPD)
- ✅ Prix compétitifs

---

### **Installation sur VPS (Ubuntu)**

Une fois ton VPS créé, connecte-toi en SSH et suis ces étapes :

#### **Étape 1 : Connexion SSH**

```bash
# Windows : Utilise PowerShell ou PuTTY
ssh root@TON_IP_VPS

# Exemple :
ssh root@123.45.67.89
```

#### **Étape 2 : Installation Python + Dépendances**

```bash
# Mise à jour du système
apt update && apt upgrade -y

# Installation Python 3.11+
apt install python3.11 python3.11-pip git -y

# Vérification
python3.11 --version
```

#### **Étape 3 : Upload ton Bot**

**Option A - Via Git (recommandé) :**
```bash
# Clone depuis GitHub (si tu as push ton code)
git clone https://github.com/TON_USERNAME/tempo-bot.git
cd tempo-bot
```

**Option B - Via SCP (depuis ton PC) :**
```bash
# Sur ton PC Windows, dans PowerShell :
scp -r tempo-contract-analyzer root@TON_IP_VPS:/root/
```

#### **Étape 4 : Configuration**

```bash
cd tempo-contract-analyzer

# Crée .env
nano .env

# Colle ta config :
DISCORD_TOKEN=ton_token_ici
TEMPO_RPC_URL=https://rpc.tempo.xyz
TEMPO_EXPLORER_API=https://contracts.tempo.xyz/api
TEMPO_CHAIN_ID=42431

# Sauvegarde : Ctrl+X, puis Y, puis Enter
```

#### **Étape 5 : Installation Dépendances**

```bash
pip3 install -r requirements.txt
```

#### **Étape 6 : Test Manuel**

```bash
# Test que ça marche
python3 bot.py

# Tu devrais voir :
# INFO - Bot is ready!

# Arrête avec Ctrl+C
```

#### **Étape 7 : Démarrage Automatique avec PM2**

PM2 = gestionnaire de processus qui garde le bot actif 24/7

```bash
# Installation PM2
apt install nodejs npm -y
npm install -g pm2

# Démarre le bot avec PM2
pm2 start bot.py --name tempo-bot --interpreter python3

# Vérifie le statut
pm2 status

# Sauvegarde pour redémarrage automatique
pm2 save
pm2 startup

# Copie et exécute la commande affichée

# Logs en temps réel
pm2 logs tempo-bot
```

#### **Étape 8 : Vérification**

```bash
# Vérifie que le bot tourne
pm2 list

# Tu devrais voir :
# ┌─────┬──────────────┬─────────┬─────────┬──────┐
# │ id  │ name         │ status  │ restart │ cpu  │
# ├─────┼──────────────┼─────────┼─────────┼──────┤
# │ 0   │ tempo-bot    │ online  │ 0       │ 5%   │
# └─────┴──────────────┴─────────┴─────────┴──────┘
```

**✅ TON BOT EST MAINTENANT 24/7 !**

---

## 🆓 **OPTION 2 : Hébergement Gratuit**

### **Railway.app** (Recommandé pour gratuit)

1. **Créer un compte :** https://railway.app/
2. **Nouveau Projet :** "New Project" → "Deploy from GitHub repo"
3. **Connecte ton GitHub**
4. **Ajoute les variables d'environnement :**
   - `DISCORD_TOKEN`
   - `TEMPO_RPC_URL`
   - etc.
5. **Deploy !**

**Limites :**
- ✅ Gratuit : $5/mois de crédit
- ⚠️ Suffisant pour un bot léger

### **Render.com**

1. **Créer un compte :** https://render.com/
2. **New Web Service**
3. **Connect GitHub**
4. **Build Command :** `pip install -r requirements.txt`
5. **Start Command :** `python bot.py`

**Limites :**
- ✅ Gratuit
- ⚠️ Le bot s'endort après 15 min d'inactivité

---

## 🏠 **OPTION 3 : Raspberry Pi chez Toi**

Si tu as un **Raspberry Pi** (ou vieux PC) :

### **Avantages :**
- ✅ Une seule fois ~50€
- ✅ Hébergement "gratuit" après
- ✅ Tu contrôles tout

### **Inconvénients :**
- ⚠️ Dépend de ta connexion internet
- ⚠️ Consommation électrique
- ⚠️ Pas de support professionnel

### **Installation :**

```bash
# Sur Raspberry Pi (Ubuntu/Raspbian)
sudo apt update
sudo apt install python3 python3-pip git -y

cd ~
git clone TON_REPO
cd tempo-contract-analyzer

pip3 install -r requirements.txt

# Avec PM2 (pareil que VPS)
npm install -g pm2
pm2 start bot.py --name tempo-bot --interpreter python3
pm2 save
pm2 startup
```

---

## 🔧 **OPTION 4 : Services Bot Hosting**

Services spécialisés pour bots Discord :

### **Discloud** (Brésilien, bon marché)
- **Site :** https://discloud.app/
- **Prix :** ~R$10/mois (2€)
- ✅ Interface simple
- ✅ Spécialisé Discord

### **BotGhost** (Interface graphique)
- **Site :** https://botghost.com/
- **Prix :** Gratuit avec limites
- ⚠️ Moins flexible

---

## 📊 **Comparaison Rapide**

| Option | Prix/mois | Complexité | Uptime | Recommandé |
|--------|-----------|------------|---------|------------|
| **VPS (Contabo)** | 4-5€ | Moyenne | 99.9% | ⭐⭐⭐⭐⭐ |
| **Railway.app** | Gratuit | Facile | 99% | ⭐⭐⭐⭐ |
| **Raspberry Pi** | ~0€* | Moyenne | Variable | ⭐⭐⭐ |
| **Render** | Gratuit | Facile | 90%** | ⭐⭐ |

*Après achat initial  
**S'endort après inactivité

---

## 🎯 **MA RECOMMANDATION**

### **Pour Débuter (Gratuit) :**
👉 **Railway.app**
- Setup en 10 minutes
- Interface graphique
- Gratuit pour commencer

### **Pour Production (Payant) :**
👉 **Contabo VPS** (4€/mois)
- Le meilleur rapport qualité/prix
- Contrôle total
- Performance excellente

---

## 🚀 **Guide Rapide VPS (Contabo)**

### **Étape par Étape :**

1. **Achète un VPS Contabo**
   - https://contabo.com/en/vps/
   - Choisis "Cloud VPS S" (4€/mois)
   - OS : Ubuntu 22.04

2. **Tu reçois un email avec :**
   - IP du serveur : `123.45.67.89`
   - User : `root`
   - Password : `xyz...`

3. **Connecte-toi :**
   ```bash
   ssh root@123.45.67.89
   # Entre le password
   ```

4. **Script d'installation automatique :**

```bash
# Copie-colle cette commande :
curl -o setup.sh https://raw.githubusercontent.com/ton-repo/setup.sh && bash setup.sh
```

Ou manuellement :

```bash
# Installation complète automatique
apt update && apt upgrade -y
apt install python3.11 python3.11-pip git nodejs npm -y
npm install -g pm2

# Clone ton bot
cd /root
git clone TON_GITHUB_REPO
cd tempo-contract-analyzer

# Config
nano .env
# Colle ton token, etc.

# Install
pip3 install -r requirements.txt

# Démarre
pm2 start bot.py --name tempo-bot --interpreter python3
pm2 save
pm2 startup
```

5. **Vérifie sur Discord**
   - Le bot devrait être ONLINE ! 🟢

---

## 📱 **Gestion à Distance**

### **Commandes Utiles PM2 :**

```bash
# Voir les logs
pm2 logs tempo-bot

# Redémarrer
pm2 restart tempo-bot

# Arrêter
pm2 stop tempo-bot

# Voir le statut
pm2 status

# Mettre à jour le bot
cd /root/tempo-contract-analyzer
git pull
pm2 restart tempo-bot
```

### **Connexion depuis Téléphone :**

**App Android/iOS :**
- **Termius** (gratuit) : https://termius.com/
- Connexion SSH depuis mobile
- Gère ton bot de n'importe où !

---

## 🔒 **Sécurité VPS**

```bash
# Crée un utilisateur non-root
adduser botuser
usermod -aG sudo botuser

# Désactive login root direct
nano /etc/ssh/sshd_config
# Change : PermitRootLogin no

# Firewall
ufw allow 22/tcp
ufw enable

# Mises à jour auto
apt install unattended-upgrades -y
```

---

## 💰 **Coûts Mensuels Réels**

- **VPS Contabo :** 4€/mois = 48€/an
- **VPS DigitalOcean :** $6/mois = 72$/an
- **Railway (gratuit) :** 0€ (avec limites)
- **Raspberry Pi :** ~3€/an (électricité)

**Mon conseil : Commence avec Railway (gratuit), puis passe à VPS si besoin de plus !**

---

## 🆘 **Problèmes Courants**

### **Bot offline après quelques heures**
→ Vérifie que PM2 est configuré : `pm2 startup`

### **RAM insuffisante**
→ Upgrade vers VPS avec plus de RAM

### **Bot ne se connecte pas**
→ Vérifie le firewall : `ufw allow out 443/tcp`

---

## ✅ **Checklist Finale**

- [ ] VPS acheté et accès SSH obtenu
- [ ] Python 3.11+ installé
- [ ] Bot uploadé sur le serveur
- [ ] `.env` configuré avec le token
- [ ] Dépendances installées
- [ ] PM2 configuré pour auto-restart
- [ ] Bot online sur Discord
- [ ] Logs vérifiés (pas d'erreurs)

---

**Quelle option tu préfères ? VPS payant ou hébergement gratuit ?** 🤔

Je peux t'aider à setup n'importe laquelle !
