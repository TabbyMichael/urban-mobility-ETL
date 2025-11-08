#!/bin/bash

# Vercel deployment script for Urban Mobility Analytics Dashboard

echo "Deploying Urban Mobility Analytics Dashboard to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null
then
    echo "Vercel CLI could not be found. Please install it first:"
    echo "npm install -g vercel"
    exit 1
fi

# Login to Vercel (if not already logged in)
echo "Please login to Vercel if prompted..."
vercel login

# Deploy to Vercel
vercel --prod

echo "Deployment completed!"
echo "Your dashboard will be available at: $(vercel --prod --token=$(vercel token) 2>/dev/null)"