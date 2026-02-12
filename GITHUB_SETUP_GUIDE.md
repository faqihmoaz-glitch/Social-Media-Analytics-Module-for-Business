# COMPLETE GITHUB SETUP GUIDE

This guide will help you push your Social Media Analytics project to GitHub in just a few minutes!

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start (3 minutes)](#quick-start)
3. [Detailed Instructions](#detailed-instructions)
4. [Troubleshooting](#troubleshooting)
5. [Future Updates](#future-updates)

---

## 📋 Prerequisites

Before you begin, make sure you have:

- [ ] **Git installed** - Download from https://git-scm.com/download/win
- [ ] **GitHub account** - Free at https://github.com
- [ ] **GitHub personal access token** - Create at https://github.com/settings/tokens
  - Scopes needed: `repo`, `gist`, `user`, `workflow`
  - Note: Don't share this token!

---

## 🚀 Quick Start (3 minutes)

### Step 1: Install Git
1. Download Git: https://git-scm.com/download/win
2. Run installer (accept all defaults)
3. **Important: Restart your terminal/PowerShell after installation**

### Step 2: Run Setup Script
Open PowerShell in the `B864` folder and run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
.\setup_github.ps1
```

Or run the batch file:
```cmd
setup_github.bat
```

### Step 3: Create GitHub Repository
1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `social_media_analytics`
   - **Description:** `A comprehensive Python-based social media analytics system`
   - **Visibility:** Choose Public or Private
3. Click **Create repository**
4. **Copy the HTTPS URL** (looks like: `https://github.com/YOUR_USERNAME/social_media_analytics.git`)

### Step 4: Connect Local to GitHub
Open PowerShell in the `B864` folder and run (replace URL):

```powershell
git remote add origin https://github.com/YOUR_USERNAME/social_media_analytics.git
git push -u origin main
```

When prompted:
- **Username:** Your GitHub username
- **Password:** Your personal access token (from prerequisites)

### ✅ Done! 
Your repository is now on GitHub at:
```
https://github.com/YOUR_USERNAME/social_media_analytics
```

---

## 📝 Detailed Instructions

### Section A: Install Git

#### Windows - GUI Installer (Recommended)
1. Visit: https://git-scm.com/download/win
2. Download the latest installer
3. Run the .exe file
4. Click through the installer (accept defaults):
   - ✓ Use Git from the Windows Command Prompt
   - ✓ Use the native Windows Secure Channel library
   - ✓ Checkout Windows-style, commit Unix-style line endings
   - ✓ Use MinTTY (the default terminal of MSYS2)
5. Click **Install**
6. Uncheck "View Release Notes"
7. Click **Finish**
8. **Restart PowerShell completely** (close and reopen)

#### Verify Installation
Open PowerShell and run:
```powershell
git --version
```

You should see something like: `git version 2.43.0.windows.1`

### Section B: Create GitHub Account & Token

#### Create GitHub Account
1. Go to https://github.com/join
2. Enter username, email, password
3. Verify your email
4. Answer setup questions (optional)
5. Done!

#### Create Personal Access Token
1. Go to https://github.com/settings/tokens/new
2. **Token name:** `Social Media Analytics`
3. **Expiration:** 90 days (or custom)
4. **Scopes to select:**
   - ✓ repo (all)
   - ✓ gist
   - ✓ user (all)
   - ✓ workflow
5. Click **Generate token**
6. **⚠️ Copy the token immediately** - you won't see it again!
7. Store safely (password manager)

### Section C: Run Setup Script

#### Option 1: PowerShell (Recommended)

1. **Open PowerShell as Administrator:**
   - Press Windows key
   - Type "PowerShell"
   - Right-click "Windows PowerShell"
   - Click "Run as administrator"

2. **Navigate to project:**
   ```powershell
   cd C:\Users\lab6\Documents\B864
   ```

3. **Enable script execution (first time only):**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
   ```

4. **Run the setup script:**
   ```powershell
   .\setup_github.ps1
   ```

#### Option 2: Batch File (Simpler)

1. **Open Command Prompt** (cmd.exe)
2. **Navigate to project:**
   ```cmd
   cd C:\Users\lab6\Documents\B864
   ```
3. **Run batch file:**
   ```cmd
   setup_github.bat
   ```

#### Option 3: Manual Git Commands

1. **Open PowerShell**
2. **Navigate to project:**
   ```powershell
   cd C:\Users\lab6\Documents\B864
   ```
3. **Run these commands:**
   ```powershell
   # Initialize repository (if not already done)
   git init
   
   # Configure your user
   git config --global user.name "Your Name"
   git config --global user.email "your.email@github.com"
   
   # Stage all files
   git add .
   
   # Create commit
   git commit -m "Initial commit: Social Media Analytics Module for Business
   
   - Complete sentiment analysis with VADER + TextBlob
   - Multi-content analysis (text, images, audio, video, emojis)
   - Professional visualizations (Pygal, Matplotlib, Word Clouds)
   - Comprehensive dashboard and JSON reports
   - Batch processing and real-time analytics"
   
   # Rename branch to main
   git branch -M main
   ```

### Section D: Create GitHub Repository

1. **Log in to GitHub** at https://github.com
2. **Go to:** https://github.com/new
3. **Fill in the form:**

   | Field | Value |
   |-------|-------|
   | Repository name | `social_media_analytics` |
   | Description | `A comprehensive Python-based social media analytics system` |
   | Visibility | Public (or Private) |
   | Initialize repository | ❌ (leave unchecked) |

4. **Click "Create repository"**
5. **You'll see a page with three options - select the second one:**
   ```
   …or push an existing repository from the command line
   ```
6. **Copy the two commands shown** (look like the code below)

### Section E: Push to GitHub

After creating your GitHub repository, you'll see instructions. Here's what to do:

1. **Open PowerShell** in your B864 project folder

2. **Add remote (replace YOUR_USERNAME):**
   ```powershell
   git remote add origin https://github.com/YOUR_USERNAME/social_media_analytics.git
   ```

3. **Verify remote was added:**
   ```powershell
   git remote -v
   ```
   
   Should show:
   ```
   origin  https://github.com/YOUR_USERNAME/social_media_analytics.git (fetch)
   origin  https://github.com/YOUR_USERNAME/social_media_analytics.git (push)
   ```

4. **Push to GitHub:**
   ```powershell
   git push -u origin main
   ```

5. **When prompted:**
   - **Username:** Enter your GitHub username
   - **Password:** Paste your personal access token (not your GitHub password!)

6. **Wait for upload** - depending on internet speed, this takes 10-30 seconds

7. **Success message:**
   ```
   Enumerating objects: X, done.
   Counting objects: 100% (X/X), done.
   ...
   To https://github.com/YOUR_USERNAME/social_media_analytics.git
    * [new branch]      main -> main
   Branch 'main' set up to track remote branch 'main' from 'origin'.
   ```

### Step F: Verify Upload

1. **Go to your GitHub repository:**
   ```
   https://github.com/YOUR_USERNAME/social_media_analytics
   ```

2. **You should see:**
   - ✓ All your files and folders
   - ✓ README.md displayed
   - ✓ LICENSE file listed
   - ✓ green "commits" badge showing "1 commit"

---

## ❌ Troubleshooting

### Problem: "git is not recognized as an internal or external command"

**Solution:**
1. Close PowerShell completely
2. Install Git from https://git-scm.com/download/win
3. Restart computer (not just PowerShell)
4. Open PowerShell again and try again

### Problem: "fatal: object directory has 16 objects, but index contains 17 objects"

**Solution:**
```powershell
rm -r .git
git init
git add .
git commit -m "Initial commit"
```

### Problem: "128 fatal: setting certificate verify failed while accessing repository"

**Temporary solution:**
```powershell
git config --global http.sslVerify false
git push -u origin main
```

**Permanent solution:** Update Git to latest version

### Problem: "Support for password authentication was removed. Please use a personal access token instead."

**Solution:**
1. Delete saved credentials: Open Credential Manager (Windows)
2. Go to: Windows Credentials → Generic Credentials
3. Find and delete GitHub entries
4. Try pushing again - use token as password

### Problem: git config user.name doesn't stick

**Solution:**
```powershell
# Configure globally (for all projects)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Verify
git config --global user.name
```

### Problem: "repository not found"

**Causes:**
- Repository doesn't exist yet (create at github.com/new)
- Wrong URL (check for typos in username)
- Not authenticated (use correct token as password)

---

## 🔄 Future Updates

Once your repository is set up, updating it is easy:

### Make Changes
```powershell
# Edit files in your project
# ...save all changes...

# Check status
git status
```

### Stage & Commit Changes
```powershell
# Stage all changes
git add .

# Create a commit describing your changes
git commit -m "Brief description of changes"

# Examples:
git commit -m "Add emoji sentiment analysis"
git commit -m "Fix word cloud generation"
git commit -m "Update documentation"
```

### Push to GitHub
```powershell
# Upload commits to GitHub
git push

# Or if it's a new branch:
git push -u origin branch-name
```

### View Commit History
```powershell
# See your commits
git log --oneline

# See last 10 commits
git log --oneline -10

# See commits in one line in a graph
git log --oneline --graph --all
```

### Create a Branch for New Features
```powershell
# Create and switch to new branch
git checkout -b feature/new-feature-name

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push branch to GitHub
git push -u origin feature/new-feature-name

# Create Pull Request on GitHub to merge back to main
```

---

## 📚 Useful Git Commands Reference

```powershell
# Basic workflow
git status              # Check what changed
git add .               # Stage all changes
git commit -m "..."     # Commit with message
git push                # Upload to GitHub
git pull                # Download latest from GitHub

# Branching
git branch              # List branches
git branch -a           # List all branches (local + remote)
git checkout -b name    # Create new branch
git checkout name       # Switch to branch
git branch -d name      # Delete branch

# Viewing
git log                 # See commit history
git diff                # See changes not staged
git diff --staged       # See staged changes

# Undoing changes
git restore file        # Discard changes in file
git reset HEAD~1        # Undo last commit (keep changes)
git revert HEAD         # Create new commit that undoes last commit

# Remote
git remote -v           # List remotes
git remote add name url # Add new remote
git push origin main    # Push branch to remote
git pull origin main    # Pull branch from remote
```

---

## ✅ Checklist - You're All Set!

- [ ] Git installed and working
- [ ] GitHub account created
- [ ] Personal access token generated
- [ ] Repository initialized locally
- [ ] Files staged and committed
- [ ] GitHub repository created
- [ ] Remote added
- [ ] Pushed to GitHub successfully
- [ ] Verified files on GitHub

---

## 🎉 You Did It!

Your Social Media Analytics project is now on GitHub! 

Next steps:
- Share the repository link with others
- Add topics/tags on GitHub settings
- Create Issues for features/bugs
- Invite collaborators
- Enable GitHub Pages for documentation
- Set up GitHub Actions for CI/CD

---

**For more help:**
- GitHub Docs: https://docs.github.com
- Git Docs: https://git-scm.com/doc
- Stack Overflow: https://stackoverflow.com/questions/tagged/git

**Happy coding! 🚀**
