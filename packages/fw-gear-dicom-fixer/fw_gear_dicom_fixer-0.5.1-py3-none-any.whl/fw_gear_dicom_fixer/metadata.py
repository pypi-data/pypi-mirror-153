import datetime
import logging
import sys
import typing as t
from collections import Counter

from fw_file.dicom import DICOM, DICOMCollection
from fw_file.dicom.config import IMPLEMENTATION_CLASS_UID, IMPLEMENTATION_VERSION_NAME
from fw_file.dicom.fixer import ReplaceEvent, TrackedRawDataElement
from fw_file.dicom.utils import generate_uid
from pydicom.datadict import dictionary_VR, tag_for_keyword
from pydicom.dataelem import DataElement, DataElement_from_raw
from pydicom.dataset import Dataset
from pydicom.filebase import DicomBytesIO
from pydicom.filewriter import write_data_element
from pydicom.sequence import Sequence
from pydicom.tag import BaseTag
from pydicom.valuerep import validate_value
from pydicom.values import convert_value
from tzlocal import get_localzone

from . import pkg_name
from .fixers import empty_pydicom_callback

log = logging.getLogger(__name__)


def add_non_conforming_element(seq: Sequence, tag: BaseTag, val: t.Any):
    """Add an element to the NonConformingElementSequence.

    If an original element was non conforming, add it here.
    """
    # NOTE: More to add here if we want, also supports private
    # tags with a specific creator, etc.
    el = Dataset()
    el.SelectorAttribute = tag
    # Not reporting multiple non-conforming elements in a vm > 1 el.
    # Simply report a problem with the whole element at idx 1
    el.SelectorValueNumber = 1
    el.NonconformingDataElementValue = val
    seq.append(el)


def handle_tracker_event(
    modified: Dataset,
    non_conforming: Sequence,
    original: TrackedRawDataElement,
    buffer: DicomBytesIO,
) -> None:
    """Write tracker events.

    Takes in:
    - Dataset for ModifiedAttributesSequence
    - a Sequence for NonconformingModifiedAttributesSequence.
    - A TrackedRawDataElement
    """
    orig = original.export()["original"]
    try:
        # Validation mode RAISE
        val = convert_value(orig.VR, orig)
        validate_value(orig.VR, val, 2)
        with empty_pydicom_callback():
            elem = DataElement_from_raw(orig)
            write_data_element(buffer, elem)
        modified[orig.tag] = elem
    except Exception:  # pylint: disable=broad-except
        log.debug(
            (
                f"{str(orig)} invalid, writing to "
                "NonconformingModifiedAttributesSequence"
            ),
            exc_info=True,
        )
        add_non_conforming_element(non_conforming, orig.tag, orig.value)


def handle_replace_event(
    modified: Dataset,
    non_conforming: Sequence,
    original: ReplaceEvent,
    buffer: DicomBytesIO,
) -> None:
    """Write replace events.

    Takes in:
    - Dataset for ModifiedAttributesSequence
    - a Sequence for NonconformingModifiedAttributesSequence.
    - A ReplaceEvent
    """
    # NOTE: Eventually this won't work if we want to track private data
    # elements.  See note in add_non_conforming_element as well.

    # Just a replace event passed in.  Need to look up tag and VR
    tag = tag_for_keyword(original.field)
    VR = ""
    de: t.Optional[DataElement] = None
    if tag:
        try:
            VR = dictionary_VR(tag)
            # Validation mode RAISE
            validate_value(VR, original.old, 2)
            de = DataElement(tag, VR, original.old)
            with empty_pydicom_callback():
                write_data_element(buffer, de)
        except (ValueError, KeyError):
            log.debug(
                f"{original} invalid, writing to "
                "NonconformingModifiedAttributesSequence"
            )
            # If either tag doesn't have VR or if the value is invalid,
            # write to nonconforming sequence
            add_non_conforming_element(non_conforming, BaseTag(tag), original.old)
            return
        modified[tag] = de
    else:
        log.error(f"Cannot write ReplaceEvent {original}")
        return


def update_modified_dicom_info(
    dcm: DICOM, evts: t.Optional[t.List[ReplaceEvent]] = None
) -> None:
    """Add OriginalAttributesSequence and Implementation information.

    Args:
        dcm (DICOM): DICOM to update.
    """
    add_implementation(dcm)
    # Modified and non-conforming datasets
    mod_dat, non_conform = Dataset(), Sequence()
    dcm_buffer = DicomBytesIO()
    dcm_buffer.is_little_endian = True
    dcm_buffer.is_implicit_VR = False
    for element in dcm.tracker.data_elements:
        handle_tracker_event(mod_dat, non_conform, element, dcm_buffer)
    if evts:
        for evt in evts:
            handle_replace_event(mod_dat, non_conform, evt, dcm_buffer)

    # Only update if anything changed.
    if mod_dat or non_conform:
        log.debug(f"Populating OriginalAttributesSequence on {dcm.localpath}")
        time_zone = get_localzone()
        curr_dt = datetime.datetime.now().replace(tzinfo=time_zone)
        curr_dt_str = curr_dt.strftime("%Y%m%d%H%M%S.%f%z")
        # Original attributes dataset
        orig_dat = Dataset()
        # Add Modified attributes dataset as a sequence
        orig_dat.ModifiedAttributesSequence = Sequence([mod_dat])
        orig_dat.NonconformingModifiedAttributesSequence = non_conform
        orig_dat.ModifyingSystem = pkg_name
        orig_dat.ReasonForTheAttributeModification = "CORRECT"
        orig_dat.AttributeModificationDateTime = curr_dt_str
        orig_dat.SourceOfPreviousValues = ""

        raw = dcm.dataset.raw
        if not raw.get("OriginalAttributesSequence", None):
            raw.OriginalAttributesSequence = Sequence()
        raw.OriginalAttributesSequence.append(orig_dat)


def add_implementation(dcm: DICOM) -> None:
    """Write implementation information to a dicom.

    Args:
        dcm (DICOM): DICOM to update.
    """
    i_class_uid = dcm.dataset.raw.file_meta.get("ImplementationClassUID")
    i_version_name = dcm.dataset.raw.file_meta.get("ImplementationVersionName")

    if not i_class_uid or i_class_uid != IMPLEMENTATION_CLASS_UID:
        log.debug(f"Adding ImplementationClassUID: {IMPLEMENTATION_CLASS_UID}")
        setattr(dcm, "ImplementationClassUID", IMPLEMENTATION_CLASS_UID)

    if not i_version_name or i_version_name != IMPLEMENTATION_VERSION_NAME:
        log.debug(f"Addding ImplementationVersionName: {IMPLEMENTATION_VERSION_NAME}")
        setattr(dcm, "ImplementationVersionName", IMPLEMENTATION_VERSION_NAME)


def add_missing_uid(dcms: DICOMCollection) -> bool:
    """Check for and add missing SeriesInstanceUID.

    Args:
        dcms (DICOMCollection): Dicom to check.

    Returns:
        (bool): Whether or not any modification was made.

    Raises:
        ValueError: When multiple SeriesInstanceUIDs are present across archive
    """
    mod = False
    series_uid = None
    try:
        series_uid = dcms.get("SeriesInstanceUID")
    except ValueError:
        counts = Counter(dcms.bulk_get("SeriesInstanceUID"))
        log.error(
            f"Multiple SeriesInstanceUIDs found: \n{counts} " "\nPlease run splitter."
        )
        sys.exit(1)

    sops = dcms.bulk_get("SOPInstanceUID")
    if not all(sops):
        log.info("Populating missing SOPInstanceUIDs.")
        for dcm in dcms:
            if not dcm.get("SOPInstanceUID"):
                setattr(dcm, "SOPInstanceUID", generate_uid())
        mod = True

    if not series_uid:
        log.info("Populating missing SeriesInstanceUID.")
        series_uid = generate_uid()
        dcms.set("SeriesInstanceUID", series_uid)
        mod = True

    return mod
