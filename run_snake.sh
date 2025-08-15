#!/bin/bash

echo "================================"
echo "    TERMINAL SNAKE GAME"
echo "================================"
echo ""
echo "Controls:"
echo "  Arrow Keys or WASD - Move snake"
echo "  SPACE - Restart after game over"
echo "  Q or ESC - Quit game"
echo ""
echo "Press any key to start..."
read -n 1

# Run the game (no virtual environment needed for terminal version)
python main.py