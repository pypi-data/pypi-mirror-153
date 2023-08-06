import json

import cro_validate.api.definition_api as DefinitionApi
import cro_validate.api.exception_api as ExceptionApi
import cro_validate.api.example_api as ExampleApi
import cro_validate.classes.rule_classes as Rules
import cro_validate.input.normalize_input as NormalizeInput
import cro_validate.classes.schema_classes as Schemas
from cro_validate.enum import DataType, VersionMutationType
from test.test_versions_basic_classes import TestModelVerConv_v0, TestModelVerConv_v1


def register():
	DefinitionApi.clear()

	DefinitionApi.add_version('v0')
	DefinitionApi.add_version('v1')
	DefinitionApi.add_version('v1.1')
	DefinitionApi.add_version('v1.2')
	DefinitionApi.add_version('v2')
	DefinitionApi.add_version('v3')

	json_str = '''
	{
		"a": {
			"data_type": "Boolean",
			"default_value": true,
			"default_value_type": "builtins.bool",
			"description": "Demo field a."
		},
		"b": {
			"data_type": "Boolean",
			"default_value": true,
			"default_value_type": "builtins.bool",
			"description": "Demo field b."
		},
		"TestModel": {
			"base_version": "v0",
			"base_version_conversion": {
				"config": {},
				"type": "test.test_versions_basic_classes.TestModelVerConv_v0"
			},
			"data_format": {
				"load_defaults": true,
				"model": {
					"a": {},
					"b": {
						"required": false
					},
					"e": {
						"definition_name": "a",
						"required": false
					}
				},
				"model_name": "AdditionalItemModel",
				"model_type": "SchemaDefinition"
			},
			"data_format_type": "cro_validate.classes.schema_classes.Schema",
			"data_type": "Object",
			"description": "Demo model.",
			"versions": {
				"v0": {
					"conversion": {
						"config": {},
						"type": "test.test_versions_basic_classes.TestModelVerConv_v0"
					}
				},
				"v1": {
					"conversion": {
						"config": {},
						"type": "test.test_versions_basic_classes.TestModelVerConv_v1"
					},
					"mutations": [
						{
							"action": "AddField",
							"config": {
								"input_name": "c",
								"definition_name": "b",
								"required": false
							}
						},
						{
							"action": "AddField",
							"config": {
								"input_name": "d",
								"definition_name": "b",
								"required": true
							}
						}
					]
				},
				"v2": {
					"mutations": [
						{
							"action": "RemoveField",
							"config": {
								"input_name": "b"
							}
						},
						{
							"action": "MutateField",
							"config": {
								"field_name": "d",
								"definition_name": "a"
							}
						},
						{
							"action": "RenameField",
							"config": {
								"field_name": "e",
								"new_field_name": "f"
							}
						}
					]
				}
			}
		},
		"TestModel2": {
			"base_version": "v1",
			"final_version": "v2",
			"data_format": {
				"load_defaults": true,
				"model": {
					"a": {}
				},
				"model_type": "SchemaDefinition"
			},
			"data_format_type": "cro_validate.classes.schema_classes.Schema",
			"data_type": "Object",
			"description": "Demo model 2."
		}
	}
	'''
	root = json.loads(json_str)
	DefinitionApi.from_json_dict(root)


def test__definition_version__compare_versions():
	# Verify compare_versions
	register()
	assert DefinitionApi.compare_versions('v0', 'v1') == -1
	assert DefinitionApi.compare_versions('v1', 'v1') == 0
	assert DefinitionApi.compare_versions('v2', 'v1') == 1


def test__definition_version__before_base():
	# Verify requesting version before base throws exception
	register()
	try:
		DefinitionApi.get('TestModel2', version='v0')
		assert False
	except Exception as ex:
		assert ExceptionApi.is_internal_error(ex) is True


def test__definition_version__after_final():
	# Verify requesting version after final throws exception
	register()
	try:
		DefinitionApi.get('TestModel2', version='v3')
		assert False
	except Exception as ex:
		assert ExceptionApi.is_internal_error(ex) is True


def test__definition_version__has_version():
	# Version v1 exists
	register()
	d = DefinitionApi.get('TestModel', version='v1')
	assert d.version == 'v1'


def test__latest_version__add_field():
	# Latest version should have c
	register()
	v = {'a':True, 'd': True}
	result = DefinitionApi.validate_input('TestModel', v)
	assert 'c' in result['TestModel']


def test__latest_version__mutate_field_v1():
	# Latest version should have d w/definition set to a
	register()
	d = DefinitionApi.get('TestModel', version='v1')
	assert d.list_fields()['d'].definition_name == 'b'


def test__latest_version__mutate_field():
	# Latest version should have d w/definition set to a
	register()
	d = DefinitionApi.get('TestModel')
	assert d.list_fields()['d'].definition_name == 'a'


def test__latest_version__rename_field():
	# Latest version should not have e and should have f
	register()
	d = DefinitionApi.get('TestModel')
	fields = d.list_fields()
	assert 'e' not in fields
	assert 'f' in fields


def test__latest_version__final_version_before_latest():
	# Test final_version
	register()
	try:
		DefinitionApi.get('TestModel2', version='v2')
		DefinitionApi.get('TestModel2')
		assert False
	except Exception as ex:
		assert ExceptionApi.is_internal_error(ex) is True


def test__base_version__has_no_c():
	# Base version should not have c
	register()
	v = {'a':True}
	result = DefinitionApi.validate_input('TestModel', v, version='base')
	assert 'c' not in result['TestModel']


def test__target_version__remove_field():
	# v2 should not have b
	register()
	v = {'a':True, 'd': True}
	result = DefinitionApi.validate_input('TestModel', v, version='v2')
	assert 'b' not in result['TestModel']


def test_version__base_version_correct():
	# Base version v0 should be returned & base version 'base' should also
	register()
	d = DefinitionApi.get('TestModel', version='v0')
	assert d.get_version() == 'v0'
	d = DefinitionApi.get('TestModel', version='base')
	assert d.get_version() == 'v0'


def test_version__version_correct():
	# Specified version v1 should be returned
	register()
	d = DefinitionApi.get('TestModel', version='v1')
	assert d.get_version() == 'v1'


def test_version__implicit_version_correct():
	# Requesting version 1.2 should return v1.2 (implicit version)
	register()
	d = DefinitionApi.get('TestModel', version='v1.2')
	assert d.get_version() == 'v1.2'


def test_version__latest_version_correct():
	# Requesting latest version should return v2
	register()
	d = DefinitionApi.get('TestModel')
	assert d.get_version() == 'v3'


def test_version__definition_has_version():
	# TestModel2 v1& v2 should exist, v0 & v3 should not
	register()
	assert DefinitionApi.definition_has_version('TestModel2', 'v0') is False
	assert DefinitionApi.definition_has_version('TestModel2', 'v1') is True
	assert DefinitionApi.definition_has_version('TestModel2', 'v2') is True
	assert DefinitionApi.definition_has_version('TestModel2', 'v3') is False


def test_version__invalid_version_throws():
	# Invalid version should throw ex
	register()
	try:
		d = DefinitionApi.get('TestModel', version='v1000')
		assert False
	except Exception as ex:
		assert ExceptionApi.is_internal_error(ex) is True


def test_version__mutation_v0_v1():
	# Mutation from v0 to v1 success
	register()
	v = {'a':True}
	result = DefinitionApi.mutate_input_version('TestModel', v, src_version='v0', target_version='v1')
	assert 'd' in result['TestModel']


def test_version__mutation_v1_v0():
	# Mutation from v1 to v0 success
	register()
	v = {'a':True, 'd': True}
	result = DefinitionApi.mutate_input_version('TestModel', v, src_version='v1', target_version='v0')
	assert 'd' not in result['TestModel']


def test_version__mutation_v0_v0():
	# Mutation from v0 to v0 success
	register()
	v = {'a':True}
	result = DefinitionApi.mutate_input_version('TestModel', v, src_version='v0', target_version='v0')
	assert 'd' not in result['TestModel']


def test_version__mutation_v0_v2():
	# Mutation from v0 to v2 success
	register()
	v = {'a':True}
	result = DefinitionApi.mutate_input_version('TestModel', v, src_version='v0', target_version='v2')
	assert 'd' in result['TestModel']
	definition = DefinitionApi.get('TestModel', version='v2')
	fields = definition.list_fields()
	assert fields['d'].definition_name == 'a'

