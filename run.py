import os

from wsgi_static_middleware import StaticMiddleware

from divo_framework.main import Framework
from views import routes
from components.front_controllers import front_controllers

BASE_DIR = os.path.dirname(__name__)
STATIC_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]

# Create WSGI-app object
app = Framework(routes, front_controllers)
app_static = StaticMiddleware(app,
                              static_root='staticfiles',
                              static_dirs=STATIC_DIRS)
