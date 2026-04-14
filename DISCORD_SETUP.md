# Discord Bot Setup Guide

## Step 1: Get Your Bot Token

You have:
- ✅ Application ID: `2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e`
- ✅ Public Key: `2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e`

**Now you need the Bot Token:**

1. Go to [Discord Developer Portal](https://discord.com/developers/applications/2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e)
   
2. Click **"Bot"** in the left sidebar

3. Scroll down to **"TOKEN"** section

4. Click **"Reset Token"** (or "Copy" if you see it)
   - ⚠️ You'll need to confirm with 2FA if enabled
   
5. **Copy the token** - it looks like:
   ```
   YOUR_BOT_TOKEN_HERE.XXXXXX.YYYYYYYYYYYYYYYYYYYYYYYY
   ```
   - It has 3 parts separated by dots
   - Much longer than your Application ID

6. **⚠️ KEEP IT SECRET!** Never share this token publicly

---

## Step 2: Enable Required Bot Permissions

While you're in the Developer Portal:

### Privileged Gateway Intents

1. Go to **Bot** section
2. Scroll to **"Privileged Gateway Intents"**
3. Enable:
   - ✅ **Message Content Intent** (required!)
   
### Bot Permissions

1. Go to **OAuth2** → **URL Generator**
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select bot permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Use Slash Commands
   - ✅ Read Message History (optional but helpful)

4. Copy the generated URL at the bottom

---

## Step 3: Invite Bot to Your Server

1. Open the URL you copied in Step 2
2. Select your Discord server
3. Click **Authorize**
4. Complete the captcha

Your bot should now appear in your server (offline until you run it).

---

## Step 4: Configure the Bot

Now that you have your bot token, let's set it up:

1. **Navigate to the bot directory:**
   ```bash
   cd tempo-contract-analyzer
   ```

2. **Create your `.env` file:**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` and add your bot token:**
   ```bash
   # Windows
   notepad .env
   
   # Mac/Linux
   nano .env
   ```
   
   Replace `your_bot_token_here` with your actual token:
   ```env
   DISCORD_TOKEN=YOUR_ACTUAL_BOT_TOKEN_HERE
   TEMPO_RPC_URL=https://rpc.tempo.xyz
   TEMPO_EXPLORER_API=https://contracts.tempo.xyz/api
   TEMPO_CHAIN_ID=42431
   ```

4. **Save and close**

---

## Step 5: Run the Bot

### Option A: Quick Start Script

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

### Option B: Manual Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
```

---

## Step 6: Verify It's Working

You should see in the terminal:

```
INFO - Loading cogs...
INFO - ✓ Loaded contract_analysis cog
INFO - ✓ Synced commands globally
INFO - ✓ Logged in as YourBotName (ID: 2db0e8be9a281345bb841284c5c12ee6)
INFO - ✓ Connected to 1 guild(s)
INFO - ✓ Bot is ready!
```

In Discord:
- Your bot should show as **Online** (green dot)
- Type `/` and you should see `/analyze-contract` appear

---

## Step 7: Test the Bot

Run your first analysis:

```
/analyze-contract 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
```

(This is USDC on Ethereum - use any Tempo contract address for real testing)

---

## Troubleshooting

### Bot shows offline
- ✅ Check your token is correct in `.env`
- ✅ Make sure you're running `python bot.py`
- ✅ Check for errors in the terminal

### "Interaction failed" error
- ✅ Wait 1 hour for global command sync (or add `DISCORD_GUILD_ID` to `.env` for instant sync)
- ✅ Make sure bot has "Use Slash Commands" permission

### Commands don't appear
- ✅ Re-invite bot with correct permissions
- ✅ Check you enabled "applications.commands" scope

### "DISCORD_TOKEN must be set" error
- ✅ Make sure `.env` file exists
- ✅ Make sure token is on the line `DISCORD_TOKEN=...` with no spaces around `=`

---

## Quick Reference: Your Bot Info

```yaml
Application ID: 2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e
Public Key: 2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e
Bot Token: [YOU NEED TO GET THIS - see Step 1]
```

Direct link to your application:
https://discord.com/developers/applications/2db0e8be9a281345bb841284c5c12ee6aa513d9bd9f5735a8bdb0558c19f0a0e

---

## Security Reminders

🔒 **NEVER share your bot token publicly!**
- It's like a password - anyone with it can control your bot
- If leaked, reset it immediately in Developer Portal
- Never commit `.env` to GitHub (it's already in `.gitignore`)

✅ **Safe to share:**
- Application ID (you already did - that's fine!)
- Public Key
- Bot's username

❌ **NEVER share:**
- Bot Token
- `.env` file contents

---

## Next Steps

Once your bot is running:

1. ✅ Test with a known safe contract
2. ✅ Test with a known risky contract (check examples in EXAMPLES.md)
3. ✅ Test rate limiting (run 4 analyses quickly)
4. ✅ Check the embed colors are correct
5. ✅ Share in your Discord server!

---

## Need Help?

- Bot won't start? Check the terminal for error messages
- Commands not working? Check QUICKSTART.md troubleshooting section
- Want to customize? See EXAMPLES.md for customization guide

**You're almost there! Just need that bot token and you're ready to go! 🚀**
