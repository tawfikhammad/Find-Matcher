from .enums import ValidationEnums
from typing import Tuple
from config import settings

class FileValidator:

    @staticmethod   
    async def isvalid(file_type : str, file_size : float) -> Tuple[bool, str]:
        
        if file_size > settings.MAX_FILE_SIZE:      # 3MB
            return False, ValidationEnums.INVALID_FILE_SIZE.value
        
        if file_type not in settings.ALLOWED_FILE_TYPES:
            return False, ValidationEnums.NOT_ALLOWED_FILE_TYPE.value 
        
        return True , ValidationEnums.VALID_FILE.value