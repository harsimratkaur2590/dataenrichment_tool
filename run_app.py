#!/usr/bin/env python3
"""
Quick launcher for Apollo Data Enrichment Tool
"""
import subprocess
import sys
import os

def main():
    """Launch the Apollo Data Enrichment Tool"""
    print("🚀 Starting Apollo Data Enrichment Tool...")
    print("=" * 50)
    
    # Check if the main app file exists
    if not os.path.exists("apollo_enrichment_app.py"):
        print("❌ Error: apollo_enrichment_app.py not found!")
        print("Make sure you're in the correct directory.")
        return False
    
    try:
        # Run the main application
        subprocess.run([sys.executable, "apollo_enrichment_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
