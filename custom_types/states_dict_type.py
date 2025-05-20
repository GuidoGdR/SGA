
from typing import Dict, Literal, Any

states_dict_keysType = Literal["allow_save", "have_changes", "students", "file"]
StatesDictInternalDictType = Dict[Literal["suscriptions", "data"], Any]
StatesDictType = Dict[states_dict_keysType, StatesDictInternalDictType]
