import argparse
from pylabview_helpers.vi import get_vi
from vicommithooks.attributes import is_vi_source_only
from vicommithooks.version import get_vi_version, LVVersion


def run_vi_checks(
    file_path, recursive, min_version, max_version, not_prerelease, assert_source_only
):
    files_to_check = []
    if recursive:
        for currentpath, folders, files in os.walk(root_dir):
            for file in files:
                filename, file_extension = os.path.splitext(file)
                if ".vi" == file_extension:
                    path = os.path.join(currentpath, file)
                    files_to_check.append(path)
    else:
        files_to_check.append(file_path)

    for file in files_to_check:
        vi = get_vi(file, parse_diagrams=False, parse_save_record=True)
        version = get_vi_version(vi)
        higher_version = LVVersion({"major": max_version})
        low_version = LVVersion({"major": min_version})
        if version > higher_version:
            raise RuntimeError(
                f"{file} is saved with {version}, but we require {higher_version} or lower."
            )
        if version < low_version:
            raise RuntimeError(
                f"{file} is saved with {version}, but we require {low_version} or higher."
            )
        if not_prerelease and version.is_prerelease:
            raise RuntimeError(f"{file} is saved with a prerelease version of LabVIEW.")
        if assert_source_only and not is_vi_source_only(vi):
            raise RuntimeError(f"{file} has not been set as source only.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", action="store")
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        default=False,
        help="Recursively searched the path for all VIs.",
    )
    parser.add_argument(
        "--source-only",
        action="store_true",
        default=False,
        help="Asserts the VI(s) are set to source only",
    )
    parser.add_argument(
        "--min-version",
        action="store",
        default=0,
        type=int,
        help="Asserts that the major version of LabVIEW the VI was saved with is greater than or equal to this value",
    )
    parser.add_argument(
        "--max-version",
        action="store",
        default=1000,
        type=int,
        help="Asserts that the major version of LabVIEW the VI was saved with is less than or equal to this value",
    )
    parser.add_argument(
        "--not-prerelease",
        action="store_true",
        default=False,
        help="Asserts that the version of LabVIEW the VI was saved with is not a prerelease version",
    )
    options = parser.parse_args()
    run_vi_checks(
        options.file,
        options.recursive,
        options.min_version,
        options.max_version,
        options.not_prerelease,
        options.source_only,
    )


if __name__ == "__main__":
    main()
