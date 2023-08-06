from pylabview_helpers.vi import get_vi
from pylabview.LVmisc import (
    isGreaterOrEqVersion,
    simpleVersionToString,
    LABVIEW_VERSION_STAGE,
)


class LVVersion:
    def __init__(self, version):
        self._version = version

    def __str__(self):
        return f"{self._version['major']}.{self._version.get('minor',0)}.{self._version.get('bugfix', 0)}"

    def __gt__(self, other):
        if self == other:
            return False
        return isGreaterOrEqVersion(
            self._version,
            other._version.get("major", None),
            other._version.get("minor", None),
            other._version.get("bugfix", None),
            other._version.get("stage", None),
        )

    def __lt__(self, other):
        return self != other and not self > other

    def __le__(self, other):
        return self == other or self < other

    def __eq__(self, other):
        return (
            self._version.get("major", None) == other._version.get("major", None)
            and self._version.get("minor", None) == other._version.get("minor", None)
            and self._version.get("bugfix", None) == other._version.get("bugfix", None)
            and self._version.get("stage", None) == other._version.get("stage", None)
        )

    def is_prerelease(self):
        return self._version["stage"] != LABVIEW_VERSION_STAGE.release


def get_vi_version(vi):
    return LVVersion(vi.getFileVersion())


def get_version_from_path(path):
    vi = get_vi(path, parse_diagrams=False, parse_save_record=True)
    return get_vi_version(vi)
