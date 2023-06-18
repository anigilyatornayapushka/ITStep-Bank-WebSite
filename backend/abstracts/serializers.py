# DRF
from rest_framework import serializers

# Python
import typing as t


class CheckFieldsValidSerializer(serializers.Serializer):
    """
    Serializer to check if passed fields are valid.
    """

    allowed_fields: tuple = ('csrfmiddlewaretoken', '_content_type',
                             '_content')

    def to_internal_value(self, data: t.OrderedDict) -> t.OrderedDict:
        """
        Checking if the transmitted data is invalid.
        """
        # All allowed fields
        all_fields: t.OrderedDict = self.get_fields()

        # Errors dict ro raise them later
        error: dict = {}

        # Check if all transmitted fields in allowed fields
        for field in data:

            # If not allowed
            if field not in all_fields and field not in self.allowed_fields:

                # Raise exception
                error.update({field: ['Not allowed.']})

        # If any error was found
        if error:
            raise serializers.ValidationError(error)

        return super().to_internal_value(data)
