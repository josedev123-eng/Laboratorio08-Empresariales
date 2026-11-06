from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, QuestionViewSet, ChoiceViewSet

router = DefaultRouter()
router.register(r'exams', ExamViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)

urlpatterns = router.urls