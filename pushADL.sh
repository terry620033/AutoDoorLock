#!/bin/bash

# Variables
GITHUB_USERNAME="terry620033"  # Replace with your actual GitHub username
REPO_NAME="AutoDoorLock"
EMAIL="terry620033@gmail.com"
WORK_DIR="$HOME/Kubernetes/Deployment/Ansible/AutoDoorLock"
REMOTE_SSH_URL="git@github.com:$GITHUB_USERNAME/$REPO_NAME.git"

echo "📁 Changing to project directory: $WORK_DIR"
cd "$WORK_DIR" || { echo "❌ Directory not found"; exit 1; }

echo "🔧 Initializing git repository..."
git init

echo "📝 Creating .gitignore..."
cat <<EOF > .gitignore
*.log
__pycache__/
EOF

echo "📄 Adding files..."
git add .

echo "📸 Committing changes..."
git commit -m "Initial commit"

echo "🔑 Generating SSH key (if not exists)..."
SSH_KEY="$HOME/.ssh/id_ed25519"
if [ ! -f "$SSH_KEY" ]; then
  ssh-keygen -t ed25519 -C "$EMAIL" -f "$SSH_KEY" -N ""
  eval "$(ssh-agent -s)"
  ssh-add "$SSH_KEY"
  echo "📋 Copy this SSH key and add to your GitHub SSH settings:"
  echo "🔐 ------------------"
  cat "$SSH_KEY.pub"
  echo "🔐 ------------------"
  echo "➡️ Visit https://github.com/settings/ssh/new and paste the key above."
  read -p "⏸️ Press Enter once you've added the SSH key to GitHub..."
else
  echo "✅ SSH key already exists."
fi

echo "🔗 Setting remote origin to SSH..."
git remote add origin "$REMOTE_SSH_URL" 2>/dev/null || git remote set-url origin "$REMOTE_SSH_URL"

echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main --force

echo "✅ Done! Your project is now on GitHub."

