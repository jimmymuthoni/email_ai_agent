import os,yaml

def load_config(config_path:str = None):
    """function to get all configurations and load them"""
    if config_path is None:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(BASE_DIR,"config","config.yaml")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError (f"configurationfile not found: {config_path}")
    
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)