import os
import shutil

import pytest


@pytest.mark.parametrize("attr", ["config", "data", "cache", "logs"])
@pytest.mark.parametrize("custom", [False, True])
async def test_app_paths(app, app_probe, attr, custom):
    if custom:
        app_probe.apply_path_customization()

    """Platform paths are as expected."""
    path = getattr(app.paths, attr)
    expected_paths = app_probe.paths(custom=custom)
    assert path == expected_paths[attr]

    try:
        # We can create a folder in the app path
        tempdir = path / f"testbed-{os.getpid()}"
        tempdir.mkdir(parents=True)

        # We can create a file in the app path
        tempfile = tempdir / f"{attr}.txt"
        with tempfile.open("w", encoding="utf-8") as f:
            f.write(f"Hello {attr}\n")

        # We can read a file in the app path
        with tempfile.open("r", encoding="utf-8") as f:
            assert f.read() == f"Hello {attr}\n"

    finally:
        if path.exists():
            shutil.rmtree(tempdir)

    if custom:
        app_probe.remove_path_customization()
