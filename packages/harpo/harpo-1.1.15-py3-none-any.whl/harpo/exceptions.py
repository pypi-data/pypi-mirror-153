import sys
from functools import wraps

from .log import get_logger


class HarpoException(Exception):
    """General Harpo Exception"""


# OS
class HarpoOSError(HarpoException):
    """General Harpo OS Error"""


class HarpoFileNotFound(HarpoOSError):
    """Harpo tried accessing a non-existent file"""


# Metadata
class HarpoMetadataException(HarpoException):
    """General metadata exception"""


class HarpoMetadataReadError(HarpoMetadataException):
    """General metadata error: READ"""


class HarpoMetadataWriteError(HarpoMetadataException):
    """General metadata error: WRITE"""


class HarpoMetadataVersionMismatch(HarpoMetadataReadError):
    """Harpo tried accessing metadata of unsupported format"""


class HarpoMetadataNotFound(HarpoMetadataReadError):
    """Failed to found Harpo metadata"""


class HarpoMetadataParsingError(HarpoMetadataReadError):
    """Unable to parse metadata"""


# Domain
class HarpoDomainException(HarpoException):
    """Harpo general domain exception"""


class HarpoDomainDoesntExist(HarpoDomainException):
    """Tried accessing domain, but domain wasn't found in metadata"""

    pass


class HarpoDomainAlreadyExists(HarpoDomainException):
    """Tried to create a new domain, but domain with the same name already exists in metadata"""


class HarpoDomainNotFound(HarpoDomainException):
    """Can't find domain in metadata"""


# User
class HarpoUserException(HarpoException):
    """Harpo general user exception"""


class HarpoUserAlreadyExists(HarpoUserException):
    """User already exists in metadata"""


class HarpoUserNotFound(HarpoUserException):
    """Can't find user in metadata"""


# Group
class HarpoGroupException(HarpoException):
    """Harpo general group exception"""


class HarpoGroupAlreadyExists(HarpoGroupException):
    """Group already exists in metadata"""


class HarpoGroupNotFound(HarpoGroupException):
    """Can't find group in metadata"""


# Key
class HarpoKeyException(HarpoException):
    """Harpo general key exception"""


class HarpoKeyNotFound(HarpoKeyException):
    """Key wasn't found in keystore"""


# Secret
class HarpoSecretException(HarpoException):
    """Harpo general secrets exception"""


class HarpoSecretBackendNotFound(HarpoSecretException):
    """Unsupported secrets backend"""


class HarpoSecretBackendException(HarpoSecretException):
    """General Harpo secret backend exception"""


class HarpoSecretNotFound(HarpoSecretBackendException):
    """Harpo can't find requested secret"""


class HarpoSecretDecryptionError(HarpoSecretBackendException):
    """Harpo can't decrypt secret"""


# System
class HarpoNotInitialized(HarpoException):
    """Can't find .harpo"""


class HarpoAlreadyInitialized(HarpoException):
    """Harpo already initialized"""


class HarpoLockFileExists(HarpoException):
    """Tried to perform an action while the lock is being held by another application instance"""


class HarpoExportError(HarpoException):
    """General Exporter error"""


def handle_harpo_exceptions(func):
    """A decorator to properly log Harpo exceptions"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        try:
            return func(*args, **kwargs)
        except HarpoException as err:
            if "__context__" in err.__dict__ and err.__context__:
                logger.exception("%s: %s - %s", err.__doc__, err, err.__context__)
            else:
                logger.exception(err)
        except Exception as err:
            logger.exception(err)
        sys.exit(255)

    return wrapper
