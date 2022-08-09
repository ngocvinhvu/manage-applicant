from flask_babel import lazy_gettext as _l
class BaseException(Exception):
    """Base Exception"""

    message = _l("An unknown exception")
    code = 500
    headers = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs
        self.kwargs['message'] = message

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                print("AttributeError")

        try:
            message = self.message % kwargs
        except Exception:
            if not message:
                message = self.message
        self.msg = message
        super(BaseException, self).__init__(message)


class ServerNotSupport(BaseException):
    message = _l('The server does not support the action requested by the browser')
    code = 501
    safe = True


class DirectoryNotEmptyException(BaseException):
    message = _l('The %(directory_name)s directory not empty')
    code = 400
    safe = True


class IllegalNameException(BaseException):
    message = _l('The %(name)s is invalid')
    code = 400
    safe = True


class NotFoundException(BaseException):
    message = _l('Resource could not be found')
    code = 404
    safe = True


class MultipartUploadCacheNotFoundByIdException(NotFoundException):
    message = _l('The upload_id %(upload_id)s could not be found')


class MultipartUploadCacheIdNotMatchFileException(NotFoundException):
    message = _l('The %(upload_id)s not match %(file_name)s')


class ActivityNotFoundException(NotFoundException):
    message = _l('Activity %(activity_id)s could not be found')


class MachineNotFoundException(NotFoundException):
    message = _l('Machine %(machine_id)s could not be found')


class BackupDirectoryNotFoundException(NotFoundException):
    message = _l('Backup directory %(backup_directory_id)s could not be found')


class PolicyNotFoundException(NotFoundException):
    message = _l('Policy %(policy_id)s could not be found')


class StorageVaultNotFoundException(NotFoundException):
    message = _l('Storage Vault %(storage_vault_id)s could not be found')


class RecoveryPointNotFoundException(NotFoundException):
    message = _l('Recovery Point %(recovery_point_id)s could not be found')


class DirectoryNotFoundException(NotFoundException):
    message = _l('Directory %(directory_id)s could not be found')


class FileNotFoundException(NotFoundException):
    message = _l('File %(file_id)s could not be found')


class ChunkerNotFoundException(NotFoundException):
    message = _l('Chunker of recovery_point %(recovery_point_id)s could not be found')


class ResourceQuotaNotFoundException(NotFoundException):
    message = _l('%(resource)s quota of tenant %(tenant_id)s could not be found')


class ExistException(BaseException):
    message = _l('Resource Exist')
    code = 400
    safe = True


class BackupDirectoryExistException(ExistException):
    # Raise exception in some cases:
    # - BackupDirectory exist in Policy
    # - Path BackupDirectory exist in machine
    message = _l('BackupDirectory %(backup_directory_id)s exist')


class BackupDirectoryNotExistException(ExistException):
    message = _l('BackupDirectory %(backup_directory_id)s not exist')


class RecoveryPointNotExistException(ExistException):
    message = _l('RecoveryPoint %(recovery_point_id)s not exist')


class RecoveryPointExistException(ExistException):
    message = _l('BackupDirectory %(recovery_point_id)s exist')


class ItemNotExistException(ExistException):
    message = _l('RecoveryPoint %(item_id)s not exist')


class ItemExistException(ExistException):
    message = _l('BackupDirectory %(item_id)s exist')


# Exception Storage
class StorageException(BaseException):
    message = _l('Storage exception')
    safe = True


class S3ObjectNotFoundException(NotFoundException):
    message = _l('Object %(key)s could be not found')


class BrokerUserUnauthorized(BaseException):
    message = _l('BrokerUserUnauthorized')
    code = 401
    safe = True
