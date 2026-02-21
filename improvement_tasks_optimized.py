#!/usr/bin/env python3
"""Autonomous improvement tasks - optimized version with error handling and new checks"""

import os
import json
import subprocess
import asyncio
import logging
import psutil
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

# Configuration
WORKSPACE = Path('/home/dangel/.openclaw/workspace')
MEMORY_DIR = WORKSPACE / 'memory'
LARGE_FILE_THRESHOLD = 10_000_000  # 10MB
OLD_FILE_DAYS = 30
DISK_USAGE_WARN = 80  # percent
DISK_USAGE_CRITICAL = 90
TIMEOUT_SECONDS = 30

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def handle_errors(func):
    """Decorator to add error handling to functions"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {type(e).__name__}: {e}")
            return None
    return wrapper


@dataclass
class ImprovementResult:
    """Structured result container"""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    actions: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    def add_action(self, msg: str):
        self.actions.append(msg)
        logger.info(msg)
    
    def add_warning(self, msg: str):
        self.warnings.append(msg)
        logger.warning(msg)
    
    def add_error(self, msg: str):
        self.errors.append(msg)
        logger.error(msg)
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp,
            'actions': self.actions,
            'warnings': self.warnings,
            'errors': self.errors,
            'metrics': self.metrics
        }


async def run_command_async(cmd: List[str], timeout: int = TIMEOUT_SECONDS) -> Tuple[int, str, str]:
    """Run a command async with timeout"""
    try:
        proc = await asyncio.wait_for(
            asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
            timeout=timeout
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        return proc.returncode, stdout.decode().strip(), stderr.decode().strip()
    except asyncio.TimeoutError:
        logger.error(f"Command '{' '.join(cmd)}' timed out after {timeout}s")
        return -1, "", "Timeout"
    except Exception as e:
        logger.error(f"Command failed: {e}")
        return -1, "", str(e)


@handle_errors
def check_uncommitted_work() -> Tuple[List[str], List[str]]:
    """Check git status with error handling"""
    files = []
    errors = []
    
    try:
        original_dir = os.getcwd()
        os.chdir(WORKSPACE)
        
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )
        
        os.chdir(original_dir)
        
        if result.returncode != 0:
            errors.append(f"Git status failed: {result.stderr}")
            return files, errors
        
        if result.stdout.strip():
            files = [line[3:] for line in result.stdout.strip().split('\n') if line]
            logger.info(f"Found {len(files)} uncommitted files")
            
    except subprocess.TimeoutExpired:
        errors.append("Git status timed out")
    except FileNotFoundError:
        errors.append("Git command not found")
    except Exception as e:
        errors.append(f"Git check error: {e}")
    
    return files, errors


def check_file_optimized(path: Path, threshold: int) -> Optional[Tuple[Path, int]]:
    """Optimized file size check for thread pool"""
    try:
        size = path.stat().st_size
        if size > threshold:
            return (path, size)
    except (OSError, PermissionError):
        pass
    return None


@handle_errors
def find_optimization_opportunities_parallel() -> Tuple[List[Tuple[Path, int]], List[str]]:
    """Find large files using parallel processing"""
    large_files = []
    errors = []
    
    files_to_check = []
    for f in WORKSPACE.rglob('*'):
        if f.is_file() and '.git' not in f.parts and 'node_modules' not in f.parts:
            files_to_check.append(f)
    
    # Use ThreadPoolExecutor for parallel stat calls
    with ThreadPoolExecutor(max_workers=min(32, os.cpu_count() + 4)) as executor:
        futures = [
            executor.submit(check_file_optimized, f, LARGE_FILE_THRESHOLD)
            for f in files_to_check
        ]
        
        for future in as_completed(futures):
            try:
                result = future.result(timeout=5)
                if result:
                    large_files.append(result)
            except Exception as e:
                errors.append(f"File check error: {e}")
    
    # Sort by size descending
    large_files.sort(key=lambda x: x[1], reverse=True)
    return large_files[:100], errors  # Limit to top 100


@handle_errors
def check_old_files_optimized(days: int = OLD_FILE_DAYS) -> Tuple[List[Path], List[str]]:
    """Find old files with generator-based iteration"""
    old_files = []
    errors = []
    cutoff = datetime.now() - timedelta(days=days)
    extensions = {'.py', '.js', '.json', '.md', '.txt'}
    
    skip_paths = {'.git', 'node_modules', '__pycache__', '.pytest_cache'}
    
    try:
        for f in WORKSPACE.rglob('*'):
            if f.is_file() and f.suffix in extensions:
                # Skip if in excluded paths
                if any(skip in f.parts for skip in skip_paths):
                    continue
                
                try:
                    mtime = datetime.fromtimestamp(f.stat().st_mtime)
                    if mtime < cutoff:
                        old_files.append(f)
                except (OSError, PermissionError) as e:
                    errors.append(f"Cannot access {f}: {e}")
                    
    except Exception as e:
        errors.append(f"Directory scan error: {e}")
    
    return old_files[:500], errors  # Limit to 500 files


@handle_errors
def check_dead_processes() -> Tuple[List[Dict], List[str]]:
    """NEW: Detect dead/zombie processes"""
    dead_processes = []
    errors = []
    
    try:
        # Check for zombie processes
        zombie_count = 0
        for proc in psutil.process_iter(['pid', 'name', 'status', 'create_time']):
            try:
                if proc.info['status'] == psutil.STATUS_ZOMBIE:
                    zombie_count += 1
                    dead_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'status': 'zombie',
                        'age': str(datetime.now() - datetime.fromtimestamp(proc.info['create_time']))
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
            except Exception as e:
                errors.append(f"Process check error: {e}")
        
        if zombie_count == 0:
            logger.info("No zombie processes found")
            
    except Exception as e:
        errors.append(f"Dead process check failed: {e}")
    
    return dead_processes, errors


@handle_errors
def check_disk_space() -> Tuple[List[Dict], List[str]]:
    """NEW: Monitor disk space on all mounted filesystems"""
    warnings = []
    errors = []
    
    try:
        partitions = psutil.disk_partitions(all=False)
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                percent_used = usage.percent
                
                info = {
                    'mountpoint': partition.mountpoint,
                    'device': partition.device,
                    'fstype': partition.fstype,
                    'total_gb': round(usage.total / (1024**3), 2),
                    'used_gb': round(usage.used / (1024**3), 2),
                    'free_gb': round(usage.free / (1024**3), 2),
                    'percent_used': percent_used
                }
                
                if percent_used >= DISK_USAGE_CRITICAL:
                    warnings.append({
                        'severity': 'CRITICAL',
                        'mountpoint': partition.mountpoint,
                        'percent': percent_used,
                        'message': f"CRITICAL: {partition.mountpoint} is {percent_used}% full!"
                    })
                elif percent_used >= DISK_USAGE_WARN:
                    warnings.append({
                        'severity': 'WARNING',
                        'mountpoint': partition.mountpoint,
                        'percent': percent_used,
                        'message': f"WARNING: {partition.mountpoint} is {percent_used}% full"
                    })
                else:
                    logger.info(f"Disk {partition.mountpoint}: {percent_used}% used ({info['free_gb']}GB free)")
                    
            except PermissionError:
                errors.append(f"Permission denied checking {partition.mountpoint}")
            except Exception as e:
                errors.append(f"Disk check error for {partition.mountpoint}: {e}")
                
    except Exception as e:
        errors.append(f"Disk space check failed: {e}")
    
    return warnings, errors


@handle_errors
def check_temperature_and_fans() -> Tuple[Dict, List[str]]:
    """NEW: Check CPU temperature and fan status"""
    results = {'temperature': {}, 'fans': {}, 'thermal_zone': []}
    errors = []
    
    try:
        # Check temperature sensors
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                results['temperature'][name] = []
                for entry in entries:
                    temp_data = {
                        'label': entry.label or name,
                        'current': entry.current,
                        'high': entry.high,
                        'critical': entry.critical
                    }
                    results['temperature'][name].append(temp_data)
                    
                    # Log warnings for high temps
                    if entry.critical and entry.current >= entry.critical:
                        logger.warning(f"CRITICAL TEMP: {entry.label}: {entry.current}°C")
                    elif entry.high and entry.current >= entry.high:
                        logger.warning(f"HIGH TEMP: {entry.label}: {entry.current}°C")
        else:
            errors.append("No temperature sensors available")
        
        # Check fan speeds
        fans = psutil.sensors_fans()
        if fans:
            for name, entries in fans.items():
                results['fans'][name] = []
                for entry in entries:
                    fan_data = {
                        'label': entry.label,
                        'rpm': entry.current
                    }
                    results['fans'][name].append(fan_data)
        else:
            logger.info("No fan sensors available")
            
    except Exception as e:
        errors.append(f"Temperature/fan check failed: {e}")
    
    return results, errors


def research_new_skill() -> Dict:
    """Research new tools/skills"""
    skills_to_research = [
        {"name": "jq", "desc": "JSON processing and querying", "priority": "high"},
        {"name": "fzf", "desc": "Fuzzy finding for files and history", "priority": "medium"},
        {"name": "ripgrep", "desc": "Fast searching with patterns", "priority": "high"},
        {"name": "bat", "desc": "Syntax-highlighted cat replacement", "priority": "low"},
        {"name": "fd", "desc": "Fast file finder alternative to find", "priority": "medium"},
        {"name": "eza", "desc": "Modern ls replacement with icons", "priority": "low"},
        {"name": "dust", "desc": "Disk usage analyzer with visualization", "priority": "medium"}
    ]
    
    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    skills_to_research.sort(key=lambda x: priority_order.get(x['priority'], 3))
    
    return skills_to_research[0] if skills_to_research else {}


async def run_checks_concurrent(result: ImprovementResult) -> None:
    """Run independent checks concurrently using asyncio"""
    
    @handle_errors
    async def wrapped_git_check():
        files, errors = check_uncommitted_work()
        if files:
            result.add_action(f"Found {len(files)} uncommitted files")
        for err in errors:
            result.add_error(err)
        return files
    
    @handle_errors
    async def wrapped_opt_check():
        large, errors = find_optimization_opportunities_parallel()
        if large:
            result.add_action(f"Found {len(large)} large files that could be optimized")
            total_size = sum(f[1] for f in large)
            result.metrics['large_files_bytes'] = total_size
            result.metrics['large_files_count'] = len(large)
        for err in errors:
            result.add_error(err)
        return large
    
    @handle_errors
    async def wrapped_old_check():
        old, errors = check_old_files_optimized()
        if old:
            result.add_action(f"Found {len(old)} files older than {OLD_FILE_DAYS} days")
            result.metrics['old_files_count'] = len(old)
        for err in errors:
            result.add_error(err)
        return old
    
    @handle_errors
    async def wrapped_dead_check():
        dead, errors = check_dead_processes()
        if dead:
            result.add_warning(f"Found {len(dead)} zombie/dead processes")
            result.metrics['zombie_processes'] = dead
        for err in errors:
            result.add_error(err)
        return dead
    
    @handle_errors
    async def wrapped_disk_check():
        disk_warnings, errors = check_disk_space()
        for warning in disk_warnings:
            result.add_warning(warning['message'])
        for err in errors:
            result.add_error(err)
        return disk_warnings
    
    @handle_errors
    async def wrapped_temp_check():
        temps, errors = check_temperature_and_fans()
        if temps.get('temperature'):
            result.metrics['temperature'] = temps['temperature']
        if temps.get('fans'):
            result.metrics['fans'] = temps['fans']
        for err in errors:
            result.add_error(err)
        return temps
    
    # Run all checks concurrently
    await asyncio.gather(
        wrapped_git_check(),
        wrapped_opt_check(),
        wrapped_old_check(),
        wrapped_dead_check(),
        wrapped_disk_check(),
        wrapped_temp_check(),
        return_exceptions=True
    )


def run_improvement() -> Dict:
    """Main improvement routine - optimized"""
