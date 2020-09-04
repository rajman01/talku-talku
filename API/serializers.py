from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import Profile
from language.models import Language, Stage, StudyMaterial, Question, AnswerOptions, Result


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']

    def save(self, **kwargs):
        email = self.validated_data['email']
        if User.objects.filter(email=email).first():
            raise serializers.ValidationError({'email': 'email already exist'})
        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match'})
        account.set_password(password)
        account.save()
        return account


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # language_set = serializers.HyperlinkedRelatedField(
    #     view_name='language-detail',
    #     read_only=True,
    #     many=True
    # )
    profile = serializers.HyperlinkedRelatedField(
        view_name='profile-detail',
        read_only=True,
        many=False
    )
    result_set = serializers.HyperlinkedRelatedField(
        view_name='result-detail',
        read_only=True,
        many=True
    )

    class Meta:
        model = User
        fields = ['url', 'id', 'email', 'username', 'profile', 'result_set']
        read_only_fields = ['id', ]


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    # user = serializers.ReadOnlyField(source='user.username')

    # avatar = serializers.SerializerMethodField('get_image')

    class Meta:
        model = Profile
        fields = ['url', 'id', 'user', 'bio', 'avatar', 'languages', 'gender']

    # def get_image(self, profile):
    #     avatar = profile.avatar
    #     new_url = avatar.url
    #     if "?" in new_url:
    #         new_url = avatar.url[:avatar.url.rfind("?")]
    #     return new_url


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    stage_set = serializers.HyperlinkedRelatedField(
        view_name='stage-detail',
        read_only=True,
        many=True
    )

    class Meta:
        model = Language
        fields = ['url', 'id', 'name', 'brief_description', 'stage_set']


class StageSerializer(serializers.HyperlinkedModelSerializer):
    # language = serializers.HyperlinkedRelatedField(
    #     view_name='language-detail',
    #     read_only=True,
    #     many=False
    # )
    studymaterial = serializers.HyperlinkedRelatedField(
        view_name='studymaterial-detail',
        read_only=True,
        many=False
    )

    class Meta:
        model = Stage
        fields = ['url', 'id', 'language', 'number', 'studymaterial']


class StudyMaterialSerializer(serializers.HyperlinkedModelSerializer):
    question_set = serializers.HyperlinkedRelatedField(
        view_name='question-detail',
        read_only=True,
        many=True
    )

    class Meta:
        model = StudyMaterial
        fields = ['url', 'id', 'stage', 'topic', 'text', 'audio', 'question_set']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answeroptions_set = serializers.HyperlinkedRelatedField(
        view_name='answeroptions-detail',
        read_only=True,
        many=True
    )

    class Meta:
        model = Question
        fields = ['url', 'id', 'study_material', 'text', 'audio', 'answeroptions_set']


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnswerOptions
        fields = ['url', 'id', 'question', 'options_text', 'is_correct']


class ResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Result
        fields = ['url', 'id', 'user',  'study_material', 'score']


class CreateResultSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    study_material_id = serializers.CharField()

    class Meta:
        model = Result
        fields = ['username', 'study_material_id', 'score']

    def save(self, **kwargs):
        username = self.validated_data['username']
        study_material_id = self.validated_data['study_material_id']
        score = self.validated_data['score']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'user': 'user does not exist'})
        try:
            study_material = StudyMaterial.objects.get(pk=int(study_material_id))
        except StudyMaterial.DoesNotExist:
            raise serializers.ValidationError({'study_material': 'study material does not exist'})
        result = Result.objects.filter(user=user, study_material=study_material).first()
        if result:
            raise serializers.ValidationError({'result': 'result already exist'})
        else:
            result = Result(
                user=user,
                study_material=study_material,
                score=score
            )
            result.save()
            return result

