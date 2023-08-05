import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

logger = logging.getLogger(__name__)

DEFAULT_PODINFO_PATH = '/etc/podinfo'
DOT_REPLACEMENT = '-'


def parse_properties(lines: List[str]) -> Dict[str, str]:
    lines = (line.split('=', 1) for line in lines if line)
    return {
        # NOTE: elastic is not accepting keys with dots
        k.strip().replace('.', DOT_REPLACEMENT): v.strip().strip('"')
        for k, v in lines
    }


def get_k8s_metadata(metadata_dir: Union[str, Path] = None) -> Optional[Dict]:
    metadata_dir = Path(metadata_dir or DEFAULT_PODINFO_PATH)
    metadata = {}
    if not metadata_dir.exists() or not metadata_dir.is_dir():
        # TODO try to get from env vars?
        return

    for path in metadata_dir.iterdir():
        if not path.is_file():
            continue
        try:
            with path.open() as f:
                lines = f.readlines()
                if len(lines) == 1 and lines[0] and '=' not in lines[0]:
                    metadata[path.name] = lines[0].strip()
                else:
                    metadata[path.name] = parse_properties(lines)
        except Exception as e:
            logger.warning(f'Failed to parse k8s metadata at `{path}`: {e}')
    return metadata


original_log_record_factory = logging.getLogRecordFactory()


def setup_logging_k8s_metadata(metadata_attr_name: str = None, metadata_dir: Union[str, Path] = None, dump=True):
    """
    Set up log record factory

    Set up custom factory which sets kubernetes metadata attribute into log
    record.

    Args:
        metadata_attr_name: Kubernetes metadata attribute name.
            Default: 'kubernetes'
        metadata_dir: Metadata directory. Default: '/etc/podinfo'
        dump: Whether to dump metadata to json
    """

    def log_record_factory(*args, **kwargs):
        record = original_log_record_factory(*args, **kwargs)
        setattr(record, metadata_attr_name or 'kubernetes', k8s_metadata)
        return record

    k8s_metadata = get_k8s_metadata(metadata_dir=Path(metadata_dir or DEFAULT_PODINFO_PATH))
    if dump:
        k8s_metadata = json.dumps(k8s_metadata)
    logging.setLogRecordFactory(log_record_factory)
