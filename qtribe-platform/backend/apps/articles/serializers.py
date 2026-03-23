from rest_framework import serializers
from .models import Article, ArticleImage, Tag, ArticleTag, Comment
from apps.users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description']


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = ['id', 'image', 'order']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'parent', 'like_count', 'replies', 'is_liked', 'create_time']
        read_only_fields = ['id', 'create_time', 'like_count']

    def get_replies(self, obj):
        if hasattr(obj, 'replies'):
            replies = obj.replies.filter(is_deleted=False)[:3]
            return CommentSerializer(replies, many=True, context=self.context).data
        return []

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from apps.interactions.models import Like
            return Like.objects.filter(
                user=request.user,
                comment=obj,
                is_active=True
            ).exists()
        return False


class ArticleListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_collected = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'summary', 'cover_image', 'author',
            'view_count', 'like_count', 'collect_count', 'comment_count',
            'is_top', 'tags', 'is_liked', 'is_collected',
            'published_at', 'create_time'
        ]

    def get_tags(self, obj):
        return TagSerializer([at.tag for at in obj.article_tags.all()], many=True).data

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from apps.interactions.models import Like
            return Like.objects.filter(
                user=request.user,
                article=obj,
                is_active=True
            ).exists()
        return False

    def get_is_collected(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from apps.interactions.models import Collection
            return Collection.objects.filter(
                user=request.user,
                article=obj,
                is_active=True
            ).exists()
        return False


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.SerializerMethodField()
    images = ArticleImageSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_collected = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'summary', 'cover_image', 'author',
            'view_count', 'like_count', 'collect_count', 'comment_count',
            'is_published', 'is_top', 'status', 'tags', 'images',
            'is_liked', 'is_collected', 'is_author',
            'published_at', 'create_time', 'update_time'
        ]

    def get_tags(self, obj):
        return TagSerializer([at.tag for at in obj.article_tags.all()], many=True).data

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from apps.interactions.models import Like
            return Like.objects.filter(
                user=request.user,
                article=obj,
                is_active=True
            ).exists()
        return False

    def get_is_collected(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from apps.interactions.models import Collection
            return Collection.objects.filter(
                user=request.user,
                article=obj,
                is_active=True
            ).exists()
        return False

    def get_is_author(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False


class ArticleCreateSerializer(serializers.ModelSerializer):
    tag_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'summary', 'cover_image', 'tag_ids', 'is_published']

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        article = Article.objects.create(**validated_data)

        for tag_id in tag_ids:
            try:
                tag = Tag.objects.get(id=tag_id)
                ArticleTag.objects.create(article=article, tag=tag)
            except Tag.DoesNotExist:
                pass

        return article

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tag_ids is not None:
            ArticleTag.objects.filter(article=instance).delete()
            for tag_id in tag_ids:
                try:
                    tag = Tag.objects.get(id=tag_id)
                    ArticleTag.objects.create(article=instance, tag=tag)
                except Tag.DoesNotExist:
                    pass

        return instance


class ArticleUpdateSerializer(serializers.ModelSerializer):
    tag_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'summary', 'cover_image', 'tag_ids', 'is_published', 'is_top']

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tag_ids is not None:
            ArticleTag.objects.filter(article=instance).delete()
            for tag_id in tag_ids:
                try:
                    tag = Tag.objects.get(id=tag_id)
                    ArticleTag.objects.create(article=instance, tag=tag)
                except Tag.DoesNotExist:
                    pass

        return instance


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'parent']

    def validate_parent(self, value):
        if value:
            article_id = self.context.get('article_id')
            if value.article_id != article_id:
                raise serializers.ValidationError('父评论不属于当前文章')
        return value


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'description']

    def validate_name(self, value):
        if Tag.objects.filter(name=value.lower()).exists():
            raise serializers.ValidationError('标签已存在')
        return value.lower()
