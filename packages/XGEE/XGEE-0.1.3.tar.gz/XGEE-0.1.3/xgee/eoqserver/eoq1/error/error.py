### EXCEPTION DEFINITIONS ###

EOQ_ERROR_TYPE_PARSE = 1000
EOQ_ERROR_TYPE_CONTEXT = 2000
EOQ_ERROR_TYPE_RETRIEVE = 3000
EOQ_ERROR_TYPE_UPDATE = 4000
EOQ_ERROR_TYPE_CREATE = 5000
EOQ_ERROR_TYPE_ID = 6000
EOQ_ERROR_TYPE_VALUE = 7000
EOQ_ERROR_TYPE_TRANSACTION = 8000
EOQ_ERROR_TYPE_ACTION = 8500
EOQ_ERROR_TYPE_GENERAL = 9999



class EoqError(Exception):
    def __init__(self,type,code):
        self.type = type
        self.code = code #all errors will show a specific code

class EoqParseError(EoqError):
    def __init__(self, code, message, query):
        super().__init__(EOQ_ERROR_TYPE_PARSE,code)
        self.message = message
        self.query = query

class EoqContextError(EoqError):
    def __init__(self, code, message):
        super().__init__(EOQ_ERROR_TYPE_CONTEXT,code)
        self.message = message

class EoqRetrieveError(EoqError):
    def __init__(self, code, message):
        super().__init__(EOQ_ERROR_TYPE_RETRIEVE,code)
        self.message = message

class EoqUpdateError(EoqError):
    def __init__(self, code, message, value):
        super().__init__(EOQ_ERROR_TYPE_UPDATE,code)
        self.message = message
        self.value = value

class EoqCreateError(EoqError):
    def __init__(self, code, message, package, clazz):
        super().__init__(EOQ_ERROR_TYPE_CREATE,code)
        self.message = message
        self.package = package
        self.clazz = clazz
        
class EoqIdError(EoqError):
    def __init__(self, code, message, idNb):
        super().__init__(EOQ_ERROR_TYPE_ID,code)
        self.message = message
        self.idNb = idNb
        
class EoqValueError(EoqError):
    def __init__(self, code, message, value):
        super().__init__(EOQ_ERROR_TYPE_VALUE,code)
        self.message = message
        self.value = value
        
class EoqTransactionError(EoqError):
    def __init__(self, code, message):
        super().__init__(EOQ_ERROR_TYPE_TRANSACTION,code)
        self.message = message
        
class EoqActionError(EoqError):
    def __init__(self, code, message):
        super().__init__(EOQ_ERROR_TYPE_ACTION,code)
        self.message = message
        
class EoqGeneralError(EoqError):
    def __init__(self, code, message):
        super().__init__(EOQ_ERROR_TYPE_CREATE,code)
        self.message = message