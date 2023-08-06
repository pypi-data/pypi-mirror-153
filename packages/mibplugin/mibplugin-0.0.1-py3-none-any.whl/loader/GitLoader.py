

import tarfile

import gzip

import requests
import shutil
import tempfile

import os
import io

import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__file__)

from temporaryContainer.TempDir import TempDir



def download_all_mibs_from_artifactory(artifactory_base_url, package_version, temporary_directory_object: TempDir):

    file_contents = requests.get(url=f'{artifactory_base_url}/{package_version}.tar.gz', headers={"Accept" : "application/octet-stream"})
    print("full url %s"%(f'{artifactory_base_url}/{package_version}.tar.gz'))

    temporary_base_dir = temporary_directory_object.get_full_path()
    net_snmp_dir = os.path.join(temporary_base_dir, 'netsnmp')
    os.makedirs(net_snmp_dir, exist_ok=True)
    extract_dir = temporary_base_dir

    file_obj = io.BytesIO(file_contents.content)

    tar_object = tarfile.open(fileobj=file_obj, mode='r:gz')

    tar_object.extractall(path=net_snmp_dir)

def set_up_folder_structure(temporary_directory_object: TempDir, mib_path):
    temporary_base_dir = temporary_directory_object.get_full_path()

    mib_dir = os.path.join(temporary_base_dir, "mib_paths")
    temporary_base_dir = temporary_directory_object.get_full_path()

    net_snmp_dir = os.path.join(temporary_base_dir, 'netsnmp')

    os.makedirs(mib_dir, exist_ok=True)
    uncompiled_mib_dir = os.path.join(mib_dir, 'uncompiled_mibs')
    compiled_mib_dir = os.path.join(mib_dir, 'compiled_mibs')
    os.makedirs(uncompiled_mib_dir, exist_ok=True)
    os.makedirs(compiled_mib_dir, exist_ok=True)
    shutil.rmtree(path=os.path.join(mib_dir, 'mibs'), ignore_errors=True)
    shutil.copytree(os.path.join(net_snmp_dir, os.listdir(net_snmp_dir)[0], 'mibs'), os.path.join(mib_dir, 'mibs'))

    shutil.copy(mib_path, uncompiled_mib_dir)

    full_file_name = mib_path.rsplit(os.path.sep, maxsplit=1)[-1]
    file_name = full_file_name.replace('.mib', '')
    shutil.move(os.path.join(uncompiled_mib_dir, full_file_name), os.path.join(uncompiled_mib_dir, file_name))

if __name__ == '__main__':

    temp_dir_object = TempDir()

    download_all_mibs_from_artifactory(artifactory_base_url='https://github.com/net-snmp/net-snmp/archive/refs/tags', package_version='v5.9.2.rc1',
                                       temporary_directory_object=temp_dir_object)

    print(os.listdir(path=temp_dir_object.get_full_path()))