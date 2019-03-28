# Defining nsg errors code


# TODO: to complete
class Errors(object):

    class Authorization(object):
        code = 1

        def __str__(self):
            return "User doesn't have permission (not in correct role)."

    class Authentication(object):
        code = 2

        def __str__(self):
            return "Bad or missing basic auth credentials or cipres custom headers."

    class NotFound(object):
        code = 4

        def __str__(self):
            return "Job, user, document, app or tool not found."

    class FormValidation(object):
        code = 5

        def __str__(self):
            return "Bad form parameter."

    class UserMismatch(object):
        code = 6

        def __str__(self):
            return "Username in url doesn't own the job or document specified in url."

    class BadRequest(object):
        code = 7

        def __str__(self):
            return "Something wrong with request, other bad form param. Maybe bad or missing query param."

    # This mean jersey didn't like the request. Didn't even make it to cipres code. Client may not
    # care wheter it's BAD REQUEST or BAD INVOCATION but cipres admin may want to know.
    # bad_invocation = 102

    class GenericServiceError(object):
        code = 100

        def __str__(self):
            return 'Display message is "Internal Cipres Error".'

    class GenericCommonError(object):
        code = 101

        def __str__(self):
            return "If client gets an exception while making a request, \
                    or if status returned is other than 200, but ErrorData \
                    with this code, in order to provide a consistent interface \
                    to higher level code"

    class UserError(object):
        code = 102

        def __str__(self):
            return "User error, detected by client application, not thrown by service."

#   // Too many active requests, too many SUs consumed, etc. See sdk/Jobs/UsageLimit.java.
#   // Http status code will be 429: see cipresrest/webresource/UsageLimitExceptionMapper.java
#   // When this is set, ErrorData will include a LimitStatus element.
#   public static final int USAGE_LIMIT = 103;
#
#   public static final int DISABLED_RESOURCE = 104;


def get_error(code):
    if code == 1:
        return Errors.Authorization
    elif code == 2:
        return Errors.Authentication
    elif code == 4:
        return Errors.NotFound
    elif code == 5:
        return Errors.FormValidation
    elif code == 6:
        return Errors.UserMismatch
    elif code == 7:
        return Errors.BadRequest
    elif code == 100:
        return Errors.GenericServiceError
    elif code == 101:
        return Errors.GenericCommonError
    elif code == 102:
        return Errors.UserError

