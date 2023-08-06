import cro_validate.api.configuration_api as ConfigApi


def resolve_definition_name(definitions, definition_name):
	return ConfigApi.get_definition_name_resolver().resolve(definitions, definition_name)

def resolve_parameter(parameters, parameter_name):
	return ConfigApi.get_parameter_name_resolver().resolve(parameters, parameter_name)