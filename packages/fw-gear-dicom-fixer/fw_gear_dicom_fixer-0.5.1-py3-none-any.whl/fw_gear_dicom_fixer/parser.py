"""Parser module to parse gear config.json."""
import typing as t
from pathlib import Path

from flywheel_gear_toolkit import GearToolkitContext


def parse_config(
    gear_context: GearToolkitContext,
) -> t.Tuple[Path, bool, bool]:
    """Parse config.json and return relevant inputs and options."""
    input_path = Path(gear_context.get_input_path("dicom")).resolve()
    transfer_syntax = gear_context.config.get("transfer_syntax", False)
    unique = gear_context.config.get("unique", False)
    return input_path, transfer_syntax, unique
