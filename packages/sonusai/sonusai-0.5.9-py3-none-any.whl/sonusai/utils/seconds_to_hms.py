def seconds_to_hms(seconds: float) -> str:
    """Convert given seconds into string of H:MM:SS"""
    h = int(seconds / 3600)
    s = seconds - h * 3600
    m = int(s / 60)
    s = int(seconds - h * 3600 - m * 60)
    return f'{h:d}:{m:02d}:{s:02d} (H:MM:SS)'
