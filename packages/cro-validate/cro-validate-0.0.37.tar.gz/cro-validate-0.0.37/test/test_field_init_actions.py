import json, pytest

import cro_validate.api.definition_api as DefinitionApi
import cro_validate.api.exception_api as ExceptionApi
import cro_validate.api.example_api as ExampleApi
import cro_validate.classes.rule_classes as Rules
import cro_validate.input.normalize_input as NormalizeInput
import cro_validate.classes.schema_classes as Schemas
from cro_validate.enum import DataType

definitions_json = '''
{
	"TestModel": {
		"data_format": {
			"model": {
				"s": {},
				"options": {
				}
			},
			"dependency_resolver": {
				"kw": {},
				"type": "test_one_of_definition.TestResolver"
			},
			"model_name": "TestModel",
			"model_type": "SchemaDefinition"
		},
		"data_format_type": "cro_validate.classes.schema_classes.Schema",
		"data_type": "Object",
		"description": "Job item."
	},
	"A": {
		"data_format": {
			"model": {
				"variant_i": {
					"definition_name": "i",
					"required": false
				},
				"random_s": {
					"definition_name": "s",
					"required": false
				}
			},
			"model_name": "A",
			"model_type": "SchemaDefinition",
			"field_init_actions": [
				{
					"type": "cro_validate.classes.field_init_action_classes.SetFieldsRequired",
					"kw": {
						"required": true,
						"pattern": ".*"
					}
				}
			]
		},
		"data_format_type": "cro_validate.classes.schema_classes.Schema",
		"data_type": "Object",
		"description": "Test type A."
	},
	"B": {
		"data_format": {
			"model": {
				"variant_i": {
					"definition_name": "i",
					"required": false
				},
				"random_s": {
					"definition_name": "s",
					"required": false
				}
			},
			"model_name": "A",
			"model_type": "SchemaDefinition",
			"field_init_actions": [
				{
					"type": "cro_validate.classes.field_init_action_classes.SetFieldsRequired",
					"kw": {
						"required": true,
						"pattern": ".*"
					}
				},
				{
					"type": "cro_validate.classes.field_init_action_classes.SetFieldsRequired",
					"kw": {
						"required": false,
						"field_list": ["random_s"]
					}
				}
			]
		},
		"data_format_type": "cro_validate.classes.schema_classes.Schema",
		"data_type": "Object",
		"description": "Test type A."
	},
	"options": {
		"data_format": ["i", "variant_1", "A"],
		"data_format_type": "builtins.list",
		"data_type": "OneOf",
		"description": "Dependent on model state."
	},
	"s": {
		"data_type": "String",
		"description": "Sample string."
	},
	"i": {
		"data_type": "Integer",
		"description": "Sample integer.",
		"rules": [
			{
				"config": {
					"minimum": -11
				},
				"type": "cro_validate.classes.rule_classes.IntGte"
			}
		]
	},
	"variant_1": {
		"data_type": "Float",
		"description": "Variant 1 float.",
		"rules": [
			{
				"config": {
					"minimum": -11
				},
				"type": "cro_validate.classes.rule_classes.FloatGte"
			}
		]
	}
}
'''


class TestResolver:
	def _resolve_options(self, fqn, field_name, obj):
		if obj.s == 'base_case':
			return 'i'
		if obj.s == 'variant_1':
			return 'variant_1'
		if obj.s == 'variant_2':
			return 'A'
		if obj.s == 'variant_3':
			return 'missing_from_one_of'

	def resolve(self, fqn, field_name, obj):
		if field_name == 'options':
			return self._resolve_options(fqn, field_name, obj)


def _register():
	DefinitionApi.clear()
	json_dict = json.loads(definitions_json)
	DefinitionApi.from_json_dict(json_dict)


def test_init_actions_basic():
	_register()
	definition = DefinitionApi.get('A')
	fields = definition.list_fields()
	for field_name in fields:
		field = fields[field_name]
		msg = 'All fields.required must be initialized to True ({0}.required != True)'.format(field_name)
		assert field.required is True, msg


def test_init_actions_random_s_false():
	_register()
	definition = DefinitionApi.get('B')
	fields = definition.list_fields()
	assert fields['variant_i'].required is True
	assert fields['random_s'].required is False
