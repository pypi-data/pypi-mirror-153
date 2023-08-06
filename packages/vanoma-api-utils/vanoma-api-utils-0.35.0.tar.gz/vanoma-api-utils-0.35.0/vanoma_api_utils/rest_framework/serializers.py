from typing import Any, Dict
from django.db.models import Model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.serializers import *  # Import everything so that this file is enough to access DRF stuffs


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base model serializer which can also be used as a relation field of another serializer. DRF
    separates relation fields from the regular fields of a serializer, but the main difference between
    both from the API'sperspective is that a relation field takes "queryset" parameter. They also differ
    implementation wise in that the to_internal_value method returns an instance of the model in relation
    field while it doesn't for non-relation field. So this class allows model serializer class to be passed
    a queryset parameter to imply that it is being used a relation field.
    """

    def __init__(
        self,
        instance: Model = None,
        data: Any = serializers.empty,
        **kwargs: Any,
    ) -> None:
        self.queryset = kwargs.pop("queryset", None)
        self.primary_key = kwargs.pop("primary_key", None)
        super().__init__(instance=instance, data=data, **kwargs)

    def run_validators(self, value: Any) -> None:
        """
        Serializer inherits from Field and override this method to transform *value* into an iterable
        obviouly because a Serializer contains an iterable of fields. However, if this model is being
        used as a relation field, we expect value to be a non-iterable. In that case, we should call
        the Field.run_validators method instead of Serializer.run_validators
        """
        if self.queryset is None:
            return super().run_validators(value)

        return super(serializers.Serializer, self).run_validators(value)

    def to_internal_value(self, data: Dict[str, Any]) -> Any:
        if self.queryset is None:
            return super().to_internal_value(data)

        if not isinstance(data, dict):
            message = "Invalid data type. Expected a dict but found {}".format(
                type(data)
            )
            raise serializers.ValidationError(message)

        if self.primary_key not in data:
            message = f"Nested field {self.primary_key} can not be empty"
            raise serializers.ValidationError(message)

        try:
            return self.queryset.get(**{self.primary_key: data[self.primary_key]})
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                f"Invalid {self.primary_key}. Object does not exist"
            )
