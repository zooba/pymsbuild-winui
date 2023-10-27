import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).absolute().parent.parent
sys.path.insert(0, str(ROOT))
TESTDATA = ROOT / "tests" / "testdata"

import packaging
import pymsbuild
PYTHONPATH = os.pathsep.join(str(s) for s in [
    ROOT,
    pathlib.Path(packaging.__spec__.origin).parent.parent,
    pathlib.Path(pymsbuild.__spec__.origin).parent.parent,
])


def run(*cmd, cwd=None, env=None):
    env = {
        **os.environ,
        "PYTHONPATH": PYTHONPATH,
        **(env or {}),
    }
    subprocess.check_call(
        cmd,
        cwd=cwd,
        env=env,
    )


def test_build_app1(tmp_path):
    run(sys.executable, "-m", "venv", tmp_path, "--system-site-packages", "--without-pip")
    env_exe = tmp_path / "Scripts" / "python.exe"
    run(env_exe, "-m", "pymsbuild", cwd=TESTDATA / "app1")


def test_build_BasicPhotoViewer(tmp_path):
    run(sys.executable, "-m", "venv", tmp_path, "--system-site-packages", "--without-pip")
    env_exe = tmp_path / "Scripts" / "python.exe"
    run(env_exe, "-m", "pymsbuild", cwd=TESTDATA / "BasicPhotoViewer")
