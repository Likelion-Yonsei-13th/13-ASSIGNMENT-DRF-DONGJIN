from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

#유저 모델 가져오기
User = get_user_model()


#ModelSerializer user의 모든 정보
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    #Usermodel 쓸거야
    #username, password, nickname만 사용자에게 입력 받을 거야
    class Meta:
        model = User
        fields = ('username', 'password', 'nickname')

    #serializer.save 호출 시 자동으로 실행됨
    #password를 따로 해시처리하고 담아야해서 create 함수 작성해야 함함
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            nickname = validated_data.get('nickname', '')
        )
        user.set_password(validated_data['password'])#해시처리리
        user.save()
        return user

#Serializer 필요한 정보
class UserLoginSerialzer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise serializers.ValidationError("아이디와 비밀번호를 모두 입력해주세요.")

        user = authenticate(username = username, password=password)

        if not user:
            raise serializers.ValidationError("아이디 또는 비밀번호가 올바르지 않음")
        
        data["user"] = user
        return data