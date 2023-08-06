import shutil

ENV_VAR_PREFIX = 'NEXUS3'
TTY_MAX_WIDTH = shutil.get_terminal_size().columns

# see cli.util.get_client()
REQUIRED_NEXUS_OPTIONS = ['PASSWORD', 'USERNAME', 'URL']
OPTIONAL_NEXUS_OPTIONS = ['API_VERSION', 'X509_VERIFY']
