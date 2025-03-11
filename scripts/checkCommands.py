import subprocess


def check(cmd):
    """Check if a command is available in the system."""
    try:
        subprocess.run([cmd, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False