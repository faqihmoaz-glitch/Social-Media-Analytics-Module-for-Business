# GitHub Setup for Windows PowerShell
# This script initializes git and prepares for GitHub push

$ErrorActionPreference = "Continue"

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor Cyan
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Status {
    param([string]$Message, [string]$Status = "INFO")
    $Color = @{
        "INFO" = "White"
        "OK" = "Green"
        "ERROR" = "Red"
        "SETUP" = "Yellow"
        "WARN" = "Magenta"
    }
    Write-Host "[$Status] $Message" -ForegroundColor $Color[$Status]
}

Write-Section "GIT INSTALLATION CHECK"

# Check if git is installed
try {
    $gitVersion = & git --version 2>$null
    Write-Status $gitVersion "OK"
}
catch {
    Write-Status "Git is not installed or not in PATH" "ERROR"
    Write-Host ""
    Write-Host "❌ Please install Git from: https://git-scm.com/download/win" -ForegroundColor Red
    Write-Host "   After installation, restart PowerShell and run this script again"
    Write-Host ""
    Read-Host "Press Enter to continue"
    exit 1
}

# Set working directory
$projectDir = "C:\Users\lab6\Documents\B864"
Set-Location $projectDir
Write-Status "Working directory: $(Get-Location)" "INFO"

Write-Section "GIT REPOSITORY SETUP"

# Initialize git repository
if (-not (Test-Path .git)) {
    Write-Status "Initializing git repository..." "SETUP"
    & git init | Out-Null
    Write-Status "Repository initialized" "OK"
}
else {
    Write-Status "Git repository already exists" "INFO"
}

# Configure git user
Write-Status "Configuring git user..." "SETUP"
& git config --global user.name "Social Media Analytics Team" | Out-Null
& git config --global user.email "team@socialmediaanalytics.dev" | Out-Null
Write-Status "Git user configured" "OK"

# Stage all files
Write-Status "Staging files..." "SETUP"
& git add . | Out-Null
Write-Status "Files staged" "OK"

# Show what will be committed
Write-Host ""
Write-Status "Files to commit:" "INFO"
Write-Host ""
& git status --short
Write-Host ""

# Create commit
Write-Status "Creating initial commit..." "SETUP"
$commitMessage = @"
Initial commit: Social Media Analytics Module for Business

- Complete sentiment analysis with VADER + TextBlob
- Multi-content analysis (text, images, audio, video, emojis)
- Professional visualizations (Pygal, Matplotlib, Word Clouds)
- Comprehensive dashboard and JSON reports
- Batch processing and real-time analytics
- Full documentation and examples
"@

& git commit -m $commitMessage | Out-Null
Write-Status "Commit created" "OK"

# Get commit hash
$commitHash = & git rev-parse --short HEAD 2>$null
Write-Host "Commit: $commitHash" -ForegroundColor Green
Write-Host ""

# Rename branch to main
Write-Status "Setting main branch..." "SETUP"
& git branch -M main | Out-Null
Write-Status "Branch set to main" "OK"

# Display git log
Write-Host ""
Write-Status "Recent commits:" "INFO"
& git log --oneline -5
Write-Host ""

Write-Section "NEXT STEPS: CONNECT TO GITHUB"

$instructions = @"
1️⃣  CREATE REPOSITORY ON GITHUB:
   • Go to: https://github.com/new
   • Repository name: social_media_analytics
   • Description: A comprehensive Python-based social media analytics system
   • Choose: Public (recommended) or Private
   • Click: Create repository
   • Copy the HTTPS URL

2️⃣  ADD GITHUB REMOTE:
   Run this command (replace YOUR_USERNAME):
   
   git remote add origin https://github.com/YOUR_USERNAME/social_media_analytics.git

3️⃣  PUSH TO GITHUB:
   git push -u origin main

4️⃣  AUTHENTICATE:
   Git will ask for your username and password
   - Username: Your GitHub username
   - Password: Your GitHub personal access token
   
   Get token from: https://github.com/settings/tokens

5️⃣  VERIFY:
   Check your GitHub repository at:
   https://github.com/YOUR_USERNAME/social_media_analytics

"@

Write-Host $instructions

Write-Section "QUICK REFERENCE - FUTURE COMMITS"

$future = @"
To update your repository in the future:

   git add .
   git commit -m "Your commit message"
   git push

For branches and collaboration:
   git checkout -b feature/feature-name
   git add .
   git commit -m "Add feature"
   git push origin feature/feature-name

"@

Write-Host $future

Write-Section "PROJECT STRUCTURE PUSHED"

Write-Host "Your GitHub repository will contain:" -ForegroundColor Yellow
Write-Host ""
Write-Host "📁 social_media_analytics/" -ForegroundColor Green
Write-Host "   ├─ main.py (entry point)" -ForegroundColor Green
Write-Host "   ├─ config.py (configuration)" -ForegroundColor Green
Write-Host "   ├─ requirements.txt (dependencies)" -ForegroundColor Green
Write-Host "   ├─ README.md (full documentation)" -ForegroundColor Green
Write-Host "   ├─ LICENSE (MIT license)" -ForegroundColor Green
Write-Host "   ├─ .gitignore (git ignore rules)" -ForegroundColor Green
Write-Host "   ├─ .github_config.json (GitHub settings)" -ForegroundColor Green
Write-Host "   │" -ForegroundColor Green
Write-Host "   ├─ analyzers/" -ForegroundColor Green
Write-Host "   │  ├─ text_analyzer.py (VADER + TextBlob)" -ForegroundColor Green
Write-Host "   │  ├─ emoji_analyzer.py (emoji analysis)" -ForegroundColor Green
Write-Host "   │  ├─ image_analyzer.py (color analysis)" -ForegroundColor Green
Write-Host "   │  ├─ audio_analyzer.py (speech to text)" -ForegroundColor Green
Write-Host "   │  └─ video_analyzer.py (frame analysis)" -ForegroundColor Green
Write-Host "   │" -ForegroundColor Green
Write-Host "   ├─ visualizations/" -ForegroundColor Green
Write-Host "   │  ├─ charts.py (Pygal `& Matplotlib)" -ForegroundColor Green
Write-Host "   │  ├─ wordcloud_gen.py (word clouds)" -ForegroundColor Green
Write-Host "   │  └─ dashboard.py (dashboard `& reports)" -ForegroundColor Green
Write-Host "   │" -ForegroundColor Green
Write-Host "   ├─ data/" -ForegroundColor Green
Write-Host "   │  ├─ sample_posts.json" -ForegroundColor Green
Write-Host "   │  └─ stopwords.txt" -ForegroundColor Green
Write-Host "   │" -ForegroundColor Green
Write-Host "   └─ output/ (generated outputs)" -ForegroundColor Green
Write-Host ""

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  ✅ GIT REPOSITORY READY FOR GITHUB!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to close this window"
