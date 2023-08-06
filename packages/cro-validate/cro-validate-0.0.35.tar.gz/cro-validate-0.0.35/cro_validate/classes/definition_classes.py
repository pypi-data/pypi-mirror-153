import importlib, collections

from enum import Enum
from cro_validate.enum import DataType, VersionMutationType, ValidationMode
from cro_validate.classes.configuration_classes import Config
import cro_validate.classes.parameter_classes as Parameters
import cro_validate.classes.schema_classes as Schemas
import cro_validate.classes.name_strategy_classes as NameStrategies
import cro_validate.classes.util_classes as Utils


def instantiate_class(fqn, *args, **kw):
	module_name, class_name = Utils.ClassName.class_fqn_parts(fqn)
	if module_name == 'builtins' and class_name == 'NoneType':
		return None
	module = importlib.import_module(module_name)
	_class = getattr(module, class_name)
	if isinstance(_class, type(Enum)):
		result = _class[args[0]]
	else:
		result = _class(*args, **kw)
	return result


class Meta:
	def initialize(self, definition, **kw):
		raise NotImplementedError()


class DefaultDefinitionMeta(Meta):
	component_name_strategy = NameStrategies.DefaultComponentNameStrategy()
	schema_name = None
	component_name = None

	def __init__(self, component_name_strategy=Utils.Empty):
		if not Utils.Empty.isempty(component_name_strategy):
			self.component_name_strategy = component_name_strategy

	def initialize(self, definition, component_name_suffix='Model', display_name=None):
		if definition.is_object():
			self.schema_name = definition.data_format.model_name
			self.component_name = self.schema_name
		elif definition.is_array():
			self.component_name = definition.data_format
		else:
			self.component_name = self.component_name_strategy.create_name(definition, component_name_suffix, display_name)


class InstantiateValueProvider:
	def __init__(self):
		pass

	def __call__(self, fqn, field_name, definition, data_type, data_format):
		try:
			if field_name is None:
				field_name = definition.get_name()
			if fqn is None:
				fqn = field_name
			if definition.is_object() is True:
				result = Parameters.Index()
				fields = definition.list_fields()
				for k in fields:
					f = fields[k]
					field_definition = Index.get(
							f.definition_name,
							version=definition.version
						)
					if Utils.Empty.isempty(f.default_value) is not True:
						result[k] = f.default_value
						continue
					field_fqn = Config.definition_name_strategy.get_fqn(fqn, k)
					result[k] = Config.instantiate_value_provider(
							field_fqn,
							k,
							field_definition,
							field_definition.get_data_type(),
							field_definition.get_data_format()
						)
				return result
			if definition.has_default_value() is True:
				return definition.get_default_value()
			if definition.is_array():
				return []
			if definition.is_nullable() is True:
				return None
			if data_type is DataType.Integer:
				return 0
			if data_type is DataType.String:
				return ''
			if data_type is DataType.Float:
				return 0.0
			if data_type is DataType.Boolean:
				return False
		except Exception as ex:
			raise Config.exception_factory.create_internal_error(
					fqn,
					'Failed to instantiate.',
					ex
				)
		raise Config.exception_factory.create_internal_error(
				fqn,
				"This default value provider doesn't support {0}.".format(data_type)
			)


class Definition:
	name = None
	aliases = []
	description = ''
	data_type = DataType.String
	data_format = None
	default_value = Utils.Empty
	examples = None
	nullable = False
	deprecated = False
	internal = False
	rules = []
	base_version = 'base'
	final_version = None
	version_conversion = None
	mutations = None
	meta = DefaultDefinitionMeta()

	def to_json_dict(self):
		# TODO: Refresh (broken) or delete this functionality.
		def _is_default(name, value):
			class_value = getattr(self.__class__, name)
			if class_value == value:
				return True
			return False
		def _set(target, name, value):
			if _is_default(name, value):
				return
			target[name] = value
		fmt = None
		if self.data_format is not None:
			if isinstance(self.data_format, Enum):
				fmt = self.data_format.name
			elif isinstance(self.data_format, Schemas.Schema):
				fmt = self.data_format.to_json_dict()
			elif isinstance(self.data_format, set):
				fmt = [f for f in self.data_format]
				fmt.sort()
			else:
				fmt = self.data_format
		fmt_type = Utils.ClassName.class_fqn(self.data_format)
		default_value_type = Utils.ClassName.class_fqn(self.default_value)
		aliases = [a for a in self.aliases]
		aliases.sort()
		result = {}
		_set(result, 'aliases', aliases)
		_set(result, 'description', self.description)
		_set(result, 'data_type', self.data_type.name)
		_set(result, 'data_format', fmt)
		_set(result, 'default_value', self.default_value)
		_set(result, 'examples', self.examples)
		_set(result, 'nullable', self.nullable)
		_set(result, 'deprecated', self.deprecated)
		_set(result, 'internal', self.internal)
		_set(result, 'rules', [{'type':Utils.ClassName.class_fqn(r), 'config':r.to_json_dict()} for r in self.rules])
		types = {
				'default_value': default_value_type,
				'data_format': fmt_type
			}
		result = {k: result[k] for k in result if not _is_default(k, result[k])}
		for k in types:
			t = types[k]
			if k in result:
				result[k + '_type'] = t
		return result

	def __init__(
				self,
				name,
				aliases,
				description,
				data_type,
				data_format,
				default_value,
				examples,
				nullable,
				deprecated,
				internal,
				rules,
				base_version,
				final_version,
				version,
				version_conversion,
				mutations,
				meta
			):
		def _set_member(name, value):
			if Utils.Empty.isempty(value):
				return
			setattr(self, name, value)
		_set_member('name', name)
		_set_member('aliases', aliases)
		_set_member('description', description)
		_set_member('data_type', data_type)
		_set_member('data_format', data_format)
		_set_member('default_value', default_value)
		_set_member('examples', examples)
		_set_member('nullable', nullable)
		_set_member('deprecated', deprecated)
		_set_member('internal', internal)
		_set_member('rules', rules)
		_set_member('base_version', base_version)
		_set_member('final_version', final_version)
		self.version = version  # mandatory
		_set_member('version_conversion', version_conversion)
		_set_member('mutations', mutations)
		_set_member('meta', meta)
		# Name
		######
		self.name = Config.definition_name_strategy.create_name(self, self.name)
		if self.name is None:
			Config.exception_factory.create_input_error(
					'<unset>', 'Definition name cannot be None (description={0})'.format(self.description)
				)
		# Aliases
		#########
		if isinstance(aliases, str):
			self.aliases = {aliases}
		# Nullable
		##########
		if self.default_value is None:
			self.nullable = True
		# Default Value
		###############
		if Utils.Empty.isempty(self.default_value):
			if self.nullable is True:
				self.default_value = None
		# Data Format
		#############
		if self.is_object() and isinstance(self.data_format, str):
			format_definition = Index.get(self.data_format)
			self.data_format = format_definition.data_format
		elif self.data_type is DataType.OneOf:
			pass
		# Validator
		###########
		if self.is_object():
			self.input_validator = self._get_obj_validator(ValidationMode.Input)
			self.output_validator = self._get_obj_validator(ValidationMode.Output)
		elif self.is_array():
			self.input_validator = self._validate_array
			self.output_validator = self._validate_array
		else:
			self.input_validator = self._assign_value
			self.output_validator = self._assign_value
		# Examples
		##########
		if not self.examples:
			self.examples = Config.default_examples_provider.get_examples(self)
		if not self.is_object() and not self.is_array():
			if not self.examples:
				raise Config.exception_factory.create_input_error(self.name, 'Missing examples')
		# Meta
		######
		self.meta.initialize(self)

	def _get_obj_validator(self, mode):
		model_validator = Schemas.ModelValidator(self.data_format, self.get_version(), mode)
		validator = Schemas.Validator(self.name, model_validator)
		return validator

	def _validate_array(
				self,
				results,
				field_fqn,
				field_name,
				definition,
				value,
				mode,
				**rules_kw):
		if isinstance(value, list):
			pass
		elif isinstance(value, set):
			value = [v for v in value]
		else:
			raise Config.exception_factory.create_input_error(field_fqn, 'Expected array, received: {0}'.format(type(value)))
		items = []
		i = 0
		for entry in value:
			item = Index.validate(
					validated=None,
					field_fqn=field_fqn + '[' + str(i) + ']',
					field_name=field_name,
					definition_or_name=self.data_format,
					value=entry,
					version=self.get_version(),
					mode=mode,
					**rules_kw
				)
			items.append(item[field_name])
			i = i + 1
		results[field_name] = items

	def _assign_value(
				self,
				results,
				field_fqn,
				field_name,
				definition,
				value,
				mode,
				**rules_kw):
		results[field_name] = value

	def validate(
				self,
				results,
				field_fqn,
				field_name,
				definition,
				value,
				mode,
				**rules_kw
			):
		'''
		The validate func
		'''
		validator = self.input_validator
		if mode is ValidationMode.Output:
			validator = self.output_validator
		try:
			results = Parameters.Index.ensure(results)
			if not validator:
				raise Config.exception_factory.create_internal_error(self.name, "Missing validator.")
			if field_name is None:
				field_name = self.name
			if field_fqn is None:
				field_fqn = field_name
				if self.data_type == DataType.Object:
					field_fqn = validator.model_validator.name
			if value is None:
				if self.nullable is True:
					results[field_name] = None
					return
				else:
					raise Config.exception_factory.create_input_error(field_fqn, 'Not nullable.')
			results[field_name] = value
			Index._eval_data_type_rules(
					results,
					field_fqn,
					field_name,
					self,
					**rules_kw
				)
			Index._eval_data_format_rules(
					results,
					field_fqn,
					field_name,
					self,
					**rules_kw
				)
			validator(
					results,
					field_fqn,
					field_name,
					self,
					results[field_name],
					mode,
					**rules_kw
				)
			for rule in self.rules:
				results[field_name] = rule.execute(field_fqn, results[field_name], **rules_kw)
			return results
		except Exception as ex:
			if self.internal:
				raise Config.exception_factory.create_internal_error(ex.source, ex.message)
			else:
				raise ex

	def has_default_value(self):
		if Utils.Empty.isempty(self.default_value):
			return False
		return True

	def get_default_value(self, fqn=None):
		if fqn is None:
			fqn = self.name
		if self.is_array() is True:
			if self.is_nullable() is True:
				return None
			return []
		if self.is_object() is True:
			if self.is_nullable() is True:
				return None
			result = Parameters.Index()
			fields = self.list_fields()
			for k in fields:
				f = fields[k]
				field_definition = Index.get(f.definition_name, version=self.version)
				if field_definition.has_default_value() is not True and field_definition.is_primitive() is True:
					field_fqn = Config.definition_name_strategy.get_fqn(fqn, k)
					raise Config.exception_factory.create_internal_error(field_fqn, 'No default value configured')
				result[k] = field_definition.get_default_value()
			return result
		if not self.has_default_value():
			raise Config.exception_factory.create_internal_error(fqn, 'No default value configured')
		return self.default_value

	def get_name(self):
		return self.name

	def get_version(self):
		return self.version

	def get_version_conversion(self):
		return self.version_conversion

	def get_base_version(self):
		return self.base_version

	def get_final_version(self):
		return self.final_version

	def get_mutations(self):
		return self.mutations

	def get_data_type(self):
		return self.data_type

	def get_data_format(self):
		return self.data_format

	def get_description(self, delim=' ', cat_rules=False):
		result = self.description
		if cat_rules is True:
			if self.rules is not None and len(self.rules) > 0:
				result = result + delim + delim.join([rule.get_description() for rule in self.rules])
		return result

	def get_aliases(self):
		return self.aliases

	def is_array(self):
		if self.data_type == DataType.Array:
			return True
		return False

	def is_object(self):
		if self.data_type == DataType.Object:
			return True
		return False

	def is_one_of(self):
		if self.data_type == DataType.OneOf:
			return True
		return False

	def is_primitive(self):
		if self.is_object() or self.is_array():
			return False
		return True

	def is_internal(self):
		return self.is_internal

	def is_nullable(self):
		return self.nullable

	def is_deprecated(self):
		return self.deprecated

	def is_obsolete(self):
		if self.final_version is not None:
			return True
		return False

	def list_fields(self):
		if self.data_type is not DataType.Object:
			return {}
		model = self.data_format.model
		if model is None:
			raise Config.exception_factory.create_internal_error(self.data_format.model_name, 'Missing model')
		fields = {}
		for k in model:
			f = model[k]
			if f.input_name is None:
				f.input_name = k
			fields[k] = f
		return fields

	def get_field(self, k):
		if self.data_type is not DataType.Object:
			return None
		model = self.data_format.model
		if model is None:
			raise Config.exception_factory.create_internal_error(self.data_format.model_name, 'Missing model')
		if k not in model:
			raise Config.exception_factory.create_internal_error(self.data_format.model_name, 'Unkown field: {0}'.format(k))
		field = model[k]
		if field.input_name is None:
			field.input_name = k
		return field

	def get_boundaries(self):
		result = []
		for rule in self.rules:
			result.extend(rule.get_boundaries())
		if self.is_nullable() is not True:
			result.append(None)
		if self.is_object() is True:
			result.append([])
		if self.is_array() is True:
			result.append({})
		return result


class DefinitionJsonDeserializer:
	def __init__(self, root):
		self.namespace = {k:k for k in root}
		#for k in root:
			#if 'aliases' not in root[k]:
			#	continue
			#for k1 in root[k]['aliases']:
			#	if k1 in self.namespace:
			#		raise Config.exception_factory.create_internal_error(k1, 'Input definition already exists.')
			#	self.namespace[k1] = k
		self.root = root

	def _get_dict_value(self, idx, k, default_value=Utils.Empty):
		if k in idx:
			return idx[k]
		return default_value

	def _set(self, src, tgt, k, default_value=Utils.Empty):
		v = self._get_dict_value(src, k, default_value)
		if Utils.Empty.isempty(v):
			return
		if k == 'is_internal':
			k = 'internal'
		tgt[k] = v

	def _get_root_obj(self, k):
		root_k = self.namespace[k]
		result = self.root[root_k]
		return result

	def _get_definition_name(self, k):
		if k in self.namespace:
			result = self.namespace[k]
			return result
		d = Index.get(k)
		return d.get_name()

	def _deserialize_schema_field(self, name, obj):
		kw = {}
		if 'default_value' in obj:
			#if obj['default_value_type'] == '<definition_name>':
			#	default_value_definition_name = obj['default_value']
			#	if not Index.exists(default_value_definition_name):
			#		dependent_definition_profile = self.deserialize(default_value_definition_name)
			#		Index.register_definition(**dependent_definition_profile)
			#	kw['default_value'] = instantiate_class(obj['default_value_type'], obj['default_value'])
			#elif obj['default_value_type'] != 'cro_validate.classes.util_classes.Empty':
			#	kw['default_value'] = instantiate_class(obj['default_value_type'], obj['default_value'])
			kw['default_value'] = instantiate_class(obj['default_value_type'], obj['default_value'])
		kw['definition_name'] = name
		if 'definition_name' in obj and obj['definition_name'] is not None:
			kw['definition_name'] = obj['definition_name']
		definition_name = self._get_definition_name(kw['definition_name'])
		if not Index.exists(definition_name):
			dependent_definition_profile = self.deserialize(definition_name)
			Index.register_definition(**dependent_definition_profile)
		self._set(obj, kw, 'ignored')
		self._set(obj, kw, 'input_name', default_value=name)
		self._set(obj, kw, 'output_name')
		self._set(obj, kw, 'required')
		self._set(obj, kw, 'unvalidated')
		field = Schemas.Field(**kw)
		return field

	def _deserialize_schema(self, obj, name):
		kw = {}
		self._set(obj, kw, 'allow_unknown_fields')
		self._set(obj, kw, 'case_sensitive')
		self._set(obj, kw, 'display_name')
		self._set(obj, kw, 'load_defaults')
		self._set(obj, kw, 'model')
		self._set(obj, kw, 'dependency_resolver')
		self._set(obj, kw, 'return_unknown_fields')
		kw['model_name'] = name
		model = {}
		field_init_actions = []
		if 'field_init_actions' in obj:
			for entry in obj['field_init_actions']:
				init_action_kw = {}
				if 'kw' in entry:
					init_action_kw = entry['kw']
				init_action_class_name = entry['type']
				init_action = instantiate_class(init_action_class_name, **init_action_kw)
				field_init_actions.append(init_action)
		kw['field_init_actions'] = field_init_actions
		if 'dependency_resolver' in obj:
			resolver_class_name = obj['dependency_resolver']['type']
			resolver_kw = {}
			if 'kw' in obj['dependency_resolver']:
				resolver_kw = obj['dependency_resolver']['kw']
			resolver = instantiate_class(resolver_class_name, **resolver_kw)
			kw['dependency_resolver'] = resolver
		if 'inherits' in obj:
			for inherited_definition_name in obj['inherits']:
				if not Index.exists(inherited_definition_name):
					dependent_definition_profile = self.deserialize(inherited_definition_name)
					Index.register_definition(**dependent_definition_profile)
				#parent_definition = Index.get(inherited_definition_name)
				#inherited_fields = parent_definition.list_fields()
				#for field_name in inherited_fields:
				#	model[field_name] = inherited_fields[field_name]
			kw['inherits'] = obj['inherits']
		if 'model' in obj:
			for field_name in obj['model']:
				field = self._deserialize_schema_field(field_name, obj['model'][field_name])
				model[field_name] = field
		kw['model'] = model
		schema = Schemas.Schema(**kw)
		return schema

	def _deserialize_rule(self, obj):
		rule = instantiate_class(obj['type'], **obj['config'])
		return rule

	def _deserialize_version(self, obj):
		result = {}
		if 'mutations' in obj:
			mutations = []
			for mutation in obj['mutations']:
				action = mutation['action']
				action = VersionMutationType[action]
				description = None
				if 'description' in mutation:
					description = mutation['description']
				config = mutation['config']
				supported_mutations = {
						VersionMutationType.AddField,
						VersionMutationType.RemoveField,
						VersionMutationType.MutateField,
						VersionMutationType.RenameField
					}
				if action not in supported_mutations:
					raise Exception('Version Mutation Not Implemented: {0}'.format(action))
				mutations.append(Utils.VersionMutation(action, config, description))
				if 'definition_name' in config:
					definition_name = config['definition_name']
					if not Index.exists(definition_name):
						dependent_definition_profile = self.deserialize(definition_name)
						Index.register_definition(**dependent_definition_profile)
			result['mutations'] = mutations
		if 'conversion' in obj:
			config = obj['conversion']['config']
			type_fqn = obj['conversion']['type']
			conversion = instantiate_class(type_fqn, **config)
			result['conversion'] = conversion
		return result

	def deserialize(self, name):
		kw = {
			'name': Utils.Empty,
			'aliases': Utils.Empty,
			'description': Utils.Empty,
			'examples': Utils.Empty,
			'nullable': Utils.Empty,
			'deprecated': Utils.Empty,
			'internal': Utils.Empty,
			'data_type': Utils.Empty,
			'data_format': Utils.Empty,
			'default_value': Utils.Empty,
			'meta': Utils.Empty,
			'rules': Utils.Empty
		}
		obj = self._get_root_obj(name)
		# Data Format
		#############
		if 'data_type' in obj:
			kw['data_type'] = DataType[obj['data_type']]
		if 'data_format' in obj:
			if obj['data_format_type'] == 'cro_validate.classes.schema_classes.Schema':
				kw['data_format'] = self._deserialize_schema(obj['data_format'], name)
			else:
				kw['data_format'] = instantiate_class(obj['data_format_type'], obj['data_format'])
		# Default Value
		###############
		if 'default_value' in obj:
			if obj['default_value_type'] == 'builtins.NoneType':
				kw['default_value'] = None
			elif obj['default_value_type'] != 'cro_validate.classes.util_classes.Empty':
				kw['default_value'] = instantiate_class(obj['default_value_type'], obj['default_value'])
		# Rules
		#######
		if 'rules' in obj:
			rules = []
			for rule in obj['rules']:
				rule_obj = self._deserialize_rule(rule)
				rules.append(rule_obj)
			kw['rules'] = rules
		# Aliases
		#########
		if 'aliases' in obj:
			aliases = obj['aliases']
			if isinstance(aliases, str):
				aliases = {aliases}
			else:
				aliases = set(aliases)
			kw['aliases'] = aliases
		# Versions
		##########
		if 'base_version' in obj:
			kw['base_version'] = obj['base_version']
		if 'final_version' in obj:
			kw['final_version'] = obj['final_version']
		if 'base_version_conversion' in obj:
			config = obj['base_version_conversion']['config']
			type_fqn = obj['base_version_conversion']['type']
			kw['base_version_conversion'] = instantiate_class(type_fqn, **config)
		if 'versions' in obj:
			kw['versions'] = {}
			for version in obj['versions']:
				if Index.version_exists(version) != True:
					raise Config.exception_factory.create_internal_error(
							name,
							'Unkown version found during deserialization: {0}.'.format(version)
						)
				kw['versions'][version] = self._deserialize_version(obj['versions'][version])
		# Simple
		########
		kw['name'] = name
		self._set(obj, kw, 'description', '')
		self._set(obj, kw, 'examples', [])
		self._set(obj, kw, 'nullable', False)
		self._set(obj, kw, 'deprecated', False)
		self._set(obj, kw, 'is_internal', False)
		return kw


class Index:
	_idx = {}
	_data_type_rules = {}
	_data_type_rule_exceptions = set()
	_data_format_rules = {}
	_data_format_rule_exceptions = set()
	_versions = ['base']
	_versions_idx = {'base': 0}
	_versions_display_names = {'base': None}
	_json_dict = {}

	def _resolve_definition_name(definition_or_name, error_on_missing=True):
		definition_name = definition_or_name
		if isinstance(definition_or_name, Definition) is True:
			definition_name = definition_or_name.get_name()
		target_ns = Index._idx
		#if definition_name not in target_ns:
		#	target_ns = Index._json_dict
		resolved = Config.definition_name_resolver.resolve(target_ns, definition_name)
		if resolved is None and error_on_missing is True:
			raise Config.exception_factory.create_internal_error(
					definition_name,
					'Definition name resolution failed (Unknown definition name).'
				)
		return resolved

	def add_version(version, display_name):
		if version in Index._versions_idx:
			raise Config.exception_factory.create_internal_error(
					version,
					'Version already exists: {0}'.format(version)
				)
		if display_name is not None:
			if Index.get_version_by_display_name(display_name) is not None:
				raise Config.exception_factory.create_internal_error(
						version,
						'Version with display name already exists: {0}'.format(display_name)
					)
		latest_version = Index.get_latest_version()
		for k in Index._idx:
			Index._ensure_loaded(k)
			final_definition_version = Index.get_definition_final_version()
			if Index.compare_versions(final_definition_version, latest_version) < 0:
				continue
			latest_def = Index.get(k, version=latest_version)
			Index._idx[k][version] = latest_def
		Index._versions_idx[version] = len(Index._versions)
		Index._versions.append(version)
		Index._versions_display_names[version] = display_name

	def get_version_display_name(version):
		if version not in Index._versions_idx:
			raise Config.exception_factory.create_internal_error(
					version,
					'No such version: {0}'.format(version)
				)
		result = Index._versions_display_names[version]
		return result

	def get_version_by_display_name(display_name):
		for version in reversed(Index.list_versions()):
			n = Index._versions_display_names[version]
			if n == display_name:
				return version
		return None

	def list_versions():
		result = []
		result.extend(Index._versions)
		return result

	def get_latest_version():
		return Index._versions[-1]

	def get_first_version():
		return Index._versions[1]

	def version_exists(version):
		if version in Index._versions_idx:
			return True
		return False

	def list_definition_versions(definition_or_name, include_identical):
		base_definition = Index.get_definition_base_version(definition_or_name)
		base_definition_name = base_definition.get_name()
		Index._ensure_loaded(base_definition_name)
		versions = Index._idx[base_definition_name]
		if include_identical is True:
			result = [versions[v].get_version() for v in Index._versions if v in versions]
			return result
		unique = set()
		unique.add(base_definition.get_version())
		for version in versions:
			definition = versions[version]
			mutations = definition.get_mutations()
			if len(mutations) < 1:
				continue
			unique.add(definition.get_version())
		result = [versions[v].get_version() for v in Index._versions if v in unique]
		return result

	def get_definition_base_version(definition_or_name):
		resolved = Index._resolve_definition_name(definition_or_name)
		for version in Index._versions:
			Index._ensure_loaded(resolved)
			if version in Index._idx[resolved]:
				return Index._idx[resolved][version]
		raise Config.exception_factory.create_internal_error(
				resolved,
				'Definition version resolution failed (base version not found).'
			)

	def get_definition_final_version(definition_or_name):
		resolved = Index._resolve_definition_name(definition_or_name)
		for version in reversed(Index._versions):
			if version in Index._idx[resolved]:
				return Index._idx[resolved][version]
		raise Config.exception_factory.create_internal_error(
				resolved,
				'Definition version resolution failed (final version not found).'
			)

	def get_definition_previous_version(definition_or_name, version):
		versions = Index.list_definition_versions(definition_or_name, include_identical=True)
		i = len(versions) - 1
		while i > 1:
			if versions[i] == version:
				previous_version = versions[i-1]
				result = Index.get(definition_or_name, previous_version)
				return result
			i = i - 1
		resolved = Index._resolve_definition_name(definition_or_name)
		raise Config.exception_factory.create_internal_error(
				resolved,
				'No previous version found (version={0}).'.format(version)
			)

	def _ensure_loaded(definition_or_name):
		if isinstance(definition_or_name, Definition):
			return definition_or_name
		if Index._idx[definition_or_name] is not None:
			return Index._idx[definition_or_name]
		deserializer = DefinitionJsonDeserializer(Index._json_dict)
		profile = deserializer.deserialize(definition_or_name)
		Index.register_definition(**profile)
		return Index._idx[definition_or_name]

	def get(definition_or_name, version=Utils.Empty):
		definition_name = Index._resolve_definition_name(definition_or_name)
		if Utils.Empty.isempty(version) is not True:
			if version not in Index._versions:
				raise Config.exception_factory.create_internal_error(
						definition_name,
						'Unknown/unregistered version requested: {0}'.format(version)
					)
		versions = Index._ensure_loaded(definition_name)
		# Latest
		########
		if Utils.Empty.isempty(version) is True:
			latest_version = Index.get_latest_version()
			final_definition = Index.get_definition_final_version(definition_name)
			if Index.compare_versions(latest_version, final_definition.get_version()) == 1:
				raise Config.exception_factory.create_internal_error(
						definition_name,
						'Version requested after final version: {0}'.format(version)
					)
			return final_definition
		# Base
		######
		if version == 'base':
			base_version_definition = Index.get_definition_base_version(definition_name)
			return base_version_definition
		# Specified
		###########
		base_definition = Index.get_definition_base_version(definition_name)
		final_definition = Index.get_definition_final_version(definition_name)
		if Index.compare_versions(version, base_definition.get_version()) == -1:
			raise Config.exception_factory.create_internal_error(
					definition_name,
					'Version requested falls before base version: {0}'.format(version)
				)
		if Index.compare_versions(version, final_definition.get_version()) == 1:
			raise Config.exception_factory.create_internal_error(
				definition_name,
				'Version requested falls after final version: {0}'.format(version)
			)

		return versions[version]

	def instantiate(
				fqn,
				field_name,
				definition_or_name,
				version=Utils.Empty,
				validate=True,
				rules_kw={},
				**initial_values
			):
		definition = Index.get(definition_or_name, version)
		if field_name is None:
			field_name = definition.get_name()
		if fqn is None:
			fqn = field_name
		value = Config.instantiate_value_provider(
				fqn,
				field_name,
				definition,
				definition.get_data_type(),
				definition.get_data_format()
			)
		if definition.is_object() is True:
			value.update(initial_values)
		if validate is True:
			result = Index.validate(
					None,
					fqn,
					field_name,
					definition,
					value,
					version,
					ValidationMode.Input,
					**rules_kw
				)
			return result[definition.get_name()]
		return value

	def exists(definition_name):
		resolved = Index._resolve_definition_name(
				definition_name,
				error_on_missing=False
			)
		if resolved is None:
			return False
		return True

	def as_dict():
		return Index._idx

	def to_json_dict():
		aliases = set()
		keys = [k for k in Index.as_dict()]
		keys.sort()
		for k in keys:
			definition = Index.get(k)
			aliases.update(definition.aliases)
		result = {k:Index.get(k).to_json_dict() for k in keys if k not in aliases}
		return result

	def from_json_dict(root):
		new_entries = {}
		for k in root:
			new_entries[k] = root[k]
			if 'aliases' in root[k]:
				if isinstance(root[k]['aliases'], list):
					new_entries.update({k1: root[k] for k1 in root[k]['aliases']})
				else:
					alias = str(root[k]['aliases'])
					new_entries[alias] = root[k]
		for k in new_entries:
			if k in Index._json_dict or k in Index._idx:
				raise Config.exception_factory.create_internal_error(
						k,
						'Definition registration collision (already defined).'
					)
		Index._json_dict.update(new_entries)
		for k in new_entries:
			Index._idx[k] = None


	def compare_versions(a, b):
		if a not in Index._versions_idx:
			raise Config.exception_factory.create_internal_error(
					'compare_versions',
					'Source version not found: {0}.'.format(a)
				)
		a_idx = Index._versions_idx[a]
		if b not in Index._versions_idx:
			raise Config.exception_factory.create_internal_error(
					'compare_versions',
					'Target version not found: {0}.'.format(b)
				)
		b_idx = Index._versions_idx[b]
		if a_idx < b_idx:
			return -1
		if a_idx == b_idx:
			return 0
		return 1

	def definition_has_version(definition_or_name, version):
		definition_name = definition_or_name
		if isinstance(definition_or_name, Definition) is True:
			definition_name = definition_or_name.get_name()
		base_definition = Index.get_definition_base_version(definition_name)
		final_definition = Index.get_definition_final_version(definition_name)
		if Index.compare_versions(base_definition.get_version(), version) == 1:
			return False
		if Index.compare_versions(final_definition.get_version(), version) == -1:
			return False
		return True

	def _mutate_model(base_model, mutations):
		# Init Mutation
		###############
		mutated_model = {}
		if isinstance(base_model, dict):
			for k in base_model:
				if k.startswith('_'):
					continue
				if isinstance(base_model[k], Schemas.Field):
					mutated_model[k] = base_model[k].copy()
				elif isinstance(base_model[k], type(None)):
					mutated_model[k] = Schemas.Field(input_name=k)
		else:
			for k in dir(base_model):
				if k.startswith('_'):
					continue
				v = getattr(base_model, k)
				if isinstance(v, Schemas.Field):
					mutated_model[k] = v.copy()
				elif isinstance(v, type(None)):
					mutated_model[k] = Schemas.Field(input_name=k)
		# Mutate
		########
		for mutation in mutations:
			if mutation.action == VersionMutationType.AddField:
				field = Schemas.Field(**mutation.config)
				field_name = field.input_name
				mutated_model[field_name] = field
			elif mutation.action == VersionMutationType.RemoveField:
				field = Schemas.Field(**mutation.config)
				del mutated_model[field.input_name]
			elif mutation.action == VersionMutationType.MutateField:
				old_field = mutated_model[mutation.config['field_name']]
				config = {
						k:mutation.config[k]
						for k in mutation.config
						if k != 'field_name'
					}
				new_field = Schemas.Field(
						input_name=old_field.input_name
					)
				new_field.mutate(**config)
				mutated_model[mutation.config['field_name']] = new_field
			elif mutation.action == VersionMutationType.RenameField:
				old_field_name = mutation.config['field_name']
				old_field = mutated_model[old_field_name]
				del mutated_model[old_field_name]
				mutated_model[mutation.config['new_field_name']] = old_field
		return mutated_model

	def _execute_field_init(model, field_init_actions):
		result = {}
		for field_name in model:
			field = model[field_name]
			for action in field_init_actions:
				field = action(field_name, field)
				if field is None:
					break  # omitted field
			if field is not None:
				result[field_name] = field
		return result

	def _get_inherited_fields(schema, version):
		result = {}
		for inherited_definition_name in schema.inherits:
			parent_definition = Index.get(inherited_definition_name, version)
			inherited_fields = parent_definition.list_fields()
			for field_name in inherited_fields:
				result[field_name] = inherited_fields[field_name]
		return result

	def _get_inherited_mutations(schema, version):
		result = []
		inherited_mutations = []
		for inherited_definition_name in schema.inherits:
			parent_definition = Index.get(inherited_definition_name, version)
			result.extend(parent_definition.get_mutations())
		return result

	def _extend_model(schema, cumulative_mutations, version):
		model = Index._get_inherited_fields(schema, version)
		for k in schema.model:
			model[k] = schema.model[k]
		model = Index._mutate_model(model, cumulative_mutations)
		model = Index._execute_field_init(model, schema.field_init_actions)
		return model

	t = 0

	def register_definition(
				name,
				aliases,
				description,
				data_type,
				data_format,
				default_value,
				examples,
				nullable,
				deprecated,
				internal,
				rules,
				meta,
				base_version=Utils.Empty,
				base_version_conversion=Utils.Empty,
				final_version=Utils.Empty,
				versions=Utils.Empty
			):
		if Utils.Empty.isempty(base_version) is True:
			base_version = 'base'
		definition_versions = {}
		latest_def_version = None
		if Utils.Empty.isempty(versions) is True:
			versions = {}
		cumulative_mutations = []
		mutated_data_format = data_format
		initial_version_index = Index._versions_idx[base_version]
		for version in Index._versions[initial_version_index:]:
			if Utils.Empty.isempty(final_version) is False:
				if Index.compare_versions(version, final_version) == 1:
					break
			mutations = []
			version_conversion = None
			if version in versions:
				if 'mutations' in versions[version]:
					mutations = versions[version]['mutations']
				if 'conversion' in versions[version]:
					version_conversion = versions[version]['conversion']
			cumulative_mutations.extend(mutations)
			if data_type == DataType.Object:
				mutated_data_format = data_format.copy()
				mutated_data_format.model = Index._extend_model(mutated_data_format, cumulative_mutations, version)
				inherited_mutations = Index._get_inherited_mutations(mutated_data_format, version)
				inherited_mutations.extend(mutations)
				mutations = inherited_mutations
			mutated_definition = Definition(
					name=name,
					aliases=aliases,
					description=description,
					data_type=data_type,
					data_format=mutated_data_format,
					default_value=default_value,
					examples=examples,
					nullable=nullable,
					deprecated=deprecated,
					internal=internal,
					rules=rules,
					base_version=base_version,
					final_version=final_version,
					version=version,
					version_conversion=version_conversion,
					mutations=mutations,
					meta=meta
				)
			definition_versions[version] = mutated_definition
			latest_def_version = mutated_definition
			if Utils.Empty.isempty(final_version) is False:
				if final_version == version:
					break
		names = set()
		names.add(name)
		if Utils.Empty.isempty(aliases):
			pass
		elif isinstance(aliases, str):
			names.add(aliases)
		else:
			names.update(aliases)
		#for entry in names:
		#	if entry not in Index._idx or Index._idx[entry] is None:
		#		continue
		#	raise Config.exception_factory.create_internal_error(
		#			entry,
		#			'Input definiton already exists.'
		#		)
		for entry in names:
			Index._idx[entry] = definition_versions
		return Index.get(name, version=final_version)

	def register_data_type_rule(data_type, rule, exceptions=[]):
		if data_type not in Index._data_type_rules:
			Index._data_type_rules[data_type] = []
		Index._data_type_rules[data_type].append(rule)
		Index._data_type_rule_exceptions.update(exceptions)

	def register_data_format_rule(data_format, rule, exceptions=[]):
		if data_format not in Index._data_format_rules:
			Index._data_format_rules[data_format] = []
		Index._data_format_rules[data_format].append(rule)
		Index._data_format_rule_exceptions.update(exceptions)

	def _eval_data_type_rules(
				results,
				field_fqn,
				field_name,
				definition,
				**rules_kw
			):
		data_type = definition.get_data_type()
		if data_type not in Index._data_type_rules:
			return
		if definition.get_name() in Index._data_type_rule_exceptions:
			return
		for rule in Index._data_type_rules[definition.get_data_type()]:
			results[field_name] = rule.execute(field_fqn, results[field_name], **rules_kw)

	def _eval_data_format_rules(
				results,
				field_fqn,
				field_name,
				definition,
				**rules_kw
			):
		data_format = definition.get_data_format()
		if not isinstance(data_format, collections.Hashable):
			# currently not supported; FUTURES
			return
		if data_format not in Index._data_format_rules:
			return
		if definition.get_name() in Index._data_format_rule_exceptions:
			return
		for rule in Index._data_format_rules[definition.get_data_format()]:
			results[field_name] = rule.execute(field_fqn, results[field_name], **rules_kw)

	def validate(
				validated,
				field_fqn,
				field_name,
				definition_or_name,
				value,
				version,
				mode,
				**rules_kw
			):
		definition = Index.get(definition_or_name, version)
		results = Parameters.Index.ensure(validated)
		definition.validate(
				results,
				field_fqn,
				field_name,
				definition,
				value,
				mode,
				**rules_kw
			)
		return results

	def mutate_input_version(
				validated,
				field_fqn,
				field_name,
				definition_or_name,
				value,
				src_version,
				target_version,
				skip_validation=False,
				**rules_kw
			):
		src_definition = Index.get(definition_or_name, src_version)
		target_definition = Index.get(definition_or_name, target_version)
		results = Parameters.Index.ensure(validated)
		results[src_definition.get_name()] = value
		src_index = Index._versions_idx[src_version]
		target_index = Index._versions_idx[target_version]
		versions = Index._idx[src_definition.get_name()]
		if skip_validation is False:
			Index.validate(results, field_fqn, field_name, src_definition, value, src_version, ValidationMode.Input, **rules_kw)
			value = results[src_definition.get_name()]
		if src_index < target_index:
			i = src_index
			last_version = None
			seen_conversions = set()
			while i < target_index:
				next_version = Index._versions[i]
				next_definition = Index.get(definition_or_name, next_version)
				i = i + 1
				last_version = next_definition.get_version()
				conversion = next_definition.get_version_conversion()
				if conversion is None:
					continue
				if conversion in seen_conversions:
					continue
				value = conversion.increment(field_fqn, next_definition, value)
				seen_conversions.add(conversion)
		else:
			i = src_index
			last_version = None
			seen_conversions = set()
			while i > target_index:
				prev_version = Index._versions[i]
				prev_definition = Index.get(definition_or_name, prev_version)
				i = i - 1
				if last_version == prev_definition.get_version():
					continue
				last_version = prev_definition.get_version()
				conversion = prev_definition.get_version_conversion()
				if conversion is None:
					continue
				if conversion in seen_conversions:
					continue
				value = conversion.decrement(field_fqn, prev_definition, value)
				seen_conversions.add(conversion)
		if src_version != target_version:
			results = {src_definition.get_name(): value}
			if skip_validation is False:
				results = Index.validate(results, field_fqn, field_name, target_definition, value, target_version, ValidationMode.Input, **rules_kw)
		return results

	def ensure_alias(name, alias):
		definition = Index.get(name)
		if alias not in Index._idx:
			Index._idx[alias] = definition

	def list_definitions():
		result = [k for k in Index._idx]
		result.sort()
		return result

	def clear():
		Index._idx = {}
		Index._data_type_rules = {}
		Index._data_type_rule_exceptions = set()
		Index._data_format_rules = {}
		Index._data_format_rule_exceptions = set()
		Index._versions = ['base']
		Index._versions_idx = {'base': 0}
		Index._json_dict = {}
