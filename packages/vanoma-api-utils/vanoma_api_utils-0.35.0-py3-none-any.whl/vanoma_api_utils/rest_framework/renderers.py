from djangorestframework_camel_case.render import CamelCaseJSONRenderer  # type: ignore


class VanomaMediaTypeRenderer(CamelCaseJSONRenderer):
    """
    We use a custom media type to support versioning. We are overriding the
    media type here so our render can work with our custom media type instead of
    the default application/json.
    """
