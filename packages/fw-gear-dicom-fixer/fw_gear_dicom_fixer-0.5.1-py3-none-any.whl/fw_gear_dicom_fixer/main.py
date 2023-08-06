"""Main module."""

import hashlib
import logging
import typing as t
import warnings
import zipfile
from pathlib import Path

from fw_file.dicom import DICOM, DICOMCollection, get_config
from pydicom import config as pydicom_config
from pydicom.datadict import keyword_for_tag

from .fixers import apply_fixers, decode_dcm, is_dcm, standardize_transfer_syntax
from .metadata import add_missing_uid, update_modified_dicom_info

log = logging.getLogger(__name__)

config = get_config()
pydicom_config.settings.reading_validation_mode = pydicom_config.IGNORE


def run(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    dicom_path: Path, out_dir: Path, transfer_syntax: bool, unique: bool
) -> t.Dict[str, t.List[str]]:
    """Run dicom fixer.

    Args:
        dicom_path (str): Path to directory containing dicom files.l
        out_dir (Path): Path to directory to store outputs.
        transfer_syntax (bool): Change transfer syntax to explicit.
        unique (bool): Remove duplicates.
    """
    events = {}
    log.info("Loading dicom")
    sops: t.Set[str] = set()
    hashes: t.Set[str] = set()
    to_del: t.List[int] = []
    updated_transfer_syntax = False
    if zipfile.is_zipfile(str(dicom_path)):
        dcms = DICOMCollection.from_zip(
            dicom_path, filter_fn=is_dcm, force=True, track=True
        )
    else:
        dcms = DICOMCollection(dicom_path, filter_fn=is_dcm, force=True, track=True)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        log.info("Processing dicoms")
        for i, dcm in enumerate(dcms):
            filename = dcm.filepath.split("/")[-1]
            if unique:
                dcm_hash, sop_instance = get_uniqueness(dcm)
                if dcm_hash in hashes or sop_instance in sops:
                    log.warning(f"Found duplicate dicom at {filename}")
                    to_del.append(i)
                    continue
                hashes.add(dcm_hash)
                sops.add(sop_instance)
            decode_dcm(dcm)
            if transfer_syntax:
                updated_transfer_syntax = standardize_transfer_syntax(dcm)
            # Update events from decoding
            dcm_evts = {}
            dcm.tracker.trim()
            for element in dcm.tracker.data_elements:
                if element.events:
                    tagname = str(element.tag).replace(",", "")
                    kw = keyword_for_tag(element.tag)
                    if kw:
                        tagname = kw
                    dcm_evts[tagname] = [str(ev) for ev in element.events]
            fix_evts = apply_fixers(dcm)

            # Handle post-decoding events from fixers (patient sex, incorrect
            # units, etc.)
            for fix in fix_evts:
                if fix.field in dcm_evts:
                    dcm_evts[fix.field].append(repr(fix))
                else:
                    dcm_evts[fix.field] = [repr(fix)]
            if dcm_evts:
                events[filename] = dcm_evts
            update_modified_dicom_info(dcm)
    if unique:
        log.info(f"Removing {len(to_del)} duplicates")
        # Remove from the end to avoid shifting indexes on deletion
        for d in reversed(sorted(to_del)):
            del dcms[d]
    unique_warnings = handle_warnings(w)
    for msg, count in unique_warnings.items():
        log.warning(f"{msg} x {count} across archive")
    added_uid = add_missing_uid(dcms)

    if (
        (len(events) > 0 and any(len(ev) > 0 for ev in events.values()))
        or added_uid
        or updated_transfer_syntax
        or unique
    ):
        file_name = dicom_path.name
        # Remove zip suffix
        file_name = file_name.replace(".zip", "")
        if len(dcms) > 1:
            file_name += ".zip"
            dcms.to_zip(out_dir / file_name)
        else:
            dcms[0].save(out_dir / file_name)
        log.info(f"Wrote output to {out_dir / dicom_path.name}")

    return events


def handle_warnings(
    warning_list: t.List[warnings.WarningMessage],
) -> t.Dict[t.Union[Warning, str], int]:
    """Find unique warnings and their counts from a list of warnings.

    Returns:
        Dictionary of warnings/str as key and int counts as value
    """
    warnings_dict: t.Dict[t.Union[Warning, str], int] = {}
    for warning in warning_list:
        msg = str(warning.message)
        if msg in warnings_dict:
            warnings_dict[msg] += 1
        else:
            warnings_dict[msg] = 1
    return warnings_dict


def get_uniqueness(dcm: DICOM) -> t.Tuple[str, str]:
    """Get uniqueness of a dicom by InstanceNumber and hash of file.

    Args:
        dcm (DICOM): _description_

    Returns:
        t.Tuple[str, int]: _description_
    """
    path = dcm.filepath
    digest = ""
    with open(path, "rb") as fp:
        md5Hash = hashlib.md5(fp.read())
        digest = md5Hash.hexdigest()
    return digest, dcm.get("SOPInstanceUID", "")
