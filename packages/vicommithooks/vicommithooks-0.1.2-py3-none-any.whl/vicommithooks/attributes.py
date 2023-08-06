from pylabview_helpers.vi import get_vi
from pylabview.LVinstrument import VI_FLAGS2
from pylabview.LVmisc import getFirstSetBitPos
import re


# mostly stolen from LVmisc.exportXMLBitfields
def flags_to_dict(EnumClass, value, skip_mask=0):
    flags = {}
    for mask in EnumClass:
        if (mask.value & skip_mask) != 0:  # Skip fields given as mask
            continue
        # Add only properties which have bit set or have non-default bit name
        addProperty = ((value & mask.value) != 0) or (
            not re.match("(^[A-Za-z]{0,3}Bit[0-9]+$)", mask.name)
        )
        if not addProperty:
            continue
        nshift = getFirstSetBitPos(mask.value) - 1
        flags[mask.name] = "{:d}".format((value & mask.value) >> nshift)
    return flags


def is_vi_source_only(vi):
    lvsr = vi.get("LVSR")
    execution2_flags = flags_to_dict(VI_FLAGS2, lvsr.sections[0].viFlags2)
    return int(execution2_flags["SourceOnly"]) == 1


def is_vi_source_only_from_path(path):
    vi = get_vi(path, parse_diagrams=False, parse_save_record=True)
    return is_vi_source_only(vi)
