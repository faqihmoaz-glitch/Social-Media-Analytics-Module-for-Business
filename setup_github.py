#!/usr/bin/env python3
"""
GitHub Setup Automation Script
Initializes git repository and prepares for GitHub push
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description=""):
    """Execute shell command and return result"""
    if description:
        print(f"  ⏳ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            if description:
                print(f"  ✅ {description}")
            return result.stdout.strip()
        else:
            if description:
                print(f"  ❌ {description}")
            print(f"     Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return None

def setup_git_repo():
    """Initialize and configure git repository"""
    print("\n" + "="*60)
    print("  🚀 GITHUB REPOSITORY SETUP")
    print("="*60 + "\n")

    base_dir = Path(__file__).parent

    # Change to project directory
    os.chdir(base_dir)
    print(f"📁 Working directory: {os.getcwd()}\n")

    # Initialize git repository
    if not (base_dir / ".git").exists():
        run_command("git init", "Initializing git repository")
    else:
        print("  ℹ️  Git repository already initialized")

    # Configure git user (global if not already set)
    print("\n  📝 Configuring git user...")
    run_command('git config --global user.name "Social Media Analytics Bot"', "Setting git username")
    run_command('git config --global user.email "analytics@example.com"', "Setting git email")

    # Add all files
    print("\n  📂 Staging files...")
    run_command("git add .", "Staging all files")

    # Check git status
    status = run_command("git status --porcelain", "Getting repository status")
    if status:
        print(f"\n  📊 Files to commit:\n{status}")
    else:
        print("  ℹ️  No changes to commit")
        return False

    # Create initial commit
    commit_msg = """Initial commit: Social Media Analytics Module for Business

- Complete sentiment analysis with VADER + TextBlob
- Multi-content analysis (text, images, audio, video, emojis)
- Professional visualizations (Pygal, Matplotlib, Word Clouds)
- Comprehensive dashboard and JSON reports
- Batch processing and real-time analytics
- Full documentation and examples"""

    print("\n  💾 Creating commit...")
    cmd = f'git commit -m "{commit_msg}"'
    run_command(cmd, "Committing changes")

    # Get commit hash
    commit_hash = run_command("git rev-parse --short HEAD")
    if commit_hash:
        print(f"\n  ✨ Commit created: {commit_hash}")
    
    # Rename branch to main
    run_command("git branch -M main", "Renaming branch to 'main'")

    return True

def display_github_instructions():
    """Display instructions for GitHub connection"""
    print("\n" + "="*60)
    print("  📝 GITHUB CONNECTION INSTRUCTIONS")
    print("="*60 + "\n")

    instructions = """
1️⃣  CREATE REPOSITORY ON GITHUB:
   • Go to: https://github.com/new
   • Repository name: social_media_analytics
   • Description: A comprehensive Python-based system for analyzing 
     social media content with advanced sentiment analysis and visualizations
   • Choose: Public (recommended) or Private
   • Click: "Create repository"
   • Copy the HTTPS URL from the page

2️⃣  ADD GITHUB REMOTE:
   Run this command (replace URL with your repository URL):
   
   git remote add origin https://github.com/YOUR_USERNAME/social_media_analytics.git

3️⃣  PUSH TO GITHUB:
   git branch -M main
   git push -u origin main

4️⃣  VERIFY:
   Check your GitHub repository at:
   https://github.com/YOUR_USERNAME/social_media_analytics

✨ FUTURE COMMITS:
   After initial setup, use these commands for future updates:
   
   git add .
   git commit -m "Your commit message"
   git push

"""
    print(instructions)

def create_github_config():
    """Create GitHub configuration file"""
    config = {
        "repository": "social_media_analytics",
        "description": "A comprehensive Python-based system for analyzing social media content",
        "topics": [
            "sentiment-analysis",
            "social-media",
            "text-analysis",
            "data-visualization",
            "emoji-analysis",
            "image-analysis",
            "audio-analysis",
            "video-analysis",
            "python",
            "analytics"
        ],
        "keywords": [
            "sentiment analysis",
            "social media analytics",
            "VADER",
            "TextBlob",
            "word cloud",
            "visualization",
            "data science"
        ]
    }
    
    config_file = Path(__file__).parent / ".github_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"  ✅ GitHub configuration saved to {config_file}")

def main():
    """Main execution"""
    try:
        # Setup git repository
        if setup_git_repo():
            print("\n" + "="*60)
            print("  ✅ GIT REPOSITORY READY!")
            print("="*60)
            
            # Create GitHub config
            create_github_config()
            
            # Display instructions
            display_github_instructions()
            
            print("\n" + "="*60)
            print("  📌 QUICK REFERENCE")
            print("="*60)
            print("""
To authenticate with GitHub, you have two options:

Option A: HTTPS with Personal Access Token (Recommended)
   1. Go to: https://github.com/settings/tokens
   2. Click "Generate new token"
   3. Select scopes: repo, write:repo_hook
   4. Generate and copy the token
   5. When git asks for password, paste the token

Option B: SSH Key (More secure)
   1. Generate SSH key: ssh-keygen -t ed25519 -C "your@email.com"
   2. Add to GitHub: https://github.com/settings/ssh/new
   3. Test: ssh -T git@github.com
   4. Use SSH URL: git@github.com:USERNAME/repo.git

""")
            
            print("="*60)
            print("  🎉 Setup Complete! Ready for GitHub push.")
            print("="*60 + "\n")
        else:
            print("\n⚠️  Setup failed. Please check the errors above.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
