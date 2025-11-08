#!/bin/bash

# Railway deployment script for Urban Mobility Analytics API

echo "Deploying Urban Mobility Analytics API to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null
then
    echo "Railway CLI could not be found. Please install it first:"
    echo "npm install -g @railway/cli"
    exit 1
fi

# Login to Railway (if not already logged in)
echo "Please login to Railway if prompted..."
railway login

# Deploy to Railway
railway up

echo "Deployment completed!"
echo "Your API will be available at: $(railway url)"