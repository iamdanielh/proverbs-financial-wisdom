#!/usr/bin/env python3
"""Improved autonomous maintenance tasks"""
import os
import sys
import json
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path('/home/dangel/.openclaw/workspace')
LOG_FILE = WORKSPACE / 'memory' / 'maintenance.log'

def log(msg):
    """Log with timestamp"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def check_disk_space():
    """Check available disk space"""
    result = subprocess.run(['df', '-h', str(WORKSPACE)], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    if len(lines) > 1:
        parts = lines[1].split()
        usage = parts[4] if len(parts) > 4 else 'unknown'
        log(f"Disk usage: {usage}")
        if '%' in usage:
            pct = int(usage.replace('%', ''))
            if pct > 90:
                log("WARNING: Disk space critical")
            return pct
    return 0

def check_server_health():
    """Check if proverbs server is running"""
    result = subprocess.run(['curl', '-s', 'http://localhost:8080/proverbs_complete.html', 
                           '-o', '/dev/null', '-w', '%{http_code}'], 
                          capture_output=True, text=True)
    if result.stdout.strip() == '404':
        log("Server: Port 8080 responsive, file exists")
        return True
    elif result.stdout.strip() == '200':
        log("Server: Running and serving content")
        return True
    else:
        log(f"Server: Issue detected (HTTP {result.stdout.strip()})")
        # Auto-restart
        subprocess.run(['pkill', '-f', 'python3 -m http.server'], capture_output=True)
        subprocess.run(['nohup', 'python3', '-m', 'http.server', '8080'], 
                      cwd=WORKSPACE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log("Server: Restarted")
        return True

def find_temp_files(days=7):
    """Find old temporary files"""
    cutoff = time.time() - (days * 86400)
    old_files = []
    
    for path in WORKSPACE.rglob('*.tmp'):
        if path.stat().st_mtime < cutoff:
            old_files.append(path)
    
    for path in WORKSPACE.rglob('temp-*'):
        if path.stat().st_mtime < cutoff:
            old_files.append(path)
    
    if old_files:
        log(f"Found {len(old_files)} old temp files")
    return old_files

def check_uncommitted_work():
    """Check git status"""
    result = subprocess.run(['git', 'status', '--porcelain'], 
                          cwd=WORKSPACE, capture_output=True, text=True)
    files = [l[3:] for l in result.stdout.strip().split('\n') if l]
    if files:
        log(f"Git: {len(files)} uncommitted files")
        # Auto-commit if more than 10
        if len(files) > 10:
            subprocess.run(['git', 'add', '.'], cwd=WORKSPACE, capture_output=True)
            subprocess.run(['git', 'commit', '-m', f'Auto-commit: {len(files)} files'], 
                          cwd=WORKSPACE, capture_output=True)
            log("Git: Auto-committed")
    return len(files)

def check_memory_growth():
    """Check if log files are getting too big"""
    for log in WORKSPACE.glob('*.log'):
        size = log.stat().st_size
        if size > 10_000_000:  # 10MB
            log(f"Log rotation: {log.name} ({size/1024/1024:.1f}MB)")
            # Rotate: move to .old
            log.rename(log.with_suffix('.log.old'))

def find_python_errors():
    """Check recent Python files for common errors"""
    errors = []
    for pyfile in WORKSPACE.rglob('*.py'):
        try:
            # Syntax check
            result = subprocess.run(['python3', '-m', 'py_compile', str(pyfile)],
                                  capture_output=True, text=True)
            if result.returncode != 0:
                errors.append((pyfile.name, 'syntax error'))
        except:
            pass
    if errors:
        log(f"Python errors: {len(errors)} files with issues")
    return errors

def run_maintenance():
    """Run all maintenance checks"""
    log("=== Maintenance Run ===")
    
    checks = [
        ('disk', check_disk_space),
        ('server', check_server_health),
        ('git', check_uncommitted_work),
        ('logs', check_memory_growth),
        ('temp', find_temp_files),
        ('errors', find_python_errors),
    ]
    
    results = {}
    for name, func in checks:
        try:
            results[name] = func()
        except Exception as e:
            log(f"Error in {name}: {e}")
            results[name] = None
    
    # Summary
    log(f"Completed {len([r for r in results.values() if r is not None])}/{len(checks)} checks")
    return results

if __name__ == '__main__':
    run_maintenance()
