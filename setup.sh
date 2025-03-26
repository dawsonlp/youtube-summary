#!/bin/bash
# Simple setup script for YouTube Summary Tool

echo "Setting up YouTube Summary Tool..."

# Check for Python 3.10+
python_version=$(python3 --version 2>&1 | awk '{print $2}')
python_major=$(echo $python_version | cut -d. -f1)
python_minor=$(echo $python_version | cut -d. -f2)

if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 10 ]); then
    echo "Error: Python 3.10+ is required but you have $python_version"
    echo "Please install Python 3.10 or higher before continuing."
    exit 1
fi

echo "✓ Python $python_version detected"

# Check for Poetry
if ! command -v poetry &> /dev/null; then
    echo "Poetry not found. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Update PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    
    if ! command -v poetry &> /dev/null; then
        echo "Failed to install Poetry. Please install manually:"
        echo "curl -sSL https://install.python-poetry.org | python3 -"
        exit 1
    fi
fi

echo "✓ Poetry installation verified"

# Install dependencies
echo "Installing project dependencies..."
poetry install
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    exit 1
fi

echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ Configuration file created"
else
    echo "✓ Configuration file already exists"
fi

# Check if Ollama is installed (only if using default provider)
if grep -q "SUMMARY_PROVIDER=ollama" .env; then
    if ! command -v ollama &> /dev/null; then
        echo "Warning: Ollama is not installed or not in your PATH."
        echo "The default configuration uses Ollama for summarization."
        echo "To install Ollama, visit: https://ollama.ai/download"
        echo ""
        echo "Alternatively, edit .env to use a different provider."
    else
        echo "✓ Ollama installation verified"
        
        # Check if the specified model is available
        model=$(grep "OLLAMA_MODEL=" .env | cut -d= -f2)
        if ! ollama list | grep -q "$model"; then
            echo "Downloading Ollama model $model..."
            ollama pull $model
            if [ $? -ne 0 ]; then
                echo "Warning: Failed to download Ollama model. You may need to manually run: ollama pull $model"
            else
                echo "✓ Ollama model $model installed"
            fi
        else
            echo "✓ Ollama model $model already installed"
        fi
    fi
fi

echo ""
echo "Setup complete! You can now use YouTube Summary:"
echo ""
echo "  poetry run youtube-summary summarize \"https://www.youtube.com/watch?v=TdAAUoJ065o\""
echo ""
echo "Or make the script executable and run it directly:"
echo ""
echo "  chmod +x setup.sh"
echo "  ./setup.sh"
echo ""
