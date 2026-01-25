#!/bin/bash
# install.sh — Create a personal Paper Digest instance
# Usage: curl -sL https://raw.githubusercontent.com/champagnealexandre/paperdigest/main/scripts/install.sh | bash

set -e

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║       Paper Digest Installer          ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Get user input
read -p "Your GitHub username: " GITHUB_USER
read -p "New repo name [paperdigest-personal]: " REPO_NAME
REPO_NAME=${REPO_NAME:-paperdigest-personal}

echo ""
echo "Cloning paperdigest template..."
git clone https://github.com/champagnealexandre/paperdigest.git "$REPO_NAME"
cd "$REPO_NAME"

echo "Setting up git remotes..."
git remote rename origin upstream
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"

echo "Creating example LOI data directory..."
mkdir -p data/example
echo "[]" > data/example/papers.json
cat > data/example/decisions.md << 'EOF'
| Status | Score | Paper |
|--------|-------|-------|
EOF

echo ""
echo "════════════════════════════════════════"
echo "Installation complete!"
echo "════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Create an empty PRIVATE repo on GitHub:"
echo "   https://github.com/new?name=$REPO_NAME&visibility=private"
echo ""
echo "2. Push to your repo:"
echo "   cd $REPO_NAME"
echo "   git push -u origin main"
echo ""
echo "3. Create your LOI config:"
echo "   cp config/loi/_example.yaml config/loi/my-topic.yaml"
echo "   # Edit the file with your keywords and prompt"
echo ""
echo "4. Create your LOI data directory:"
echo "   mkdir -p data/my-topic"
echo "   echo '[]' > data/my-topic/papers.json"
echo ""
echo "5. Add your OPENROUTER_API_KEY secret:"
echo "   https://github.com/$GITHUB_USER/$REPO_NAME/settings/secrets/actions"
echo ""
echo "6. Run locally to test:"
echo "   python3 -m venv venv && source venv/bin/activate"
echo "   pip install -r requirements.txt"
echo "   export OPENROUTER_API_KEY='your_key'"
echo "   python main.py"
echo ""