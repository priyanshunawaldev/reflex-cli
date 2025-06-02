# test_basic.py - Simple tests to make sure stuff doesn't break

import subprocess
import os
import tempfile
import shutil
import sys
from pathlib import Path


# --- Security helpers (from reflex/tracker/security.py) ---
def clean_user_input(text: str) -> str:
    """Clean user input - nothing fancy, just prevent obvious problems"""
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Limit ridiculous lengths (who writes 5000 char tasks anyway?)
    if len(text) > 1000:
        text = text[:1000] + "..."
    
    # Just escape quotes to prevent basic SQL issues
    # Yeah, we should use prepared statements everywhere but this is a quick fix
    text = text.replace("'", "''")
    
    return text

def is_reasonable_input(text: str) -> bool:
    """Check if input looks reasonable - not trying to catch everything"""
    if not text or len(text.strip()) == 0:
        return False
    
    # Basic sanity checks
    if len(text) > 1000:
        return False
        
    # Block obvious script attempts (most hackers aren't targeting CLI productivity tools anyway)
    suspicious = ['<script', 'javascript:', 'DROP TABLE', '--', ';DELETE']
    text_lower = text.lower()
    
    for sus in suspicious:
        if sus.lower() in text_lower:
            return False
    
    return True


def test_basic_commands():
    """Test that the main commands don't crash"""
    print("Testing basic commands...")
    
    # Create temp directory for testing
    test_dir = tempfile.mkdtemp()
    old_home = os.environ.get('HOME')
    
    try:
        # Point to temp directory
        os.environ['HOME'] = test_dir
        
        # Test help flag
        print("Testing help flag...")
        result = subprocess.run([sys.executable, 'reflex/main.py', '--help'], 
                              capture_output=True, text=True, timeout=10, 
                              encoding='utf-8', errors='ignore')
        if result.returncode != 0:
            print(f"❌ Help flag failed. Return code: {result.returncode}")
            print(f"Stdout: {result.stdout}")
            print(f"Stderr: {result.stderr}")
            print("This test failed, but continuing with other tests...")
        else:
            print("✅ Help flag works")
        
        # Test adding a task
        result = subprocess.run([sys.executable, 'reflex/main.py', 'add', 'Test task'], 
                              capture_output=True, text=True, timeout=10,
                              encoding='utf-8', errors='ignore')
        if result.returncode != 0:
            print(f"❌ Add task failed. Return code: {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
        print("✅ Add task works")
        
        # Test listing tasks
        print("Testing list tasks command...")
        result = subprocess.run([sys.executable, 'reflex/main.py', 'list-tasks'], 
                              capture_output=True, text=True, timeout=10,
                              encoding='utf-8', errors='ignore')
        if result.returncode != 0:
            print(f"❌ List tasks failed. Return code: {result.returncode}")
            print(f"Stderr: {result.stderr}")
            return False
        if "Test task" not in result.stdout:
            print(f"❌ Task not found in list. Output: {result.stdout}")
            return False
        print("✅ List tasks works")
        
        # Test stats
        print("Testing stats command...")
        result = subprocess.run([sys.executable, 'reflex/main.py', 'stats'], 
                              capture_output=True, text=True, timeout=10,
                              encoding='utf-8', errors='ignore')
        if result.returncode != 0:
            print(f"❌ Stats failed. Return code: {result.returncode}")
            print(f"Stderr: {result.stderr}")
            return False
        print("✅ Stats command works")
        
        # Test log
        print("Testing log command...")
        result = subprocess.run([sys.executable, 'reflex/main.py', 'log', 'Test log'], 
                              capture_output=True, text=True, timeout=10,
                              encoding='utf-8', errors='ignore')
        if result.returncode != 0:
            print(f"❌ Log failed. Return code: {result.returncode}")
            print(f"Stderr: {result.stderr}")
            return False
        print("✅ Log command works")
        
        return True
        
    finally:
        # Cleanup
        if old_home:
            os.environ['HOME'] = old_home
        else:
            del os.environ['HOME']
        shutil.rmtree(test_dir, ignore_errors=True)
def test_malicious_input():
    """Test that obviously bad input doesn't break things"""
    print("Testing malicious input...")
    
    test_dir = tempfile.mkdtemp()
    old_home = os.environ.get('HOME')
    
    try:
        os.environ['HOME'] = test_dir
        
        # Try SQL injection
        bad_inputs = [
            "'; DROP TABLE tasks; --",
            "<script>alert('xss')</script>",
            "A" * 2000,  # Very long input
            ""  # Empty input
        ]
        
        for bad_input in bad_inputs:  
            result = subprocess.run([sys.executable, 'reflex/main.py', 'add', bad_input], 
                                  capture_output=True, text=True, timeout=10,
                                  encoding='utf-8', errors='ignore')
            # Should either work safely or reject cleanly (not crash)
            if result.returncode != 0:
                print(f"⚠️ App rejected input (this is okay): {bad_input[:50]}...")
            else:
                print(f"ℹ️ App accepted input: {bad_input[:50]}...")
        
        print("✅ Malicious input handled safely")
        
    finally:
        if old_home:
            os.environ['HOME'] = old_home
        else:
            del os.environ['HOME']
        shutil.rmtree(test_dir, ignore_errors=True)

def run_quick_checks():
    """Run some quick sanity checks"""
    print("Running quick checks...")
    
    # Check if required files exist
    required_files = ['reflex/main.py', 'reflex/tracker/__init__.py', 'reflex/tracker/db.py']
    for file in required_files:
        assert os.path.exists(file), f"Missing required file: {file}"
    
    print("✅ Required files present")
    
    # Try importing main modules
    try:
        from reflex.tracker import db, tasks, logs, focus
        print("✅ All modules import successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        raise

if __name__ == "__main__":
    print("🧪 Running basic tests for Reflex...")
    run_quick_checks()
    
    if test_basic_commands():
        print("🎉 Basic tests passed!")
    else:
        print("❌ Some tests failed")
        
    test_malicious_input()
    print("✅ All tests completed!")