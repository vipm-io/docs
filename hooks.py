"""MkDocs hooks for dynamic configuration."""
from datetime import datetime


def on_config(config, **kwargs):
    """Update copyright year dynamically at build time."""
    current_year = datetime.now().year
    config['copyright'] = f'Copyright &copy; {current_year} VIPM Community Contributors'
    return config
