import json

class ConfigLoader:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Loads the configuration from a JSON file."""
        with open(self.config_file, 'r') as file:
            config = json.load(file)
        return config

    def get_all_dataset_names(self):
        """Returns a list of all dataset names (IDs)."""
        return [dataset['id'] for dataset in self.config['datasets']]
    
    def get_config_by_id(self, dataset_id):
        """Returns the configuration for a specific dataset identified by dataset_id."""
        for dataset in self.config['datasets']:
            if dataset['id'] == dataset_id:
                return dataset
        raise ValueError(f"Dataset with id '{dataset_id}' not found.")
