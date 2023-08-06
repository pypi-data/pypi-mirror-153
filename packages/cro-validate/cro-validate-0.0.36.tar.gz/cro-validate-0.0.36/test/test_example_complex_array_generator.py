import json

import cro_validate.api.definition_api as DefinitionApi
import cro_validate.api.exception_api as ExceptionApi
import cro_validate.api.example_api as ExampleApi
import cro_validate.classes.rule_classes as Rules
import cro_validate.input.normalize_input as NormalizeInput
import cro_validate.classes.schema_classes as Schemas
from cro_validate.enum import DataType


class Boolean(Rules.Rule):
	def _as_bool(self, name, value):
		# Int must be 1 or 0
		try:
			int_value = NormalizeInput.as_int_within_inclusive_range(name, value, 0, 1)
			if int_value == 0:
				return False
			if int_value == 1:
				return True
		except:
			pass
		# String must be True or False (case insensitive)
		str_value = str(value)
		if str_value.lower() == 'true':
			return True
		if str_value.lower() == 'false':
			return False
		msg = "Expected to be 'True' or 'False' (case insensitive), not ['{0}'].".format(value)
		raise ExceptionApi.create_input_error(name, msg)

	def __init__(self):
		super().__init__(
				description='Must be one of 0, 1, True, False (case insensitive).',
				callback=self._as_bool
			)


json_str = '''
{
	"a": {
		"data_type": "Boolean",
		"default_value": false,
		"default_value_type": "builtins.bool",
		"description": "Demo field a.",
		"rules": [
			{
				"config": {},
				"type": "test.test_example_complex_array_generator.Boolean"
			}
		]
	},
	"b": {
		"data_type": "Boolean",
		"default_value": false,
		"default_value_type": "builtins.bool",
		"description": "Demo field b.",
		"rules": [
			{
				"config": {},
				"type": "test.test_example_complex_array_generator.Boolean"
			}
		]
	},
	"RootModel": {
		"data_format": {
			"load_defaults": true,
			"model": {
				"a": {
					"required": false
				},
				"b": {
					"required": false
				},
				"c": {
					"definition_name": "ChildModel",
					"required": true
				}
			},
			"model_type": "SchemaDefinition"
		},
		"data_format_type": "cro_validate.classes.schema_classes.Schema",
		"data_type": "Object",
		"description": "Root model."
	},
	"ChildModel": {
		"data_format": {
			"load_defaults": true,
			"model": {
				"a1": {
					"definition_name": "a"
				}
			},
			"model_type": "SchemaDefinition"
		},
		"data_format_type": "cro_validate.classes.schema_classes.Schema",
		"data_type": "Object",
		"description": "Demo model 2."
	},
	"RootModelArray": {
		"data_format": "RootModel",
		"data_format_type": "builtins.str",
		"data_type": "Array",
		"description": "RootModel array."
	},
	"ChildModelArray": {
		"data_format": "ChildModel",
		"data_format_type": "builtins.str",
		"data_type": "Array",
		"description": "ChildModel array."
	}
}
'''


def register():
	DefinitionApi.clear()

	root = json.loads(json_str)
	DefinitionApi.from_json_dict(root)


def test__complex__array__object_validation():
	register()
	v = {
			'a':True,
			'c': {
					'a1': True
				}
		}
	result = DefinitionApi.validate_input('RootModel', v)


def test__complex_array__object_generation():
	register()
	v = {'a':[True, 100], 'b':[False, -1], 'c': {'a1':[True, -2]}}
	result = []
	for example in ExampleApi.get_example_generator('RootModel', given_values=v):
		print(json.dumps(example, indent=2, sort_keys=True))
		result.append(example)
	assert len(result) == 4


def test__complex__array_generation():
	register()
	# 6 possible invalid + 1 valid => 7 cases
	v = [
			{'a':[True, 100], 'b':[False, -1], 'c': {'a1':[False, 1]}},
			{'a':[False, 200], 'b':[True, -2], 'c': {'a1':[False, 2]}}
		]
	result = []
	for example in ExampleApi.get_example_generator('RootModelArray', given_values=v):
		print(json.dumps(example, indent=2, sort_keys=True))
		result.append(example)
	assert len(result) == 7
