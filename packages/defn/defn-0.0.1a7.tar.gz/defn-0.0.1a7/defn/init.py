import json
import os


def once():
    context = {"excludeStackIdFromLogicalIds": True, "allowSepCharsInLogicalIds": True}
    os.environ.setdefault("CDKTF_CONTEXT_JSON", json.dumps(context))


once()
