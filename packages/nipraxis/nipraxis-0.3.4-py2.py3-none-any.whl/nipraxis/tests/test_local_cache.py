""" Test local cache
"""
import shutil
from hashlib import sha1

from nipraxis import fetch_file
import nipraxis._fetcher as nipf

CAMERA_HASH = 'af7257977f30797d4b3ea7dd15fa362d4fe8c37e'


def assert_hash(fname, hash):
    with open(fname, 'rb') as fobj:
        contents = fobj.read()
    assert sha1(contents).hexdigest() == hash


def test_camera(tmp_path, monkeypatch):
    local_cache = tmp_path / 'nipraxis-local'
    staging_cache = tmp_path / 'nipraxis-staging'
    monkeypatch.delenv("NIPRAXIS_STAGING_CACHE", raising=False)
    monkeypatch.setenv("NIPRAXIS_LOCAL_CACHE", str(local_cache))
    monkeypatch.setattr('nipraxis._fetcher.NIPRAXIS_REGISTRY',  nipf.get_registry())
    fname = fetch_file('camera.txt')
    assert fname.startswith(str(local_cache))
    monkeypatch.setenv("NIPRAXIS_STAGING_CACHE", str(staging_cache))
    fname = fetch_file('camera.txt')
    assert fname.startswith(str(local_cache))
    shutil.move(local_cache, staging_cache)
    fname = fetch_file('camera.txt')
    assert fname.startswith(str(staging_cache))
