""" Fetch data from repository, or maybe local cache
"""

import os
from pathlib import Path

import pooch

DATA_VERSION = '0.4'


def get_registry():
    return pooch.create(
        # Use the default cache folder for the operating system
        path=pooch.os_cache("nipraxis"),
        # The remote data is on Github
        base_url="https://raw.githubusercontent.com/nipraxis/nipraxis-data/{version}/",
        version=DATA_VERSION,
        # If this is a development version, get the data from the "main" branch
        version_dev="main",
        registry={
            'ds107_sub012_highres.nii': 'md5:316b0635a4280f65e1ca27ecb34264d6',
            'ds107_sub012_t1r2.nii': 'md5:4546a0a3f7041261b80b56b60cd54126',
            'ds108_sub001_t1r1.nii': '6378302aad7bc006bfb48fa973866e68',
            'ds114_sub009_highres.nii': 'md5:95d1b9542a9adebb87e3948c33af478d',
            'ds114_sub009_highres_brain_222.nii': 'md5:615aad84d5b96085601fe306af614564',
            'ds114_sub009_t2r1.nii': 'md5:709fcca8d33ddb7d0b7d501210c8f51c',
            'mni_icbm152_t1_tal_nlin_asym_09a_masked_222.nii': 'md5:6d0615d6581c9f9e17f6916da480fd2e',
            'camera.txt': 'md5:e596928a61c4332252d4eb1f0b6dab1e',
            'ds114_sub009_highres_moved.hdr': 'md5:b12b3d9db549d68b984ace0b95920603',
            'ds114_sub009_highres_moved.img': 'md5:95d1b9542a9adebb87e3948c33af478d',
            'ds114_sub009_t2r1_cond.txt': 'md5:5cb29aed9c9f330afe1af7e69f8aad18',
            'new_cond.txt': 'md5:b40dc95801267932a9f273f02ac05d1e',
            'ds114_sub009_t2r1_conv.txt':
            'md5:839eadd4533af9d8aef0cf8d623ab139',
            'ds107_sub001_highres.nii': 'md5:fd733636ae8abe8f0ffbfadedd23896c',
            'anatomical.txt': 'md5:3c91c588e2bbf69d7c59c80d32988fb4',
            '24719.f3_beh_CHYM.csv': 'md5:ac1f4df5697bf356b2b060afd383430e',
        },
        # The name of an environment variable that can overwrite the cache path.
        env="NIPRAXIS_LOCAL_CACHE",
    )


NIPRAXIS_REGISTRY = get_registry()


def from_staging_cache(rel_url, staging_cache):
    known_hash = NIPRAXIS_REGISTRY.registry.get(rel_url)
    if not known_hash:
        return None
    pth = Path(staging_cache).resolve() / DATA_VERSION / rel_url
    action, verb = pooch.core.download_action(pth, known_hash)
    if action == 'update':
        pooch.utils.get_logger().info(
            f"'{rel_url}' in '{staging_cache}/{DATA_VERSION}' "
            "but hash does not match; looking in local cache / registry.")
        return None
    if action == 'fetch':
        return str(pth)


def fetch_file(rel_url):
    """ Fetch data file from local cache, or registry
    """
    staging_cache = os.environ.get('NIPRAXIS_STAGING_CACHE')
    if staging_cache:
        cache_fname = from_staging_cache(rel_url, staging_cache)
        if cache_fname:
            return cache_fname
    return NIPRAXIS_REGISTRY.fetch(rel_url)
