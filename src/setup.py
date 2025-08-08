#!/usr/bin/env python3
"""
Setup script for Real Estate Investment Analysis Tool
====================================================

This script helps with installation and initial setup.
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("   This tool requires Python 3.8 or higher")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True

def install_dependencies():
    """Install required dependencies"""
    print("\nInstalling dependencies...")
    
    try:
        # Check if pip is available
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ pip not found. Please install pip first.")
        return False
    
    try:
        # Install dependencies from requirements.txt
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_output_directory():
    """Create output directory"""
    print("\nSetting up output directory...")
    
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✅ Created output directory: {output_dir}")
    else:
        print(f"✅ Output directory already exists: {output_dir}")
    
    return True

def create_env_file():
    """Create .env file template"""
    print("\nCreating .env file template...")
    
    env_content = """# Real Estate Investment Analysis Tool - Environment Variables
# Copy this file to .env and add your API keys (optional)

# API Keys (optional - tool works without them)
# Get free API keys from:
# - RapidAPI: https://rapidapi.com/
# - Realtor.com API: https://rapidapi.com/realtor/api/realtor
# - Zillow API: https://rapidapi.com/zillow/api/zillow56

RAPIDAPI_KEY=your_rapidapi_key_here
REALTOR_API_KEY=your_realtor_api_key_here
ZILLOW_API_KEY=your_zillow_api_key_here
OPENCAGE_API_KEY=your_opencage_api_key_here

# Note: The tool will work without API keys, but with limited data sources
"""
    
    env_file = ".env"
    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ Created {env_file} template")
        print("   Edit this file to add your API keys (optional)")
    else:
        print(f"✅ {env_file} already exists")
    
    return True

def run_tests():
    """Run installation tests"""
    print("\nRunning installation tests...")
    
    try:
        result = subprocess.run([sys.executable, "src/test_installation.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def show_next_steps():
    """Show next steps after installation"""
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    
    print("\n🎉 Real Estate Investment Analysis Tool is ready to use!")
    
    print("\n📋 Quick Start Guide:")
    print("1. Test the installation:")
    print("   python test_installation.py")
    
    print("\n2. Run a sample analysis:")
    print("   python run_example.py")
    
    print("\n3. Analyze real properties:")
    print("   python main.py --locations \"Dallas, TX\" \"Austin, TX\" --target-count 100")
    
    print("\n4. Launch the web dashboard:")
    print("   python dashboard.py")
    
    print("\n📚 Documentation:")
    print("   - README.md: Complete documentation")
    print("   - config.py: Configuration settings")
    print("   - main.py --help: Command line options")
    
    print("\n🔧 Configuration:")
    print("   - Edit config.py to adjust financial assumptions")
    print("   - Edit .env to add API keys (optional)")
    
    print("\n📊 Output Files:")
    print("   - Excel files: output/property_analysis_*.xlsx")
    print("   - CSV files: output/property_analysis_*.csv")
    print("   - Reports: output/analysis_report_*.txt")
    
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("Real Estate Investment Analysis Tool - Setup")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        return 1
    
    # Create output directory
    if not create_output_directory():
        return 1
    
    # Create .env file
    if not create_env_file():
        return 1
    
    # Run tests
    if not run_tests():
        print("\n⚠️  Some tests failed, but setup can continue.")
        print("   You may need to install additional system dependencies.")
    
    # Show next steps
    show_next_steps()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
