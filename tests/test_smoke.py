import importlib
import os
import pkgutil
import subprocess
import sys
from pathlib import Path

import usolspace


def test_all_modules_importable():
    package_path = Path(usolspace.__file__).parent
    failures = []
    for module in pkgutil.iter_modules([str(package_path)]):
        if module.name.startswith("_"):
            continue
        name = f"usolspace.{module.name}"
        try:
            importlib.import_module(name)
        except Exception as exc:  # pragma: no cover - assertion reports exact module
            failures.append(f"{name}: {exc!r}")
    assert failures == []


def test_volume_script_compiles_and_helps():
    script = Path("scripts/generate_volume_plate.py")
    subprocess.run([sys.executable, "-m", "py_compile", str(script)], check=True)

    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = "src" if not existing else f"src{os.pathsep}{existing}"
    result = subprocess.run(
        [sys.executable, str(script), "--help"],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    assert "Per-volume pipeline runner" in result.stdout
    assert "--volume" in result.stdout
