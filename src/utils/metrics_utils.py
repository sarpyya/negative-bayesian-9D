"""
Metrics utilities for Bayesian Negative 9D.
Handles formatting and exporting performance data.
"""

import json
import csv
from datetime import datetime
from typing import List, Dict

def export_to_json(metrics: List[Dict], filename: str):
    """Exports metrics to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)

def export_to_csv(metrics: List[Dict], filename: str):
    """Exports metrics to a CSV file."""
    if not metrics:
        return
    
    keys = metrics[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(metrics)

def format_benchmark_report(metrics: List[Dict]) -> str:
    """Formats a simple markdown report for performance."""
    if not metrics:
        return "No metrics available."
    
    avg_fps = sum(m.get('fps', 0) for m in metrics) / len(metrics)
    max_memory = max(m.get('memory', 0) for m in metrics)
    
    report = f"## Benchmark Report - {datetime.now().isoformat()}\n"
    report += f"- Average FPS: {avg_fps:.2f}\n"
    report += f"- Max Memory: {max_memory:.2f} MB\n"
    report += f"- Samples: {len(metrics)}\n"
    return report

def track_performance(func):
    """Decorator to track function execution time."""
    import time
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f" [PERF] {func.__name__}: {elapsed*1000:.2f}ms")
        return result
    return wrapper
