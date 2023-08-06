import contextlib
import logging
import typing as t
from difflib import get_close_matches
from warnings import warn

from fw_file.dicom import DICOM, get_config
from fw_file.dicom.fixer import ReplaceEvent, raw_elem_tracker
from pydicom.charset import decode_element
from pydicom.datadict import tag_for_keyword
from pydicom.dataelem import DataElement
from pydicom.dataset import Dataset
from pydicom.tag import BaseTag
from pydicom.uid import ExplicitVRLittleEndian as standard
from pydicom.uid import UncompressedTransferSyntaxes

log = logging.getLogger(__name__)

# Black likes to format this with one entry on each line...
# fmt: off
MODALITIES = [
    "ANN", "AR", "ASMT", "AU", "BDUS", "BI", "BMD", "CR", "CT", "CTPROTOCOL",
    "DMS", "DG", "DOC", "DX", "ECG", "EEG", "EMG", "EOG", "EPS", "ES", "FID",
    "GM", "HC", "HD", "IO", "IOL", "IVOCT", "IVUS", "KER", "KO", "LEN", "LS",
    "MG", "MR", "M3D", "NM", "OAM", "OCT", "OP", "OPM", "OPT", "OPTBSV",
    "OPTENF", "OPV", "OSS", "OT", "PLAN", "Note", "POS", "PR", "PT", "PX",
    "REG", "RESP", "RF", "RG", "RTDOSE", "RTIMAGE", "RTINTENT", "RTPLAN",
    "RTRAD", "RTRECORD", "RTSEGANN", "RTSTRUCT", "RWV", "SEG", "SM", "SMR",
    "SR", "SRF", "STAIN", "TEXTUREMAP", "TG", "US", "VA", "XA", "XAPROTOCOL",
    "XC",
]
# fmt: on


def is_dcm(dcm: DICOM) -> bool:
    """Look at a potential dicom and see whether it actually is a dicom.

    Args:
        dcm (DICOM): DICOM

    Returns:
        bool: True if it probably is a dicom, False if not
    """
    num_pub_tags = 0
    keys = dcm.dir()
    for key in keys:
        try:
            if BaseTag(tag_for_keyword(key)).group > 2:  # type: ignore
                num_pub_tags += 1
        except (AttributeError, TypeError):
            continue
    # Require two public tags outside the file_meta group.
    if num_pub_tags > 1:
        return True
    log.debug(f"Removing: {dcm}. Not a DICOM")
    return False


def fix_patient_sex(dcm: DICOM) -> t.Optional[ReplaceEvent]:
    """Fix PatientSex attribute on a dicom.

    Returns:
        ReplaceEvent or None
    """
    if hasattr(dcm, "PatientSex"):
        sex = dcm.PatientSex
        if sex in ["M", "O", "F"]:
            return None
        match = get_close_matches(sex.lower(), ["male", "female"], n=1)
        if match:
            dcm.PatientSex = "M" if match[0] == "male" else "F"
        else:
            warn(f"Could not find match for PatientSex '{sex}' " "Setting to O (other)")
            dcm.PatientSex = "O"
        return ReplaceEvent("PatientSex", sex, dcm.PatientSex)
    return None


def fix_incorrect_units(dcm: DICOM) -> t.Optional[ReplaceEvent]:
    """Fix known incorrect units.

    Returns:
        ReplaceEvent or None
    """
    # MagneticFieldStrength should be in Tesla, if larger than 30, it's
    # probably milli-Tesla, so divide by 1000 to put in Tesla
    if hasattr(dcm, "MagneticFieldStrength"):
        mfs = dcm.MagneticFieldStrength
        if mfs:
            if mfs > 30:
                dcm.MagneticFieldStrength = mfs / 1000
                return ReplaceEvent(
                    "MagneticFieldStrength", mfs, dcm.MagneticFieldStrength
                )
    return None


def fix_invalid_modality(dcm: DICOM) -> t.Optional[ReplaceEvent]:
    """Fix invalid Modality field."""
    if hasattr(dcm, "Modality"):
        existing_modality = dcm.Modality
        if existing_modality is None:
            dcm.Modality = "OT"
        elif existing_modality not in MODALITIES:
            # Search for close matches, return at most 1
            match = get_close_matches(existing_modality, MODALITIES, n=1)
            # If there is a match, use that, otherwise set to OT for other.
            if match:
                dcm.Modality = match[0]
            else:
                dcm.Modality = "OT"
        else:
            return None
        return ReplaceEvent("Modality", existing_modality, dcm.Modality)
    dcm.Modality = "OT"
    return ReplaceEvent("Modality", None, dcm.Modality)


def apply_fixers(dcm: DICOM) -> t.List[ReplaceEvent]:
    """Apply all post-decoding fixers to a DICOM.

    Return a list of ReplaceEvent's for anything that was changed/fixed.
    """
    evts: t.List[ReplaceEvent] = []
    fixers = [fix_patient_sex, fix_incorrect_units, fix_invalid_modality]
    for fixer in fixers:
        evt = fixer(dcm)
        if evt:
            evts.append(evt)
    return evts


def decode_dcm(dcm: DICOM) -> None:
    """Decode dicom.

       Mirrors pydicom.dataset.Dataset.decode, except it ignores decoding the
       OriginalAttributesSequence tag.

    Args:
        dcm (DICOM): dicom file.
    """
    # pylint: disable=protected-access
    dicom_character_set = dcm.dataset.raw._character_set

    def decode(_dataset: Dataset, data_element: DataElement) -> None:
        """Callback to decode data element, but ignore OriginalAttributesSequence."""

        if data_element.VR == "SQ":
            if data_element.tag == tag_for_keyword("OriginalAttributesSequence"):
                return
            for dset in data_element.value:
                dset._parent_encoding = dicom_character_set
                dset.decode()
        else:
            decode_element(data_element, dicom_character_set)

    with raw_elem_tracker(dcm.tracker):
        dcm.walk(decode, recursive=False)
    # pylint: enable=protected-access


@contextlib.contextmanager
def empty_pydicom_callback():
    """Context manager that empties callbacks/fixers."""
    config = get_config()
    orig_fixers = config.raw_elem_fixers
    config.raw_elem_fixers = []
    try:
        yield
    finally:
        config.raw_elem_fixers = orig_fixers


def standardize_transfer_syntax(dcm: DICOM):  # pragma: no cover
    """Set TransferSyntaxUID to ExplicitVRLittleEndian.

    Args:
        dcm (DICOM): dicom file.

    Returns:
        bool: True if TransferSyntaxUID has been changed, False otherwise
    """
    # Attempt to decompress dicom PixelData with GDCM if compressed
    if dcm.dataset.raw.file_meta.TransferSyntaxUID != standard:
        log.debug(f"Convert TransferSyntaxUID to {standard} for  {dcm.localpath}")
        if (
            dcm.dataset.raw.file_meta.TransferSyntaxUID
            not in UncompressedTransferSyntaxes
        ):
            log.debug(f"Decompress {dcm.localpath}")
            dcm.dataset.raw.decompress(handler_name="gdcm")
        dcm.dataset.raw.is_implicit_VR = False
        dcm.dataset.raw.is_little_endian = True
        dcm.dataset.raw.file_meta.TransferSyntaxUID = standard
        return True
    return False
