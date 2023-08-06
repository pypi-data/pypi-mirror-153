from ....module.flutter.identity import FlutterTaskIdentity
from ....module.flutter.task.command import FlutterCommandTask

__all__ = ["FlutterPubGetIdentity"]

FlutterPubGetIdentity = FlutterTaskIdentity(
    "pub-get",
    "Runs flutter pub get",
    [],
    lambda: FlutterCommandTask(command=["pub", "get"], describe="Running pub get", require_project=True),
)
