from flask import jsonify

class MissingConfigurationException(Exception):
    
    def __init__(self, message="No configuration given, cannot start."):
        self.message = message
        super().__init__(self.message)

class MissingRequiredParamatersException(Exception):
    
    def __init__(self, message="Missing parameters."):
        self.message = message
        super().__init__(self.message)

class ObjectNotFoundException(Exception):
    
    def __init__(self, message="Not found."):
        self.message = message
        super().__init__(self.message)

class Error():
    """ Base class for errors. 
        Holds basic error structure: name, hint, message """

    def __init__(self, id="", name="", hint="", message="") -> None:
        self.id = id
        self.name = name
        self.hint = hint
        self.message = message

    def to_dict(self):
        dict = {'name':self.name, 'hint':self.hint, 'message':self.message, 'id':self.id}
        return dict

class HTTPError(Error):
    """ Base class for HTTP Errors. Extends Error and adds code """

    def __init__(self, id="", name="", hint="", message="", code=500) -> None:
        self.id = id
        self.name = name
        self.hint = hint
        self.message = message
        self.code = code
        super().__init__(self.id, self.name, self.hint, self.message)

    def to_dict(self):
        dict = {'code':self.code , 'name':self.name, 'hint':self.hint, 'message':self.message, 'id':self.id}
        return dict

    def make_error(self, format='json'):
        if format == 'json':
            return self.to_json(), self.code

    def to_json(self):
        return jsonify(self.to_dict())

class DuplicateUserKeyError(HTTPError):
    """ Error to be sent when a duplicate user key is sent for insertion """

    def __init__(self) -> None:
        self.id = 'user_create_duplicateKey'
        self.name = 'Duplicate user key'
        self.hint = 'Check for unique key restrictions'
        self.message = 'The data received for insertion includes violations to unique keys for users'
        self.code = 409
        super().__init__(self.id, self.name, self.hint, self.message, self.code)

class UserNotFoundError(HTTPError):
    """ Error to be sent when an user is not found """

    def __init__(self) -> None:
        self.id = 'user_not_found'
        self.name = 'User not found'
        self.hint = 'Check for key format and id existence'
        self.message = 'The fetch parameter for the user found no results'
        self.code = 404
        super().__init__(self.id, self.name, self.hint, self.message, self.code)

class UnexpectedError(HTTPError):
    """ Error to be sent when an internal error happens """

    def __init__(self) -> None:
        self.id = 'unexpected'
        self.name = 'Unexpected error'
        self.hint = 'Try again later'
        self.message = 'The server ran into an unexpected error, we are already working on it'
        self.code = 500
        super().__init__(self.id, self.name, self.hint, self.message, self.code)

class SSOError(HTTPError):
    """ Generic error for SSO endpoints """

    def __init__(self, id="", name="", hint="", message="", code=500, back_url_params="server_error") -> None:
        self.id = id
        self.name = name
        self.hint = hint
        self.message = message
        self.code = code
        self.back_url_params = back_url_params
        super().__init__(self.id, self.name, self.hint, self.message, self.code)

    def to_dict(self):
        dict = {'code':self.code , 'name':self.name, 'hint':self.hint, 'message':self.message, 'id':self.id, 'back_url_params' : self.back_url_params }
        return dict

    
class SSONoCredentialsError(SSOError):
    """ Missing credentials on SSO sign in """

    def __init__(self) -> None:
        self.id = 'sso_no_credentials'
        self.name = 'No Credentials'
        self.hint = 'Check the request to make sure credentials were supplied'
        self.message = 'The request had no credentials to execute authentication'
        self.code = 401
        self.back_url_params = 'error=client_id'
        super().__init__(self.id, self.name, self.hint, self.message, self.code, self.back_url_params)
    
class SSOInvalidCredentialsError(SSOError):
    """ Missing credentials on SSO sign in """

    def __init__(self) -> None:
        self.id = 'sso_invalid_credentials'
        self.name = 'Invalid Credentials'
        self.hint = 'Check the data provided and try again'
        self.message = 'Credentials did not match any of our records'
        self.code = 401
        self.back_url_params = 'error=invalid_request'
        super().__init__(self.id, self.name, self.hint, self.message, self.code, self.back_url_params)
    
class SSONoPermalinksAllowedError(SSOError):
    """ Not-authorized user asks for a long term token """

    def __init__(self) -> None:
        self.id = 'sso_permalink_not_allowed'
        self.name = 'Permalink access not granted'
        self.hint = 'Generate a temporary token or check your permissions'
        self.message = 'User is not allowed to generate long term tokens'
        self.code = 401
        self.back_url_params = 'error=client_id'
        super().__init__(self.id, self.name, self.hint, self.message, self.code, self.back_url_params)
    
class SSOAccessDeniedError(SSOError):
    """ Scope not authorized for object-action combination """

    def __init__(self, obj_type = "", action = "") -> None:
        self.id = 'sso_access_denied'
        self.name = 'Action access not granted'
        self.hint = f'Check your scopes for this object type and action: {obj_type} | {action}'
        self.message = f'User is not allowed to {action} on {obj_type}'
        self.code = 401
        self.back_url_params = 'error=client_id'
        super().__init__(self.id, self.name, self.hint, self.message, self.code, self.back_url_params)
    
class SSOInvalidUserTokenError(SSOError):
    """ The user token provided is not valid """

    def __init__(self) -> None:
        self.id = 'sso_invalid_user_token'
        self.name = 'Invalid user token'
        self.hint = 'Check the validity of the token provided'
        self.message = 'The user token provided is not valid'
        self.code = 401
        self.back_url_params = 'error=unauthorized_token'
        super().__init__(self.id, self.name, self.hint, self.message, self.code, self.back_url_params)
    
class SSOInvalidRequestError(SSOError):
    """ The request format or attributes are not valid """

    def __init__(self) -> None:
        self.id = 'sso_invalid_request'
        self.name = 'Invalid request'
        self.hint = 'Check the attributes and parameters and try again'
        self.message = 'The structure of the request is no valid'
        self.code = 400
        self.back_url_params = 'error=invalid_request'
        super().__init__(self.id, self.name, self.hint, self.message, self.code, self.back_url_params)
    
class SSOInvalidTokenError(SSOError):
    """ The token provided is not valid """

    def __init__(self) -> None:
        self.id = 'sso_invalid_token'
        self.name = 'Invalid  token'
        self.hint = 'Check the validity of the token provided'
        self.message = 'The  token provided is not valid'
        self.code = 401
        self.back_url_params = 'error=invalid_token'
        super().__init__(self.id, self.name, self.hint, self.message, self.code, self.back_url_params)

