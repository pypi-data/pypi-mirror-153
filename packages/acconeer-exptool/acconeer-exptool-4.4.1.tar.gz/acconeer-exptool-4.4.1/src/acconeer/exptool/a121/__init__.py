import sys

from ._cli import ExampleArgumentParser, get_client_args
from ._core import (
    PRF,
    Client,
    ClientError,
    ClientInfo,
    H5Record,
    H5Recorder,
    IdleState,
    Metadata,
    PersistentRecord,
    Profile,
    Record,
    Recorder,
    Result,
    SensorConfig,
    SensorInfo,
    ServerInfo,
    SessionConfig,
    StackedResults,
    SubsweepConfig,
    load_record,
    open_record,
    save_record,
    save_record_to_h5,
)


if "pytest" not in sys.modules:
    import warnings

    warnings.warn(
        "The a121 package is currently an unstable API and may change at any time.",
        FutureWarning,
    )
