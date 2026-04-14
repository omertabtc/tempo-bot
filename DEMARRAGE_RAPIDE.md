# 🚀 DÉMARRAGE RAPIDE - Bot Tempo Analyzer

Ton token est configuré ! Voici les dernières étapes :

---

## ⚡ ÉTAPE 1 : Installer les dépendances (2 minutes)

Ouvre un terminal/PowerShell dans le dossier `tempo-contract-analyzer` et tape :

```bash
pip install -r requirements.txt
```

Cela va installer :
- ✅ discord.py (framework Discord)
- ✅ web3 (interaction blockchain)
- ✅ aiohttp (HTTP async)
- ✅ python-dotenv (variables d'environnement)
- ✅ eth-abi, eth-utils (outils Ethereum)
- ✅ requests

**Attends que ça se termine** (peut prendre 1-2 minutes)

---

## ▶️ ÉTAPE 2 : Démarrer le bot

Une fois les dépendances installées, lance :

```bash
python bot.py
```

**Tu devrais voir :**
```
INFO - Loading cogs...
INFO - ✓ Loaded contract_analysis cog
INFO - ✓ Synced commands globally
INFO - ✓ Logged in as TonBotName (ID: 1493383531638816830)
INFO - ✓ Connected to X guild(s)
INFO - ✓ Bot is ready!
```

---

## 🎯 ÉTAPE 3 : Inviter le bot sur ton serveur Discord

Si tu ne l'as pas encore fait :

1. **Ouvre ce lien :**
   👉 https://discord.com/developers/applications/2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e/oauth2/url-generator

2. **Sélectionne les SCOPES :**
   - [✓] bot
   - [✓] applications.commands

3. **Sélectionne les PERMISSIONS :**
   - [✓] Send Messages
   - [✓] Embed Links
   - [✓] Use Slash Commands

4. **Copie l'URL générée** en bas de la page

5. **Ouvre l'URL** dans ton navigateur

6. **Sélectionne ton serveur** Discord

7. **Clique "Autoriser"**

Le bot devrait apparaître sur ton serveur (hors ligne jusqu'à ce que tu lances `python bot.py`)

---

## 🧪 ÉTAPE 4 : Tester le bot

Une fois le bot en ligne (point vert), dans Discord tape :

```
/analyze-contract 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
```

Tu devrais voir :
1. Un message de progression
2. Puis un **embed coloré** avec l'analyse :
   - 🟢 **Vert** = Contrat sûr
   - 🟡 **Jaune** = Attention, risques modérés
   - 🔴 **Rouge** = RISQUE ÉLEVÉ !

---

## ⚠️ IMPORTANT - SÉCURITÉ

### 🔒 APRÈS LE TEST, RÉGÉNÈRE TON TOKEN !

Tu as partagé ton token publiquement. **Tu DOIS le régénérer** :

1. Va sur : https://discord.com/developers/applications/2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e/bot
2. Clique "Regenerate" sous TOKEN
3. Copie le nouveau token
4. Remplace dans `.env` :
   ```bash
   notepad .env
   # Change DISCORD_TOKEN=... avec le nouveau
   # Sauvegarde
   ```
5. Redémarre le bot : `python bot.py`

**Lis le fichier IMPORTANT_SECURITY.md pour plus de détails !**

---

## 📋 Résumé des commandes

```bash
# 1. Installer les dépendances (une seule fois)
pip install -r requirements.txt

# 2. Lancer le bot
python bot.py

# 3. Tester sur Discord
/analyze-contract 0xadresse_du_contrat
```

---

## 🆘 Problèmes courants

### "discord module not found"
→ Lance `pip install -r requirements.txt`

### "DISCORD_TOKEN must be set"
→ Le token est déjà configuré dans `.env` normalement

### Le bot reste hors ligne
→ Assure-toi que `python bot.py` tourne
→ Vérifie qu'il n'y a pas d'erreurs dans le terminal

### La commande `/analyze-contract` n'apparaît pas
→ Attends 1 heure (synchronisation globale)
→ OU ajoute dans `.env` :
```env
DISCORD_GUILD_ID=ton_server_id
```
(Clique-droit sur ton serveur → Copier l'identifiant du serveur)

---

## ✅ Checklist finale

- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Bot invité sur le serveur Discord
- [ ] Bot démarré (`python bot.py`)
- [ ] Bot en ligne (point vert sur Discord)
- [ ] Commande `/analyze-contract` testée
- [ ] **TOKEN RÉGÉNÉRÉ** (sécurité !)

---

## 🎉 C'est tout !

Ton bot analyse maintenant les smart contracts sur Tempo blockchain !

**Prochaines étapes :**
- Teste avec de vrais contrats Tempo
- Essaye d'analyser 4 contrats rapidement pour tester le rate limiting
- Regarde les différentes couleurs d'embed (vert/jaune/rouge)

**Documentation complète en anglais :**
- START_HERE.md
- EXAMPLES.md
- OUTPUT_DEMO.md

Besoin d'aide ? Dis-moi ! 🚀
