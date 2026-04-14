# ⚠️ IMPORTANT - SÉCURITÉ DU TOKEN

## 🚨 TON TOKEN A ÉTÉ PARTAGÉ PUBLIQUEMENT !

Tu as partagé ton token Discord dans un message Telegram. N'importe qui avec ce token peut contrôler ton bot !

---

## 🔒 RÉGÉNÈRE TON TOKEN IMMÉDIATEMENT APRÈS LE TEST

### Étapes pour régénérer :

1. **Va sur la page de ton bot :**
   👉 https://discord.com/developers/applications/2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e/bot

2. **Clique sur "Regenerate" sous TOKEN**
   - Confirme l'action

3. **Copie le NOUVEAU token**

4. **Remplace dans `.env` :**
   ```bash
   notepad .env
   # Remplace l'ancien token par le nouveau
   # Sauvegarde et ferme
   ```

5. **Redémarre le bot :**
   ```bash
   python bot.py
   ```

---

## ✅ RÈGLES DE SÉCURITÉ

### ❌ NE JAMAIS :
- Partager ton token dans des messages
- Poster ton token sur Discord, Telegram, etc.
- Commiter le fichier `.env` sur GitHub
- Donner ton token à quelqu'un d'autre

### ✅ TOUJOURS :
- Garder le token secret
- Le stocker uniquement dans `.env`
- Régénérer le token s'il a été exposé
- Utiliser `.gitignore` pour exclure `.env`

---

## 🔄 APRÈS LE TEST DU BOT

1. ✅ Teste que le bot fonctionne
2. ✅ Vérifie que `/analyze-contract` marche
3. 🔒 **RÉGÉNÈRE LE TOKEN** (étapes ci-dessus)
4. ✅ Redémarre le bot avec le nouveau token

---

**Pourquoi c'est important ?**

Avec ton token, quelqu'un peut :
- Faire parler ton bot
- Spammer des serveurs
- Supprimer des messages
- Bannir des utilisateurs
- Utiliser ton bot pour des actions malveillantes

**Action immédiate après test : RÉGÉNÉRER LE TOKEN !**
