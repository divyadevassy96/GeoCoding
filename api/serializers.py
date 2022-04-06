from rest_framework import serializers

class GetAddressSerializer(serializers.Serializer):
    address = serializers.CharField()
    output_format= serializers.CharField()


    def validate_output_format(self, value):
        list = ["json", "xml"]
        if value not in list:
            raise serializers.ValidationError("Invalid output_format")
        return value
