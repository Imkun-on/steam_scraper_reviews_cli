"""Detect local PC specs and compare with game requirements."""

import subprocess
import platform


def get_pc_specs() -> dict:
    specs = {"cpu": "N/A", "gpu": "N/A", "ram": "N/A", "os": platform.platform()}

    if platform.system() != "Windows":
        return specs

    try:
        result = subprocess.run(
            ["powershell", "-Command", "(Get-CimInstance Win32_Processor).Name"],
            capture_output=True, text=True, timeout=10,
        )
        if result.stdout.strip():
            specs["cpu"] = result.stdout.strip()

        result = subprocess.run(
            ["powershell", "-Command", "(Get-CimInstance Win32_VideoController).Name"],
            capture_output=True, text=True, timeout=10,
        )
        if result.stdout.strip():
            specs["gpu"] = result.stdout.strip().split("\n")[0]

        result = subprocess.run(
            ["powershell", "-Command", "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory"],
            capture_output=True, text=True, timeout=10,
        )
        if result.stdout.strip():
            ram_bytes = int(result.stdout.strip())
            specs["ram"] = f"{ram_bytes / (1024**3):.1f} GB"
    except Exception:
        pass

    return specs
