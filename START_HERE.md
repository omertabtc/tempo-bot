# 🚀 START HERE - Quick Setup for Your Bot

Your Discord bot is already created! Here's what you need to do:

---

## ✅ You Have

- **Application ID:** `2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e`
- **Public Key:** `2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e`
- **Bot folder:** `tempo-contract-analyzer/` (all code is ready!)

---

## 🔑 What You Need: Bot Token

### Get Your Token (2 minutes):

1. **Go to your bot's page:**
   
   👉 [Click here](https://discord.com/developers/applications/2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e/bot)

2. **Click "Bot" in the left sidebar**

3. **Scroll to "TOKEN" section**

4. **Click "Reset Token" (or "Copy" if visible)**
   - Confirm with 2FA if asked
   
5. **Copy the token** - it looks like this:
   ```
   YOUR_BOT_TOKEN.XXXXXX.YYYYYYYYYYYYYYYYYYYYYYYY
   ```

6. **⚠️ Keep it secret!** Never share this!

---

## ⚡ Quick Install (Choose One)

### Option 1: Automated (Recommended)

**Windows:** Double-click `run.bat`

**Mac/Linux:**
```bash
chmod +x run.sh
./run.sh
```

The script will:
1. Check if `.env` exists (it does - I created it!)
2. Create virtual environment
3. Install all dependencies
4. Start the bot

**BUT FIRST:** You need to edit `.env` and add your token!

---

### Option 2: Manual

```bash
# 1. Go to bot folder
cd tempo-contract-analyzer

# 2. Install dependencies
pip install discord.py web3 aiohttp python-dotenv requests eth-abi eth-utils

# 3. Edit .env file
# Windows:
notepad .env

# Mac/Linux:
nano .env

# 4. Replace 'your_bot_token_here' with your actual token:
DISCORD_TOKEN=YOUR_ACTUAL_BOT_TOKEN_HERE

# Save and close

# 5. Run the bot
python bot.py
```

---

## 🎯 Enable Required Settings

Before running, make sure these are enabled in Discord Developer Portal:

### 1. Message Content Intent

1. Go to [Bot settings](https://discord.com/developers/applications/2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e/bot)
2. Scroll to **"Privileged Gateway Intents"**
3. Toggle ON: ✅ **Message Content Intent**
4. Click **Save Changes**

### 2. Invite Bot to Your Server

1. Go to [OAuth2 → URL Generator](https://discord.com/developers/applications/2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e/oauth2/url-generator)
2. Select:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Use Slash Commands
4. Copy the URL at the bottom
5. Open it in browser
6. Select your server
7. Click Authorize

---

## ✅ Check It's Working

### In Terminal:
```
INFO - ✓ Logged in as YourBotName
INFO - ✓ Connected to 1 guild(s)
INFO - ✓ Bot is ready!
```

### In Discord:
- Bot shows **Online** (green dot)
- Type `/` and see `/analyze-contract`

---

## 🧪 Test It!

Run this command in Discord:

```
/analyze-contract 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
```

You should see a beautiful colored embed report!

*(That's USDC on Ethereum - for real testing use a Tempo blockchain contract address)*

---

## 🎨 What You'll See

The bot will analyze the contract and show:

- **🟢 Green embed** = Safe contract
- **🟡 Yellow embed** = Warning, moderate risks
- **🔴 Red embed** = HIGH RISK, don't interact!

Each report includes:
- Contract type (ERC-20, NFT, etc.)
- Verification status
- Risk score
- Detailed findings in plain English
- Specific recommendations

---

## 🆘 Troubleshooting

### "DISCORD_TOKEN must be set"
→ Edit `.env` and add your token (no spaces around `=`)

### Bot is offline
→ Make sure bot is running (`python bot.py`)
→ Check token is correct

### Slash command doesn't appear
→ Wait 1 hour (global sync takes time)
→ OR add this to `.env` for instant sync:
```env
DISCORD_GUILD_ID=your_server_id_here
```

### "Interaction failed"
→ Re-invite bot with correct permissions
→ Make sure "applications.commands" scope is enabled

---

## 📚 Full Documentation

Once it's working, explore:

- **DISCORD_SETUP.md** - Detailed Discord setup
- **QUICKSTART.md** - Complete beginner guide
- **EXAMPLES.md** - See example outputs and customization
- **OUTPUT_DEMO.md** - Visual examples of all embed colors
- **README.md** - Full technical documentation

---

## 🎯 Quick Checklist

Before you start:

- [ ] Got bot token from Developer Portal
- [ ] Edited `.env` and added token
- [ ] Enabled "Message Content Intent"
- [ ] Invited bot to server with correct permissions
- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Running bot (`python bot.py`)
- [ ] Bot shows online in Discord
- [ ] Tested `/analyze-contract` command

---

## 🚀 You're Ready!

Your bot is **100% complete** and ready to analyze Tempo blockchain contracts!

**Next:** 
1. Get your bot token (link above)
2. Edit `.env` file
3. Run `python bot.py`
4. Test in Discord!

**Need help?** Check `DISCORD_SETUP.md` for detailed troubleshooting!

---

**Direct Links:**
- [Your Application Dashboard](https://discord.com/developers/applications/2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e)
- [Bot Settings](https://discord.com/developers/applications/2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e/bot)
- [Invite Link Generator](https://discord.com/developers/applications/2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e/oauth2/url-generator)

Good luck! 🎉
