#!/bin/bash
# Script d'installation automatique pour VPS Ubuntu
# Usage: curl -sL https://raw.githubusercontent.com/your-repo/setup_vps.sh | bash

echo "=========================================="
echo " Installation Tempo Bot sur VPS"
echo "=========================================="
echo ""

# Vérification Ubuntu
if ! grep -q "Ubuntu" /etc/os-release; then
    echo "⚠️  Ce script est pour Ubuntu uniquement!"
    exit 1
fi

echo "[1/7] Mise à jour du système..."
apt update -qq && apt upgrade -y -qq

echo "[2/7] Installation Python 3.11..."
apt install -y python3.11 python3.11-pip python3.11-venv git curl -qq

echo "[3/7] Installation Node.js et PM2..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash - > /dev/null 2>&1
apt install -y nodejs -qq
npm install -g pm2 --silent

echo "[4/7] Création du dossier bot..."
cd /root
mkdir -p tempo-bot
cd tempo-bot

echo "[5/7] Téléchargement des fichiers..."
echo "⚠️  ATTENTION: Tu dois maintenant:"
echo "    1. Upload tes fichiers avec: scp -r tempo-contract-analyzer root@IP:/root/tempo-bot/"
echo "    2. Ou clone depuis GitHub: git clone URL /root/tempo-bot"
echo ""
read -p "Appuie sur Enter quand c'est fait..."

echo "[6/7] Installation des dépendances Python..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --quiet
    echo "✓ Dépendances installées"
else
    echo "✗ requirements.txt non trouvé!"
    echo "  Assure-toi d'avoir uploadé les fichiers"
    exit 1
fi

echo "[7/7] Configuration..."
if [ ! -f ".env" ]; then
    echo ""
    echo "=========================================="
    echo " Configuration du bot"
    echo "=========================================="
    echo ""
    read -p "Discord Bot Token: " DISCORD_TOKEN
    read -p "Tempo RPC URL [https://rpc.tempo.xyz]: " TEMPO_RPC
    TEMPO_RPC=${TEMPO_RPC:-https://rpc.tempo.xyz}
    
    cat > .env << EOF
DISCORD_TOKEN=$DISCORD_TOKEN
TEMPO_RPC_URL=$TEMPO_RPC
TEMPO_EXPLORER_API=https://contracts.tempo.xyz/api
TEMPO_CHAIN_ID=42431
EOF
    echo "✓ Fichier .env créé"
fi

echo ""
echo "=========================================="
echo " Test du bot..."
echo "=========================================="
echo ""
echo "On va tester que le bot démarre..."
timeout 10s python3 bot.py &
sleep 8
pkill -f bot.py

echo ""
echo "=========================================="
echo " Démarrage avec PM2"
echo "=========================================="
pm2 start bot.py --name tempo-bot --interpreter python3
pm2 save
pm2 startup

echo ""
echo "=========================================="
echo " ✓ INSTALLATION TERMINÉE!"
echo "=========================================="
echo ""
echo "Commandes utiles:"
echo "  pm2 status          - Voir le statut"
echo "  pm2 logs tempo-bot  - Voir les logs"
echo "  pm2 restart tempo-bot - Redémarrer"
echo "  pm2 stop tempo-bot    - Arrêter"
echo ""
echo "Ton bot devrait être ONLINE sur Discord! 🎉"
echo ""
