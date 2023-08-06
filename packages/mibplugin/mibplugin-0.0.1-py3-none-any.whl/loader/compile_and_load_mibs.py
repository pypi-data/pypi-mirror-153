from loader.GitLoader import download_all_mibs_from_artifactory, set_up_folder_structure
from temporaryContainer.TempDir import TempDir
from loader.load_mibs import load_mibs
import os

def compile_and_load_mibs(mib_path, temp_directory_object: TempDir, compiled_mib_path = None, artifactory_base_url ="https://github.com/net-snmp/net-snmp/archive/refs/tags",
                          net_snmp_version = 'v5.9.2.rc1'):



    download_all_mibs_from_artifactory(artifactory_base_url=artifactory_base_url, package_version=net_snmp_version,
                                       temporary_directory_object=temp_directory_object)

    set_up_folder_structure(temporary_directory_object=temp_directory_object, mib_path=mib_path)

    load_mibs(mib_names=[mib_path.rsplit(os.path.sep, maxsplit=1)[-1].replace('.mib', '')], compiled_mib_path=compiled_mib_path,
              temporary_object=temp_directory_object)