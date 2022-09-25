import json
import traceback
from functools import wraps

from requests import HTTPError
from werkzeug.exceptions import BadRequest


def catch_errors(endpoint):
    @wraps(endpoint)
    def wrapper():
        try:
            return endpoint()

        except BadRequest as e:
            return e.description, e.code
        
        except HTTPError as e:
            if e.response and e.response.status_code and e.response.reason:
                reason = e.response.reason
                status_code = e.response.status_code
                return reason, status_code
            
            try:
                error = json.loads(e.strerror)['error']
                code = error['code']
                message = error['message']
                return message, code

            except Exception:
                return str(e), 500
        
        except Exception as e:
            print(traceback.format_exc())
            return str(e), 500

    return wrapper
