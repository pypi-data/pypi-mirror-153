from cro_validate.classes.util_classes import Empty


def recurse_definition(
			definition,
			fqn,
			definition_field_name,
			parent_value,
			value,
			cb,
			case_sensitive=True,
			ignore_unknown_inputs=False,
			version=Empty,
			**kw
		):
	definition = get(definition, version=version)
	if fqn is None:
		fqn = definition.get_name()
	if definition_field_name is None:
		definition_field_name = definition.get_name()
	child_kw = cb(
			definition,
			fqn,
			definition_field_name,
			parent_value,
			value,
			**kw
		)
	if value is None:
		return
	if definition.get_data_type() == DataType.Array:
		i = 0
		for item in value:
			recurse_definition(
					definition.get_data_format(),
					NameUtil.append_index(fqn, i),
					definition_field_name,
					value,
					item,
					cb,
					case_sensitive=case_sensitive,
					ignore_unknown_inputs=ignore_unknown_inputs,
					version=version,
					**child_kw
				)
			i = i + 1
	elif definition.get_data_type() == DataType.Object:
		fields = definition.list_fields()
		field_input_names = {fields[k].input_name: k for k in fields}
		if case_sensitive is False:
			fields = {k.lower(): fields[k] for k in fields}
		for input_name in list_obj_fields(value):
			if input_name not in field_input_names:
				if ignore_unknown_inputs is True:
					continue
			field_name = field_input_names[input_name]
			field = fields[field_name]
			output_name = field_name
			if field.output_name is not None:
				output_name = field.output_name
			field_fqn = NameUtil.concat(fqn, output_name)
			if case_sensitive is False:
				field_name = field_name.lower()
			if field_name not in fields:
				if ignore_unknown_inputs is True:
					continue
				raise Exceptions.InputError(field_fqn, 'Unknown field.')
			recurse_definition(
					field.definition_name,
					field_fqn,
					output_name,
					value,
					get_obj_field_value(value, input_name),
					cb,
					case_sensitive=case_sensitive,
					ignore_unknown_inputs=ignore_unknown_inputs,
					version=version,
					**child_kw
				)