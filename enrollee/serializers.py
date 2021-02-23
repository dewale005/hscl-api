from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .models import Enrollee


class UserSerializer(serializers.Serializer):
    """Serializer for the user object"""

    email = serializers.CharField(allow_blank=True, allow_null=True)
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False, allow_blank=True, allow_null=True)
    first_name = serializers.CharField(allow_blank=True, allow_null=True)
    last_name = serializers.CharField(allow_blank=True, allow_null=True)
    phone_no = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'password', 'first_name', 'last_name', 'phone_no')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}


    def create(self, validated_data):
        """create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)
        

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
            
        
        return user

class UserDetails(serializers.Serializer):

    email = serializers.CharField(allow_blank=True, allow_null=True)
    first_name = serializers.CharField(allow_blank=True, allow_null=True)
    last_name = serializers.CharField(allow_blank=True, allow_null=True)
    phone_no = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'password', 'first_name', 'last_name', 'phone_no')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=email, password=password)
        if not user:
            msg = ('Unable to autheticate with provided details')
            raise serializers.ValidationError(msg, code='authetication')

        attrs['user'] = user
        return attrs


class EnrolleeSerializers(serializers.Serializer):
    """Serializer for the enrollment object"""
    
    CHOICES = (
        ('married', 'Married'),
        ('single', 'Single'),
        ('divorsed', 'Divorsed'),
        ('widow', 'Widow'),
        ('widower', 'Widower'),
    )

    NEXT_OF_KIN = (
        ('father', 'Father'),
        ('son', 'Son'),
        ('wife', 'Wife'),
        ('husband', 'Husband'),
        ('mother', 'Mother'),
        ('sister', 'Sister'),
        ('brother', 'Brother'),
        ('relative', 'Relative'),
        ('friend', 'Friend'),
    )

    EMPLOYMENT = (
        ('employed', 'Employed'),
        ('unemployed', 'UnEmployed'),
    )

    GROUP = (
        ('individual', 'Individual'),
        ('group', 'Group'),
    )

    email = serializers.EmailField(allow_blank=True, allow_null=True)
    first_name = serializers.CharField(allow_blank=True, allow_null=True)
    last_name = serializers.CharField(allow_blank=True, allow_null=True)
    phone_no = serializers.CharField(allow_blank=True, allow_null=True)
    group_type = serializers.ChoiceField(allow_blank=True, allow_null=True, choices = GROUP)
    group_size = serializers.IntegerField()
    # address = serializers.CharField(allow_blank=True, allow_null=True)
    # date_of_birth = serializers.DateField()
    # martial_status = serializers.ChoiceField(choices = CHOICES, )
    # next_of_kin_phone_number = serializers.CharField(allow_blank=True, allow_null=True)
    # next_of_kin_name = serializers.CharField(allow_blank=True, allow_null=True)
    # next_of_kin_relationship = serializers.ChoiceField(allow_blank=True, allow_null=True, choices = NEXT_OF_KIN)
    # employment_status = serializers.ChoiceField(allow_blank=True, allow_null=True, choices = EMPLOYMENT)
    policy_id = serializers.CharField(allow_blank=True, allow_null=True)
    # has_subscribed = serializers.BooleanField(default=False)
    latitude = serializers.DecimalField(max_digits=60, decimal_places=30)
    longitude = serializers.DecimalField(max_digits=60, decimal_places=30)
    has_subscribed= serializers.BooleanField(default=False)
    # enrollment_address = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = Enrollee
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_no', 'address', 'date_of_birth', 'next_of_kin_name', 'next_of_kin_phone_number', 'martial_status', 'next_of_kin_relationship', 'employment_status', 'policy_id', 'has_subscribed', 'enrollment_address',)
        extra_kwargs = {'id': {'write_only': False, 'min_length': 5}}

    def create(self, validated_data):
        """create a new user with encrypted password and return it"""
        return Enrollee.objects.create(**validated_data)