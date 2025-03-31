from rest_framework import serializers
from .models import Lesson, LessonComment, Course, Teacher, User, StudentWorkResult, Exercise
from question.serializers import Question, QuestionSerializer
from course.serializers import CourseSerializer
# from moviepy.editor import VideoFileClip
# from tempfile import NamedTemporaryFile


class ExerciseSerializer(serializers.ModelSerializer):
    lesson_id = serializers.UUIDField()
    question_ids = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(), many=True, write_only=True)

    class Meta:
        model = Exercise
        fields = [
            'id', 'name', 'total_time', 'total_questions', 'description', 'pdf_file',
            'number_of_lesson_exercise', 'is_public', 'created_at', 'lesson_id', 'question_ids'
        ]
        read_only_fields = ['id', 'number_of_lesson_exercise',  'created_at']

    def create(self, validated_data):
        questions_data = validated_data.pop('question_ids', [])
        exercise = Exercise.objects.create(**validated_data)
        exercise.questions.set(questions_data)
        exercise.save()
        return exercise


class LessonSerializer(serializers.ModelSerializer):
    course_id = serializers.UUIDField(write_only=True)
    course = CourseSerializer(read_only=True)
    teacher_id = serializers.UUIDField()
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'pdf_file', 'video_file', 'numerical_order',
                  'number_of_lesson_views', 'number_of_likes', 'created_at', 'duration', 'course',
                  'course_id', 'teacher_id', 'is_public', 'exercises']
        read_only_fields = ['id', 'number_of_lesson_views', 'number_of_likes']

    # def get_video_duration(self, video_file) -> int:
    #     """Trích xuất thời lượng từ video file và trả về số phút (int)."""
    #     try:
    #         with NamedTemporaryFile(delete=True, suffix=".mp4") as temp_file:
    #             for chunk in video_file.chunks():
    #                 temp_file.write(chunk)
    #             temp_file.flush()

    #             clip = VideoFileClip(temp_file.name)
    #             duration_in_minutes = round(clip.duration / 60)
    #             clip.close()
    #             return duration_in_minutes
    #     except Exception as e:
    #         print("⚠️ Lỗi khi tính thời lượng video:", e)
    #         return 0
    def create(self, validated_data):
        new_position = validated_data.get('numerical_order', None)
        course_id = validated_data.get('course_id')
        course = Course.objects.get(id=course_id)

        lessons_to_update = Lesson.objects.filter(
            course=course, numerical_order__gte=new_position)
        for lesson in lessons_to_update:
            lesson.numerical_order += 1
            lesson.save()
        lesson_new = Lesson.objects.create(**validated_data)
        lesson_new.course.lesson_count += 1
        lesson_new.course.save()

        return lesson_new

    def update(self, instance, validated_data):
        new_position = validated_data.get('numerical_order', None)

        if new_position is not None and new_position != instance.numerical_order:
            course_id = validated_data.get('course_id', instance.course_id)
            course = Course.objects.get(id=course_id)

            lessons_to_update = Lesson.objects.filter(
                course=course, numerical_order__gt=instance.numerical_order)
            for lesson in lessons_to_update:
                lesson.numerical_order -= 1
                lesson.save()

            lessons_to_update = Lesson.objects.filter(
                course=course, numerical_order__gte=new_position)
            for lesson in lessons_to_update:
                lesson.numerical_order += 1
                lesson.save()

            instance.numerical_order = new_position

        return super().update(instance, validated_data)


class LessonCommentSerializer(serializers.ModelSerializer):
    lesson_id = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all())
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = LessonComment
        fields = ['id', 'content', 'number_of_likes',
                  'created_at', 'lesson_id', 'user_id']
        read_only_fields = ['id', 'number_of_likes', 'created_at']
