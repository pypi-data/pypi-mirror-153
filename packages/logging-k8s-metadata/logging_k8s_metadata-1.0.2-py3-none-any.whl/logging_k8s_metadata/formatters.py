from logging_k8s_metadata.utils import get_k8s_metadata

try:
    from fluent.handler import FluentRecordFormatter
except ImportError as e:
    raise ImportError(
        '`fluent-logger` is not installed.\n'
        '\t- pip install logging-k8s-metadata[fluent]\n'
        '\t- pip install fluent-logger\n'
    )


class K8sFluentRecordFormatter(FluentRecordFormatter):
    def __init__(self, fmt=None, datefmt=None, style='%', fill_missing_fmt_key=False, format_json=True,
                 exclude_attrs=None,
                 pod_info_key=None, pod_info_dir=None):
        super().__init__(fmt, datefmt, style, fill_missing_fmt_key, format_json, exclude_attrs)
        self.pod_info_key = pod_info_key or 'kubernetes'
        self.pod_info_dir = pod_info_dir
        self.kubernetes_pod_info = get_k8s_metadata(metadata_dir=pod_info_dir)

    def format(self, record):
        data = super().format(record)
        data[self.pod_info_key] = self.kubernetes_pod_info
        return data
