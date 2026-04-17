import shutil

from paths import BASE_DIR, STARTUP_BAT_LEGACY, STARTUP_VBS


def run() -> bool:
    removed = False
    for target in (STARTUP_VBS, STARTUP_BAT_LEGACY):
        if target.exists():
            try:
                target.unlink()
                removed = True
            except OSError:
                pass
    if BASE_DIR.exists():
        before = BASE_DIR.exists()
        shutil.rmtree(BASE_DIR, ignore_errors=True)
        if before and not BASE_DIR.exists():
            removed = True
    return removed
