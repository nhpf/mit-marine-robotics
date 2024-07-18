#!/bin/sh

# Clone the GroundingDINO repository
git clone https://github.com/IDEA-Research/GroundingDINO.git

# Change to the GroundingDINO directory
cd GroundingDINO/

# List files (optional)
ls

# Install the package in editable mode
pip install -e .

# Create weights directory
mkdir weights

# Change to weights directory
cd weights

# Download the weights file
wget -q https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth

# Return to previous directory
cd ..
