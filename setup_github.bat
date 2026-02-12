@echo off
REM GitHub Setup for Windows PowerShell
REM This script initializes git and pushes to GitHub

echo.
echo ======================================================================
echo   GIT INSTALLATION CHECK
echo ======================================================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not installed or not in PATH
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo After installation, restart this script
    echo.
    pause
    exit /b 1
)

echo [OK] Git is installed
git --version
echo.

REM Navigate to project directory
cd /d "C:\Users\lab6\Documents\B864"
echo [INFO] Working directory: %CD%
echo.

echo ======================================================================
echo   GIT REPOSITORY SETUP
echo ======================================================================
echo.

REM Initialize git repository
if not exist ".git" (
    echo [SETUP] Initializing git repository...
    git init
    echo [OK] Repository initialized
) else (
    echo [INFO] Git repository already exists
)
echo.

REM Configure git user
echo [SETUP] Configuring git user...
git config --global user.name "Social Media Analytics Team"
git config --global user.email "team@socialmediaanalytics.dev"
echo [OK] Git user configured
echo.

REM Stage all files
echo [SETUP] Staging files...
git add .
echo [OK] Files staged
echo.

REM Show what will be committed
echo [INFO] Files to commit:
git status --short
echo.

REM Create commit
echo [SETUP] Creating initial commit...
git commit -m "Initial commit: Social Media Analytics Module for Business

- Complete sentiment analysis with VADER + TextBlob
- Multi-content analysis (text, images, audio, video, emojis)
- Professional visualizations (Pygal, Matplotlib, Word Clouds)
- Comprehensive dashboard and JSON reports
- Batch processing and real-time analytics"

echo.
echo [OK] Commit created
echo.

REM Rename branch to main
echo [SETUP] Setting main branch...
git branch -M main
echo [OK] Branch set to main
echo.

REM Display next steps
echo ======================================================================
echo   NEXT STEPS: CONNECT TO GITHUB
echo ======================================================================
echo.
echo 1. Go to: https://github.com/new
echo    - Repository name: social_media_analytics
echo    - Description: A comprehensive Python-based social media analytics system
echo    - Choose: Public or Private
echo    - Click: Create repository
echo    - Copy the HTTPS URL
echo.
echo 2. Run this command (replace YOUR_USERNAME):
echo    git remote add origin https://github.com/YOUR_USERNAME/social_media_analytics.git
echo.
echo 3. Push to GitHub:
echo    git push -u origin main
echo.
echo 4. Verify at: https://github.com/YOUR_USERNAME/social_media_analytics
echo.
echo ======================================================================
echo.

pause
