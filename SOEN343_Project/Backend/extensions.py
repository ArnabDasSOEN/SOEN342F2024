# extensions.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create the limiter instance without attaching it to any app yet
limiter = Limiter(key_func=get_remote_address)
