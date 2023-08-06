from rest_framework.routers import DefaultRouter

from huscy.users import views


router = DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = router.urls
