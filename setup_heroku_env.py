#!/usr/bin/env python3
"""
Script to help set up environment variables in Heroku for AWS S3 and other services.
Run this script to get the commands you need to run in your terminal.
"""

import os

def print_heroku_commands():
    print("=== HEROKU ENVIRONMENT VARIABLES SETUP ===")
    print("\nRun these commands in your terminal to set up your Heroku environment variables:")
    print("\n# AWS S3 Configuration:")
    print("heroku config:set USE_AWS=True")
    print("heroku config:set AWS_ACCESS_KEY_ID=your-aws-access-key-id")
    print("heroku config:set AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key")
    
    print("\n# Django Configuration:")
    print("heroku config:set SECRET_KEY=your-django-secret-key")
    
    print("\n# Stripe Configuration:")
    print("heroku config:set STRIPE_PUBLIC_KEY=your-stripe-public-key")
    print("heroku config:set STRIPE_SECRET_KEY=your-stripe-secret-key")
    print("heroku config:set STRIPE_WH_SECRET=your-stripe-webhook-secret")
    
    print("\n# Email Configuration:")
    print("heroku config:set EMAIL_HOST_USER=your-email@example.com")
    print("heroku config:set EMAIL_HOST_PASS=your-email-password")
    print("heroku config:set DEFAULT_FROM_EMAIL=your-email@example.com")
    
    print("\n# To check your current config:")
    print("heroku config")
    
    print("\n# To view logs and debug:")
    print("heroku logs --tail")

def check_aws_bucket():
    print("\n=== AWS S3 BUCKET CHECKLIST ===")
    print("Make sure your AWS S3 bucket 'nothingspecial-project' is set up correctly:")
    print("1. Bucket name: nothingspecial-project")
    print("2. Region: eu-west-2")
    print("3. Bucket permissions allow public read access")
    print("4. CORS configuration allows your domain")
    print("5. IAM user has proper S3 permissions")

def check_static_files():
    print("\n=== STATIC FILES CHECKLIST ===")
    print("1. Run 'python manage.py collectstatic' locally")
    print("2. Make sure your static files are in the correct location")
    print("3. Check that your CSS files are in static/css/")
    print("4. Verify media files are being uploaded to S3")

if __name__ == "__main__":
    print_heroku_commands()
    check_aws_bucket()
    check_static_files() 