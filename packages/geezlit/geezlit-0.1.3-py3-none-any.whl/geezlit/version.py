_MAJOR = "0"
_MINOR = "1"
# On main and in a nightly release the patch should be one ahead of the last
# released build.
_PATCH = "3"
# This is mainly for nightly builds which have the suffix ".dev$DATE". See
# https://semver.org/#is-v123-a-semantic-version for the semantics.
_SUFFIX = ""

VERSION_SHORT = "{0}.{1}".format(_MAJOR, _MINOR)
VERSION = "{0}.{1}.{2}{3}".format(_MAJOR, _MINOR, _PATCH, _SUFFIX)


__title__ = "geezlit"
__version__ = VERSION
__description__ = "Ge'ez Transliteration"
__author__ = "Fitsum Gaim"
__author_email__ = "fitsum@geezlab.com"
__copyright__ = "2022 Fitsum Gaim"
__license__ = "Apache 2.0"
__url__ = "https://github.com/fgaim/geezlit"
