#!/usr/bin/env python3
"""
Build script for FileLens
Handles cross-platform building and packaging
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True


def clean_build():
    """Clean build directories."""
    dirs_to_clean = ['build', 'dist', 'node_modules', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Clean Python cache
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                shutil.rmtree(os.path.join(root, dir_name))


def install_dependencies():
    """Install Python and Node dependencies."""
    print("Installing Python dependencies...")
    if not run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt']):
        return False
    
    print("Installing Node dependencies...")
    if not run_command(['npm', 'install']):
        return False
    
    return True


def build_backend():
    """Build Python backend with PyInstaller."""
    print("Building backend...")
    
    # Create spec file for PyInstaller
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src/main.py'],
    pathex=['src'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'chromadb',
        'sentence_transformers',
        'fastapi',
        'uvicorn',
        'pydantic',
        'PyPDF2',
        'docx',
        'pptx',
        'openpyxl',
        'markdown',
        'bs4',
        'jieba',
        'tiktoken',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='filelens-backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open('filelens.spec', 'w') as f:
        f.write(spec_content)
    
    if not run_command(['pyinstaller', 'filelens.spec', '--clean']):
        return False
    
    return True


def build_frontend():
    """Build Electron frontend."""
    print("Building frontend...")
    
    # Copy backend executable to frontend resources
    backend_exe = 'dist/filelens-backend'
    if platform.system() == 'Windows':
        backend_exe += '.exe'
    
    if os.path.exists(backend_exe):
        os.makedirs('frontend/resources', exist_ok=True)
        shutil.copy(backend_exe, 'frontend/resources/')
    
    # Build with electron-builder
    if not run_command(['npm', 'run', 'build:frontend']):
        return False
    
    return True


def main():
    """Main build function."""
    import argparse
    parser = argparse.ArgumentParser(description='Build FileLens')
    parser.add_argument('--clean', action='store_true', help='Clean build directories')
    parser.add_argument('--skip-deps', action='store_true', help='Skip installing dependencies')
    args = parser.parse_args()
    
    if args.clean:
        clean_build()
    
    if not args.skip_deps:
        if not install_dependencies():
            print("Failed to install dependencies")
            sys.exit(1)
    
    # Build backend
    if not build_backend():
        print("Failed to build backend")
        sys.exit(1)
    
    # Build frontend
    if not build_frontend():
        print("Failed to build frontend")
        sys.exit(1)
    
    print("Build completed successfully!")
    print(f"Output directory: {os.path.abspath('dist')}")


if __name__ == '__main__':
    main()
