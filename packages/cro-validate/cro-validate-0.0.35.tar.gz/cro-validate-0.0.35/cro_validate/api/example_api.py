import cro_validate.api.configuration_api as ConfigApi

def get_example_generator(definition, **kw):
	generator = ConfigApi.get_example_generator_factory().create(definition, **kw)
	return generator

def get_default_examples(definition, **kw):
	return ConfigApi.get_default_examples_provider().get_examples(definition, **kw)