
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from serviceb_client.api.genres_api import GenresApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from serviceb_client.api.genres_api import GenresApi
from serviceb_client.api.lists_api import ListsApi
from serviceb_client.api.movies_api import MoviesApi
from serviceb_client.api.oauth2_api import Oauth2Api
from serviceb_client.api.users_api import UsersApi
