#!/usr/bin/env python3
"""
Test ZenML Connection - Kiểm tra kết nối ZenML mà không chạy pipeline

Chạy script này:
cd learning-code && poetry run python test_zenml_connection.py
"""

import json
import sys
from datetime import datetime


def test_basic_imports():
    """Test basic Python imports"""
    print("🔍 Testing basic Python imports...")
    
    try:
        import datetime
        import json
        import random
        print("✅ Basic Python modules: OK")
        return True
    except Exception as e:
        print(f"❌ Basic imports failed: {e}")
        return False

def test_zenml_import():
    """Test ZenML import without triggering integrations"""
    print("🔍 Testing ZenML import...")
    
    try:
        # Test basic import first
        from zenml.client import Client
        print("✅ ZenML Client import: OK")
        
        # Test creating client
        client = Client()
        print("✅ ZenML Client creation: OK")
        
        return True, client
    except Exception as e:
        print(f"❌ ZenML import failed: {e}")
        return False, None

def test_zenml_server_connection(client):
    """Test connection to ZenML server"""
    print("🔍 Testing ZenML server connection...")
    
    try:
        # Get server info
        server_info = client.zen_store.get_store_info()
        print(f"✅ Server connection: OK")
        print(f"📊 Server type: {server_info.type}")
        print(f"📊 Server URL: {getattr(server_info, 'url', 'Local')}")
        return True, server_info
    except Exception as e:
        print(f"❌ Server connection failed: {e}")
        return False, None

def test_stacks(client):
    """Test listing stacks"""
    print("🔍 Testing stack access...")
    
    try:
        stacks = client.list_stacks()
        print(f"✅ Stack access: OK")
        print(f"📊 Available stacks: {len(stacks)}")
        
        if stacks:
            active_stack = client.active_stack
            print(f"📊 Active stack: {active_stack.name}")
        
        return True
    except Exception as e:
        print(f"❌ Stack access failed: {e}")
        return False

def test_artifacts(client):
    """Test listing artifacts"""
    print("🔍 Testing artifact access...")
    
    try:
        artifacts = client.list_artifacts(size=5)  # Only get first 5
        print(f"✅ Artifact access: OK")
        print(f"📊 Recent artifacts: {len(artifacts)}")
        return True
    except Exception as e:
        print(f"❌ Artifact access failed: {e}")
        return False

def test_pipelines(client):
    """Test listing pipelines"""
    print("🔍 Testing pipeline access...")
    
    try:
        pipelines = client.list_pipelines(size=5)  # Only get first 5
        print(f"✅ Pipeline access: OK") 
        print(f"📊 Recent pipelines: {len(pipelines)}")
        return True
    except Exception as e:
        print(f"❌ Pipeline access failed: {e}")
        return False

def test_ctypes_issue():
    """Test if _ctypes issue exists"""
    print("🔍 Testing for _ctypes issue...")
    
    try:
        import ctypes
        print("✅ ctypes module: OK")
        return True
    except ModuleNotFoundError as e:
        if "_ctypes" in str(e):
            print("❌ _ctypes module missing - this is the root cause!")
            print("💡 Solution needed: reinstall Python with libffi support")
            return False
        else:
            print(f"❌ Other ctypes issue: {e}")
            return False

def test_pandas_availability():
    """Test pandas availability"""
    print("🔍 Testing pandas availability...")
    
    try:
        import pandas as pd
        print(f"✅ pandas available: {pd.__version__}")
        return True
    except Exception as e:
        print(f"❌ pandas not available: {e}")
        return False

def generate_report(results):
    """Generate test report"""
    print("\n" + "="*60)
    print("📋 ZenML CONNECTION TEST REPORT")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r)
    
    print(f"📊 Tests passed: {passed_tests}/{total_tests}")
    print(f"📊 Success rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\n🔍 Detailed Results:")
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    # Recommendations
    print("\n💡 Recommendations:")
    
    if not results.get('ctypes_test', True):
        print("  🚨 CRITICAL: _ctypes module missing")
        print("     Solution: Reinstall Python with libffi support")
        print("     Commands:")
        print("       sudo apt install -y libffi-dev libssl-dev")
        print("       pyenv install 3.11.8 --force")
        print("       poetry env remove --all && poetry install")
    
    if not results.get('pandas_test', True):
        print("  ⚠️  pandas unavailable due to _ctypes issue")
    
    if results.get('zenml_import', True) and results.get('server_connection', True):
        print("  ✅ ZenML basic functionality works")
        print("  💡 You can use ZenML CLI and Dashboard")
        print("  🌐 Dashboard: http://127.0.0.1:8237/")
    
    if all([results.get('zenml_import', True), results.get('server_connection', True), 
            results.get('stacks_test', True)]):
        print("  🎯 ZenML infrastructure is healthy")
        print("  📝 You can create simple pipelines (avoiding pandas)")

def main():
    """Main test function"""
    print("🚀 ZenML Connection Test Started")
    print("=" * 60)
    print(f"📅 Test time: {datetime.now().isoformat()}")
    print(f"🐍 Python version: {sys.version}")
    print(f"📍 Working directory: {sys.path[0]}")
    print()
    
    results = {}
    
    # Test 1: Basic imports
    results['basic_imports'] = test_basic_imports()
    print()
    
    # Test 2: _ctypes issue
    results['ctypes_test'] = test_ctypes_issue()
    print()
    
    # Test 3: pandas availability  
    results['pandas_test'] = test_pandas_availability()
    print()
    
    # Test 4: ZenML import
    zenml_import_ok, client = test_zenml_import()
    results['zenml_import'] = zenml_import_ok
    print()
    
    if not zenml_import_ok:
        print("❌ Cannot proceed with ZenML tests - import failed")
        generate_report(results)
        return
    
    # Test 5: Server connection
    server_ok, server_info = test_zenml_server_connection(client)
    results['server_connection'] = server_ok
    print()
    
    if not server_ok:
        print("❌ Cannot proceed with advanced tests - server connection failed")
        generate_report(results)
        return
    
    # Test 6: Stacks
    results['stacks_test'] = test_stacks(client)
    print()
    
    # Test 7: Artifacts
    results['artifacts_test'] = test_artifacts(client)
    print()
    
    # Test 8: Pipelines
    results['pipelines_test'] = test_pipelines(client)
    print()
    
    # Generate final report
    generate_report(results)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        import traceback
        print(f"🚨 Full traceback:\n{traceback.format_exc()}") 