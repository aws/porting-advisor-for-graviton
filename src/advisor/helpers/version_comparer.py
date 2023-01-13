import logging
from packaging.version import Version, InvalidVersion

class VersionComparer:
    def compare(version1, version2):
        """Compare two versions in a semantic versioning format

        Args:
            version1 (str): the first version to compare
            version2 (str): the second version to compare

        Returns:
            int: 1 if version1 > version2 \n
                -1 if version1 < version2 \n
                 0 if version1 = version2
        """

        v1 = Version(version1)
        v2 = Version(version2)

        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1
        else:
            return 0
    
    def is_valid(version):
        try:
            Version(version)
        except InvalidVersion:
            logging.debug(f'Invalid version provided: {version}')
            return False
        return True