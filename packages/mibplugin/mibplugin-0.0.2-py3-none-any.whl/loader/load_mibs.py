from loader.MibLoader import MibLoader
from temporaryContainer.TempDir import TempDir
import os
import pathlib
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__file__)

def load_mibs(mib_names, compiled_mib_path = None, dependant_mib_path = None, source_mib_path = None, temporary_object: TempDir = None):
    """
    Load Mibs, compiling them should the need arise. If unable to load, the mibs are compiled and saved to the compiled path or a temp location if it is not
    given.

    example - load_mibs(['INFINERA-GX-MIB'], compiled_mib_path = <dir as a pathlike[str] object>, dependant_mib_path=[file://dirpathasurl], source_mib_path=[file://dirpathurl])

    :param mib_names: Names of mibs to load as a list
    :type mib_names: list[str]
    :param compiled_mib_path: The path where the mibs are in their compiled form. If left empty, the mibs are compiled to temp.
    :type compiled_mib_path: str
    :param dependant_mib_path: List of directories where dependant mibs are, in the form URLs - file://, http://, etc.
    :type dependant_mib_path: list[str]
    :param source_mib_path: List of directories where required mibs that need to be compiled are
    :type source_mib_path: list[str]
    :return: A MibLoader object that can be passed around to SNMP functions. This should also be passed onto the close_mib_viewer function.
    :rtype: MibLoader

    """

    if compiled_mib_path is None:
        compiled_mib_path = os.path.join(temporary_object.get_full_path(), 'mib_paths', 'compiled_mibs')

    if source_mib_path is None:
        source_mib_path = [os.path.join(temporary_object.get_full_path(), 'mib_paths', 'uncompiled_mibs')]

    if dependant_mib_path is None:
        dependant_mib_path = [os.path.join(temporary_object.get_full_path(), 'mib_paths')]

    os.environ['PYSNMP_MIB_DIRS'] = ':'.join(dependant_mib_path)

    os.environ['PYSNMP_MIB_DIRS'] = compiled_mib_path

    source_mib_path_uri = [pathlib.Path(each_path).as_uri().replace('///', '//') if os.path.sep != '/' else pathlib.Path(each_path).as_uri() for each_path in source_mib_path]

    dependant_mib_path_uri = [pathlib.Path(each_path).as_uri().replace('///', '//') if os.path.sep != '/' else pathlib.Path(each_path).as_uri() for each_path in dependant_mib_path]

    logger.info(source_mib_path_uri)

    logger.info(os.listdir(compiled_mib_path))

    logger.info(os.listdir(source_mib_path[0]))

    mib_loader = MibLoader(compiled_mib_path=compiled_mib_path, source_mib_path=source_mib_path_uri,
                           dependant_mib_paths=dependant_mib_path_uri)

    mib_loader.load(mib_names=mib_names)

    logger.info(os.listdir(compiled_mib_path))

    return mib_loader

def close_mib_viewer(mib_loader):
    """
    Call after opening mib object at the end after viewing the mib.

    :param mib_loader: Mib object returned by load_mibs
    :return: None
    """


    mib_loader.cleanup_temp()



