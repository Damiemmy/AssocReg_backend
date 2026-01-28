from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from api.models import Association,AssociationMembership,Executive,Event,Transaction,Receipt

User = get_user_model()

import requests

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2=serializers.CharField(write_only=True,required=True)

    class Meta:
        model=User
        fields=['full_name','reg_number','phone','email','password','password2']

    def validate(self,attr):
        if attr['password']!= attr['password2']:
            raise serializers.validationError({"password":"password fields didn't match"})
        return attr
    def create(self,validated_data):
        user=User.objects.create(
            reg_number=validated_data['reg_number'],
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            phone=validated_data['phone'],
        )
        email_username= user.email.split('@')[0]
        user.username=email_username
        user.set_password(validated_data['password'])
        user.save()

         # 🔔 Notify n8n (non-blocking)
        try:
            requests.post(
                "http://localhost:5678/webhook-test/user-register",
                json={
                    "email": user.email,
                    "full_name": user.full_name,
                    "reg_number": user.reg_number,
                    "phone":user.phone
                },
                timeout=5
            )
        except Exception as e:
            print("n8n registration webhook failed:", e)

        return user
        
class AssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        fields = "__all__"

class AssociationMembershipSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AssociationMembership
        fields = "__all__"
class ExecutiveSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    association = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Executive
        fields = "__all__"

class EventListSerializer(serializers.ModelSerializer):
    association = serializers.StringRelatedField()

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "image",
            "event_date",
            "is_paid",
            "amount",
        )

class EventDetailSerializer(serializers.ModelSerializer):
    association = AssociationSerializer(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = "__all__"

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "id",
            "event",
            "association",
            "amount",
            "payment_method",
        )

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    event = serializers.StringRelatedField()

    class Meta:
        model = Transaction
        fields = "__all__"

class ReceiptSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer(read_only=True)

    class Meta:
        model = Receipt
        fields = "__all__"

