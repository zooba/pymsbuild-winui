import argparse
import functools
import io
import json
import os
import pathlib
import re
import shutil
import sys
import zipfile
from urllib.request import urlopen

parser = argparse.ArgumentParser()
parser.add_argument("-o", metavar="PATH", type=pathlib.Path, default=".", required=False, help="Output directory")
parser.add_argument("--verbose", action="store_true", help="Display non-failure messages")
parser.add_argument("--force", action="store_true", help="Always redownload files")
args = parser.parse_args()

PACKAGES = [
    ("Microsoft.Windows.CppWinRT", "2.0"),
    ("Microsoft.WindowsAppSDK", "1.4"),
    ("Microsoft.Windows.SDK.BuildTools", "10.0"),
    ("Microsoft.Windows.ImplementationLibrary", "1.0"),
]

@functools.lru_cache
def nuget_service():
    url = os.getenv("PYMSBUILD_NUGET_FEED") or "https://api.nuget.org/v3/index.json"

    with urlopen(url) as u:
        service = [s for s in json.load(u).get('resources', ())
                   if s.get('@type') == 'PackageBaseAddress/3.0.0']

    if not service:
        raise Exception("ERROR: Specified feed does not appear to be a Nuget feed")
    return service[0]["@id"]

def get_package_url(package, version):
    url = f"{nuget_service()}{package.lower()}/index.json"
    with urlopen(url) as u:
        versions = [v for v in json.load(u).get('versions', ()) if '-' not in v]

    if version not in versions:
        releases = [v for v in versions if v.startswith(f"{version}.")]
        if not releases:
            raise Exception("ERROR: No versions found from " + str(versions))
        version = max(releases, key=lambda v: tuple(map(int, v.split('.'))))

    return f"{nuget_service()}{package.lower()}/{version.lower()}/{package.lower()}.{version.lower()}.nupkg"

def read_package(url):
    buffer = io.BytesIO()
    with urlopen(url) as r:
        buffer.write(r.read())
    buffer.seek(0)
    with zipfile.ZipFile(buffer, "r") as zf:
        for n in zf.namelist():
            if ".." in n:
                continue
            yield n, zf.read(n)


for p, v in PACKAGES:
    dest = args.o / p
    if dest.is_dir():
        if args.force:
            shutil.rmtree(dest)
        else:
            if args.verbose:
                print("[pymsbuild-winui] Found", p, "at", dest, "- skipping download")
            continue
    url = get_package_url(p, v)
    if args.verbose:
        print("[pymsbuild-winui] Downloading", p, "from", url)
    for name, contents in read_package(url):
        d = dest / name
        d.parent.mkdir(parents=True, exist_ok=True)
        with open(d, "wb") as f:
            f.write(contents)
