import cro_validate.classes.definition_classes as Definitions
import cro_validate.classes.util_classes as Utils
from cro_validate.enum import DataType, ValidationMode
import cro_validate.util.definition_util as DefinitionUtil

def get(definition_or_name, version=Utils.Empty):
	"""
	Returns the :ref:`Definition` instance representing this definition. Use the
	returned Definition to retrieve all meta for this definition
	(name, data_type, etc.). Raises input error if Definition is not found.

	:param str definition_or_name: Definition name to retrieve from the global index.
	For convenience, the Definition instance itself may be passed.
	:return: The Definition instance loaded.
	:rtype: Definition
	:raises: Input error if definition not found.
	"""
	return Definitions.Index.get(definition_or_name, version)


def exists(name):
	"""
	Returns True if the name is indexed, otherwise False.

	:param str name: Definition name to verify.
	:return: True if name exists, otherwise False.
	:rtype: bool
	:exception: Input error if definition not found.
	"""
	return Definitions.Index.exists(name)


def as_dict():
	return Definitions.Index.as_dict()


def to_json_dict():
	return Definitions.Index.to_json_dict()


def from_json_dict(root):
	return Definitions.Index.from_json_dict(root)


def add_version(version, display_name=None):
	return Definitions.Index.add_version(version, display_name)


def get_version_display_name(version):
	return Definitions.Index.get_version_display_name(version)


def get_version_by_display_name(display_name):
	return Definitions.Index.get_version_by_display_name(display_name)


def list_versions():
	return Definitions.Index.list_versions()

def compare_versions(a, b):
	return Definitions.Index.compare_versions(a, b)


def list_definition_versions(definition_or_name, include_identical=True):
	return Definitions.Index.list_definition_versions(definition_or_name, include_identical)


def definition_has_version(definition_or_name, version):
	return Definitions.Index.definition_has_version(definition_or_name, version)


def get_definition_base_version(definition_or_name):
	return Definitions.Index.get_definition_base_version(definition_or_name)


def get_definition_final_version(definition_or_name):
	return Definitions.Index.get_definition_final_version(definition_or_name)


def get_definition_previous_version(definition_or_name, version):
	return Definitions.Index.get_definition_previous_version(definition_or_name, version)


def get_latest_version():
	return Definitions.Index.get_latest_version()


def get_first_version():
	return Definitions.Index.get_first_version()


def version_exists(version):
	return Definitions.Index.version_exists(version)


def register_data_type_rule(data_type, rule, exceptions=[]):
	return Definitions.Index.register_data_type_rule(data_type, rule, exceptions)


def register_data_format_rule(data_format, rule, exceptions=[]):
	return Definitions.Index.register_data_format_rule(data_format, rule, exceptions)


def register_definition(
 			name=Utils.Empty,
			aliases=Utils.Empty,
			description=Utils.Empty,
			data_type=Utils.Empty,
			data_format=Utils.Empty,
			default_value=Utils.Empty,
			examples=Utils.Empty,
			nullable=Utils.Empty,
			deprecated=Utils.Empty,
			internal=Utils.Empty,
			rules=Utils.Empty,
			base_version=Utils.Empty,
			base_version_conversion=Utils.Empty,
			versions=Utils.Empty,
			meta=Utils.Empty
		):
	result = Definitions.Index.register_definition(
			name=name,
			aliases=aliases,
			description=description,
			data_type=data_type,
			data_format=data_format,
			default_value=default_value,
			examples=examples,
			nullable=nullable,
			deprecated=deprecated,
			internal=internal,
			rules=rules,
			base_version=base_version,
			base_version_conversion=base_version_conversion,
			versions=versions,
			meta=meta
		)
	return result


def ensure_alias(name, alias):
	Definitions.Index.ensure_alias(name, alias)


def list_definitions():
	results = Definitions.Index.list_definitions()
	return results


def list_dependent_definitions(definition_name):
	results = Definitions.Index.list_dependent_definitions(definition_name)
	return results


def validate_input(
			definition_or_name,
			value,
			field_fqn=None,
			field_name=None,
			version=Utils.Empty,
			**rules_kw
		):
	results = Definitions.Index.validate(
			None,
			field_fqn,
			field_name,
			definition_or_name,
			value,
			version,
			ValidationMode.Input,
			**rules_kw
		)
	return results


def validate_output(
			definition_or_name,
			value,
			field_fqn=None,
			field_name=None,
			version=Utils.Empty,
			**rules_kw
		):
	results = Definitions.Index.validate(
			None,
			field_fqn,
			field_name,
			definition_or_name,
			value,
			version,
			ValidationMode.Output,
			**rules_kw
		)
	return results


def mutate_input_version(
			definition_or_name,
			value,
			src_version,
			target_version,
			field_fqn=None,
			field_name=None,
			**rules_kw
		):
	results = Definitions.Index.mutate_input_version(
			None,
			field_fqn,
			field_name,
			definition_or_name,
			value,
			src_version,
			target_version,
			**rules_kw
		)
	return results


def instantiate(
			fqn,
			field_name,
			definition_or_name,
			version=Utils.Empty,
			validate=True,
			rules_kw={},
			**initial_values
		):
	result = Definitions.Index.instantiate(
			fqn,
			field_name,
			definition_or_name,
			version,
			validate,
			rules_kw,
			**initial_values
		)
	return result


def recurse_definition(
			definition,
			fqn,
			value,
			cb,
			case_sensitive=True,
			ignore_unknown_inputs=False,
			version=Utils.Empty,
			**kw
		):
	return DefinitionUtil.recurse_definition(
				definition,
				fqn,
				None,
				None,
				value,
				cb,
				case_sensitive,
				ignore_unknown_inputs,
				version,
				**kw
			)

def clear():
	Definitions.Index.clear()