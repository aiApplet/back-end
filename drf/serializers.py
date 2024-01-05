from rest_framework.serializers import ModelSerializer as DRFModelSerializer


class ModelSerializer(DRFModelSerializer):
    """重新定义序列化类"""

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # if data.get("image") and "http://" in data["image"]:
        #     data["image"] = data["image"].replace("http://", "https://")
        # if data.get("cover") and "http://" in data["cover"]:
        #     data["cover"] = data["cover"].replace("http://", "https://")
        return data
