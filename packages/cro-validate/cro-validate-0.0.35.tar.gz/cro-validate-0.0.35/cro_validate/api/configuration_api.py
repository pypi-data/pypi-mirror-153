from cro_validate.classes.configuration_classes import Config

def get_exception_factory():
	return Config.exception_factory


def set_exception_factory(f):
	Config.exception_factory = f


def get_definition_name_resolver():
	return Config.definition_name_resolver


def set_definition_name_resolver(r):
	Config.definition_name_resolver = r


def get_parameter_name_resolver():
	return Config.parameter_name_resolver


def set_parameter_name_resolver(r):
	Config.parameter_name_resolver = r


def get_example_generator_factory():
	return Config.example_generator_factory


def set_example_generator_factory(f):
	Config.example_generator_factory = f


def get_default_examples_provider():
	return Config.default_examples_provider


def set_default_examples_provider(p):
	Config.default_examples_provider = p


def set_definition_name_strategy(s):
	Config.definition_name_strategy = s


def get_definition_name_strategy():
	return Config.definition_name_strategy


def set_instantiate_value_provider(p):
	Config.instantiate_value_provider = p


def get_instantiate_value_provider():
	return Config.instantiate_value_provider