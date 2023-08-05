from bitso.media.models import MEDIA_PATH_RESOLVER
from bitso.utils import get_setting
from storages.backends.s3boto import S3BotoStorage

VERSION = get_setting("VERSION")

class S3Storage(S3BotoStorage):
    
    def url(self, name):
        
        url = S3BotoStorage.url(self, name)
        
        upload_path = None
        
        if isinstance(MEDIA_PATH_RESOLVER, (str, unicode)):
            
            upload_path = MEDIA_PATH_RESOLVER
            
        elif hasattr(MEDIA_PATH_RESOLVER, "path"):
            
            upload_path = MEDIA_PATH_RESOLVER.path
            
        if upload_path and url.__contains__(upload_path):
            
            return url
        
        if url.__contains__("?") :
        
            return url + "&version=" + VERSION
        
        return url + "?version=" + VERSION