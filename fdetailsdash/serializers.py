# # File: fdetailsdash/serializers.py
# from rest_framework import serializers
# from core.models import ChecklistItem
# from .models import StudentChecklistStatus, StudentItemStatus

# class ChecklistItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChecklistItem
#         fields = ['id', 'name']

# class StudentItemStatusSerializer(serializers.ModelSerializer):
#     item_name = serializers.ReadOnlyField(source='item.name')

#     class Meta:
#         model = StudentItemStatus
#         fields = ['id', 'item', 'item_name', 'checked']

# class StudentChecklistStatusSerializer(serializers.ModelSerializer):
#     items = StudentItemStatusSerializer(many=True)

#     class Meta:
#         model = StudentChecklistStatus
#         fields = ['id', 'roll', 'remarks', 'items']

#     def create(self, validated_data):
#         items_data = validated_data.pop('items')
#         student = StudentChecklistStatus.objects.create(**validated_data)
#         for item in items_data:
#             StudentItemStatus.objects.create(student=student, **item)
#         return student

#     def update(self, instance, validated_data):
#         items_data = validated_data.pop('items', [])
#         instance.remarks = validated_data.get('remarks', instance.remarks)
#         instance.save()

#         for item in items_data:
#             StudentItemStatus.objects.update_or_create(
#                 student=instance,
#                 item=item['item'],
#                 defaults={'checked': item['checked']}
#             )
#         return instance

# serializers.py

from rest_framework import serializers
from .models import StudentRequirementStatus


class StudentRequirementStatusSerializer(serializers.ModelSerializer):
    # This will handle file uploads
    certificate_file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = StudentRequirementStatus
        fields = [
            'id',
            'student',
            'faculty_subject',
            'requirement_type',
            'is_completed',
            'remarks',
            'certificate_file',
        ]

