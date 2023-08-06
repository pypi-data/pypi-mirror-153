from enum import unique, Enum


@unique
class DataType(Enum):
	String = 1
	Object = 2
	OneOf = 3
	Array = 4
	Integer =5
	Float = 6
	Boolean = 7


@unique
class VersionMutationType(Enum):
	AddField = 1 # name + def
	RemoveField = 2 # name
	MutateField = 3 # new def (no rename)
	RenameField = 4
	AddRule = 5 # index
	RemoveRule = 6 # rule index
	MutateRule = 7 # rule index + new rule + config


@unique
class ValidationMode(Enum):
	Input = 1
	Output = 2
	Instantiate = 3