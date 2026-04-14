# Fresh Git Push Script
# Removes old git history and pushes clean

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Fresh Git Push - Clean History" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check for tokens
Write-Host "[1/5] Checking for exposed tokens..." -ForegroundColor Yellow
$tokens = Select-String -Path *.md -Pattern "MTQ5MzM4|MTIzNDU2" -SimpleMatch -ErrorAction SilentlyContinue
if ($tokens) {
    Write-Host "[ERROR] Tokens still found in files!" -ForegroundColor Red
    $tokens | ForEach-Object { Write-Host "  $($_.Filename):$($_.LineNumber)" -ForegroundColor Red }
    Write-Host ""
    Write-Host "Cannot push with secrets in files!" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "[OK] No tokens found" -ForegroundColor Green

# Remove old git
Write-Host ""
Write-Host "[2/5] Removing old git history..." -ForegroundColor Yellow
Remove-Item -Recurse -Force .git -ErrorAction SilentlyContinue
Write-Host "[OK] Old history removed" -ForegroundColor Green

# Fresh init
Write-Host ""
Write-Host "[3/5] Initializing fresh git..." -ForegroundColor Yellow
git init
git add .
git commit -m "Initial commit - Tempo Contract Analyzer Bot"
Write-Host "[OK] Fresh commit created" -ForegroundColor Green

# Add remote
Write-Host ""
Write-Host "[4/5] Connecting to GitHub..." -ForegroundColor Yellow
git remote add origin https://github.com/omertabtc/tempo-bot.git
git branch -M main
Write-Host "[OK] Connected to repo" -ForegroundColor Green

# Push
Write-Host ""
Write-Host "[5/5] Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "[INFO] This will REPLACE all GitHub history with clean version" -ForegroundColor Cyan
Write-Host ""
$confirm = Read-Host "Continue? (y/n)"
if ($confirm -ne 'y') {
    Write-Host "Cancelled." -ForegroundColor Red
    exit
}

git push -u origin main --force

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host " SUCCESS!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your code is now on GitHub (clean history)!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Go to https://railway.app/" -ForegroundColor White
    Write-Host "  2. Deploy from GitHub repo" -ForegroundColor White
    Write-Host "  3. Add environment variables" -ForegroundColor White
    Write-Host ""
    Write-Host "IMPORTANT: Regenerate your Discord token!" -ForegroundColor Yellow
    Write-Host "  https://discord.com/developers/applications/1493383531638816830/bot" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "[ERROR] Push failed!" -ForegroundColor Red
    Write-Host "Check the error message above" -ForegroundColor Red
}

pause
