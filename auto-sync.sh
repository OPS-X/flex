#!/bin/bash

# Check for any changes in the remote repository
git pull origin main

# Add all changes to staging
git add .

# Commit changes with a timestamp message
git commit -m "Auto-sync: $(date)"

# Push changes to the main branch
git push origin main
