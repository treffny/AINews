#!/usr/bin/env python3
"""
Test script to verify dual email functionality
"""

import sys
import os
from datetime import datetime

# Add the current directory to the path so we can import from the main script
sys.path.append(os.getcwd())

# Import the email function from the main script
from generate_and_push_report import send_email_newsletter

def test_dual_email():
    """Test sending email to both recipients"""
    
    # Test content
    test_content = """# Daily AI News Report

## Date: July 12, 2025

### General AI News

1. **Test News Item** - This is a test news item to verify email functionality. (Source: Test) [Ref1]

## References

[Ref1] https://example.com/test
"""
    
    # Test with both email addresses
    recipient_emails = [
        "raphael.treffny@teleplanforsberg.com",
        "raphael.treffny@gmail.com"
    ]
    
    print("Testing dual email functionality...")
    print("=" * 50)
    
    # Test the email function
    result = send_email_newsletter(test_content, recipient_emails)
    
    print("=" * 50)
    if result:
        print("✅ Email test completed successfully!")
        print(f"✅ Emails would be sent to: {', '.join(recipient_emails)}")
    else:
        print("❌ Email test failed!")
    
    return result

if __name__ == "__main__":
    test_dual_email()

