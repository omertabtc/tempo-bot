# Quick Start Guide

Get your Tempo Contract Analyzer bot running in 5 minutes!

## Step 1: Get Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Give it a name (e.g., "Tempo Analyzer")
4. Go to "Bot" section → Click "Add Bot"
5. Under "TOKEN", click "Reset Token" and copy it (save it securely!)
6. Enable these Privileged Gateway Intents:
   - ✅ Message Content Intent
7. Go to "OAuth2" → "URL Generator":
   - Scopes: `bot`, `applications.commands`
   - Bot Permissions: `Send Messages`, `Embed Links`, `Use Slash Commands`
8. Copy the generated URL and open it to invite the bot to your server

## Step 2: Install Python Dependencies

```bash
# Navigate to the project directory
cd tempo-contract-analyzer

# Create a virtual environment (recommended)
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your favorite editor
# Add your Discord token:
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
```

**Important:** Never commit your `.env` file! It's already in `.gitignore`.

## Step 4: Run the Bot

```bash
python bot.py
```

You should see:
```
✓ Logged in as YourBotName (ID: ...)
✓ Connected to X guild(s)
✓ Synced commands globally
✓ Bot is ready!
```

## Step 5: Test in Discord

In your Discord server, type:
```
/analyze-contract 0x1234567890abcdef1234567890abcdef12345678
```

Replace with any Tempo blockchain contract address!

## Troubleshooting

### "DISCORD_TOKEN must be set"
- Make sure you created `.env` file
- Make sure you pasted your token correctly (no spaces)

### "Failed to load contract_analysis cog"
- Check that all files are in the correct directories
- Make sure `cogs/` and `analyzers/` folders exist
- Verify all `__init__.py` files are present

### "Command not showing up"
- Commands sync can take up to 1 hour globally
- For instant testing, add `DISCORD_GUILD_ID=your_server_id` to `.env`
- Get your server ID by: Right-click server → Copy Server ID (need Developer Mode enabled)

### "Failed to fetch contract"
- Verify the Tempo RPC URL is correct in `.env`
- Check if the contract address is valid
- Ensure the contract is actually deployed on Tempo chain

## Advanced Configuration

### Use Custom RPC
Edit `.env`:
```env
TEMPO_RPC_URL=https://your-custom-rpc.com
```

### Change Analysis Timeout
```env
ANALYSIS_TIMEOUT=120  # 2 minutes instead of default 60s
```

### Disable Bytecode Analysis (Verified Only)
```env
ENABLE_BYTECODE_ANALYSIS=false
```

## Running in Production

### Using Screen (Linux)
```bash
screen -S tempo-bot
python bot.py
# Press Ctrl+A then D to detach
# Reconnect with: screen -r tempo-bot
```

### Using PM2 (Recommended)
```bash
npm install -g pm2
pm2 start bot.py --name tempo-analyzer --interpreter python3
pm2 save
pm2 startup  # Follow the instructions
```

### Using Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

Build and run:
```bash
docker build -t tempo-analyzer .
docker run -d --env-file .env --name tempo-bot tempo-analyzer
```

## Security Best Practices

1. ✅ Never commit `.env` file
2. ✅ Never share your Discord bot token
3. ✅ Use a dedicated Discord bot account (don't use your main account)
4. ✅ Regularly update dependencies: `pip install -r requirements.txt --upgrade`
5. ✅ Review bot permissions (don't give admin unless needed)

## Need Help?

- Check the main README.md for detailed documentation
- Review logs in `bot.log`
- Enable debug logging: Add to `bot.py`:
  ```python
  logging.basicConfig(level=logging.DEBUG)
  ```

Happy analyzing! 🔍🛡️
