import json
from wg_config import config_file_path

class PluginEnvironment:
	def __init__(self, data, environment_name=None):
		self.data = data

		if environment_name:
			self.environment_name = environment_name
		else:
			self.environment_name = self.get_default_environment()

	def get_default_environment(self):
		environments = self.get_environments()

		for environment_name, environment in environments.iteritems():
			if environment.get('default'):
				return environment_name

		raise PluginEnvironmentException('No default environment was found')

	def get_all_plugin_contexts(self):
		plugins = self.get_environment_plugins()

		plugin_contexts = []

		for plugin_name in plugins.keys():
			context = self.get_plugin_context(plugin_name)
			plugin_contexts.append(context)

		return plugin_contexts

	def get_plugin_context(self, plugin_name):
		context = {}

		environment = self.get_environment()
		plugin = self.get_plugin(plugin_name)

		context['plugin_name'] = plugin_name
		context['plugin_id'] = plugin['id']
		context['namespace'] = plugin['namespace']
		context['route'] = plugin['route']
		context['api_endpoint'] = environment['api_endpoint']
		context['access_token'] = environment['access_token']

		return context

	def get_plugin(self, plugin_name):
		plugins = self.get_environment_plugins()

		try:
			return plugins[plugin_name]
		except KeyError:
			raise PluginEnvironmentException("Plugin not found: " + plugin_name)

	def get_environment_plugins(self):
		environment = self.get_environment()

		return environment['plugins']

	def get_environment(self):
		environments = self.get_environments()

		try:
			return environments[self.environment_name]
		except KeyError:
			raise PluginEnvironmentException("Environment not found: " + self.environment_name)

	def get_environments(self):
		return self.data

class PluginEnvironmentException(Exception):
	pass

def make_environment(environment_name=None):

	data = read_json_config_file()

	return PluginEnvironment(data, environment_name)

def read_json_config_file():
	try:
		with open(config_file_path) as json_file:
			return json.load(json_file)
	except IOError:
		raise PluginEnvironmentException('Config file not found: ' + config_file_path)