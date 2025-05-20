
from typing import Dict, Literal, Any

settings_dict_key_type = Literal["approve_at", "promote_at"]

SettingsDictType = Dict[settings_dict_key_type, Any]
