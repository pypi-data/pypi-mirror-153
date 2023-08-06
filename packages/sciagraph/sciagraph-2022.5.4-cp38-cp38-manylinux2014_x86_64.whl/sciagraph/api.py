"""Public API for interacting with Sciagraph."""

from datetime import datetime, timezone
from typing import Optional
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from ctypes import CDLL, c_uint32, c_char, POINTER

__all__ = ["ReportResult", "set_job_id"]

_LOGGER = logging.getLogger("sciagraph")

_DOWNLOAD_INSTRUCTIONS = """\
Successfully uploaded the Sciagraph profiling report.

Job start time: {job_time}
Job ID: {job_id}

{local_storage}\
An encrypted copy of the report was uploaded to the Sciagraph storage server.
To download the report, run the following on Linux/Windows/macOS, Python 3.7+.

If you're inside a virtualenv:

    pip install --upgrade sciagraph-report

Otherwise:

    pip install --user --upgrade sciagraph-report

Then:

    python -m sciagraph_report download {download_key} {decryption_key}

If you have trouble installing sciagraph-report, please read the documentation:

https://sciagraph.com/docs/howto/report-viewer
"""

_STORAGE_INSTRUCTIONS = """\
Successfully uploaded the Sciagraph profiling report.

Job start time: {job_time}
Job ID: {job_id}

The report was stored in {report_path}
"""


@dataclass
class ReportResult:
    """
    Information about how to download uploaded profiling report.

    This will get logged by Sciagraph when profiling is finished.
    """

    job_time: str
    job_id: str
    download_key: Optional[str]
    decryption_key: Optional[str]
    report_path: Optional[Path]

    def __str__(self):
        if self.download_key is not None and self.decryption_key is not None:
            if self.report_path is not None:
                local_storage = (
                    f"The report was stored locally at path {self.report_path}\n\n"
                )
            else:
                local_storage = ""
            return _DOWNLOAD_INSTRUCTIONS.format(
                **asdict(self), local_storage=local_storage
            )
        else:
            return _STORAGE_INSTRUCTIONS.format(**asdict(self))


_UNKNOWN_JOB_ID = "Unknown, see docs to learn how to set this"


def _log_result(
    job_secs_since_epoch: int,
    job_id: Optional[str],
    download_key: Optional[str],
    decryption_key: Optional[str],
    report_path: Optional[Path],
):
    """Log a ``ReportResult``."""
    if job_id is None:
        job_id = _UNKNOWN_JOB_ID
    job_time = datetime.fromtimestamp(job_secs_since_epoch, timezone.utc).isoformat()
    report = ReportResult(
        job_time=job_time,
        job_id=job_id,
        download_key=download_key,
        decryption_key=decryption_key,
        report_path=report_path,
    )
    _LOGGER.warning(report)


def set_job_id(job_id: str):
    """
    Set the current job's ID; it will then be included in the resulting report
    and logged message.
    """
    if not isinstance(job_id, str):
        job_id = f"You called set_job_id() wih a non-string value: {repr(job_id)}"

    # The symbols in the current running process:
    dll = CDLL(None)
    f = getattr(dll, "sciagraph_set_job_id", None)
    if f is None:
        # Profiling is not actually happening, do nothing
        return

    f.argtypes = [POINTER(c_char), c_uint32]
    f.restype = None
    job_id_bytes = job_id.encode("utf-8")
    f(job_id_bytes, len(job_id_bytes))
