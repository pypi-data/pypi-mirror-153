def initialize():
	import cro_validate.classes.exception_classes as Exceptions
	import cro_validate.classes.example_generator_classes as Examples
	import cro_validate.classes.name_resolver_classes as NameResolvers
	import cro_validate.classes.name_strategy_classes as NameStrategies
	import cro_validate.classes.definition_classes as Definitions
	from cro_validate.classes.configuration_classes import Config

	Config.exception_factory = Exceptions.DefaultExceptionFactory()
	Config.example_generator_factory = Examples.DefaultExampleGeneratorFactory()
	Config.default_examples_provider = Examples.DefaultExamplesProvider()
	Config.definition_name_resolver = NameResolvers.DefaultNameResolver()
	Config.parameter_name_resolver = NameResolvers.DefaultNameResolver()
	Config.definition_name_strategy = NameStrategies.DefaultDefinitionNameStrategy()
	Config.instantiate_value_provider = Definitions.InstantiateValueProvider()

initialize()