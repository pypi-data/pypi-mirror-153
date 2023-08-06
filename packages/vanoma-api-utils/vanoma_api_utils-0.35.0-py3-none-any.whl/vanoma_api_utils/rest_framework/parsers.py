from djangorestframework_camel_case.parser import CamelCaseJSONParser  # type: ignore


class VanomaMediaTypeParser(CamelCaseJSONParser):
    """
    REST framework's header-based versioning looks at the Accept header to determine
    the version. Content-Type is never used to determine version. Therefore, we don't
    have to override media type here as we did for the renderer because clients will
    be include Accept header anywhere. Content-Type (for data submitted for example in
    POST request) will still be application/json.
    """
