import json
import os

class Config:
	def __init__(self, config_path=None):
		self.config_path = config_path or self._get_default_config_path()
		self.settings = self._load_config()
		
	def _get_default_config_path(self):
		"""Get the default path to settings.json"""
		base_dir = os.path.dirname(os.path.abspath(__file__))
		project_dir = os.path.dirname(base_dir)
		return os.path.join(project_dir, "config", "settings.json")
	
	def _load_config(self):
		"""Load configuration from JSON file"""
		try:
			if os.path.exists(self.config_path):
				with open(self.config_path, 'r') as f:
					return json.load(f)
			else:
				# Return default config if file doesn't exist
				return self._get_default_settings()
		except Exception as e:
			print(f"Error loading config: {e}")
			return self._get_default_settings()
	
	def _get_default_settings(self):
		"""Return default settings if config file is missing"""
		return {
			"database": {
				"user_data_directory": "data/",
				"budget_db_name": "budget.db"
			},
			"display": {
				"terminal_width": 60,
				"currency_symbol": "₦"
			}
		}
	
	def get(self, key_path, default=None):
		"""Get a configuration value using dot notation"""
		keys = key_path.split('.')
		value = self.settings
		
		try:
			for key in keys:
				value = value[key]
			return value
		except (KeyError, TypeError):
			return default
	
	def save(self):
		"""Save current settings to file"""
		try:
			os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
			with open(self.config_path, 'w') as f:
				json.dump(self.settings, f, indent=2)
			return True
		except Exception as e:
			print(f"Error saving config: {e}")
			return False