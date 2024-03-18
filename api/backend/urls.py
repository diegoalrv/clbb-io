from rest_framework.routers import DefaultRouter
from django.urls import path, include
from backend.views.map.map import MapViewSet, TestImageViewSet
from backend.views.slots.slots import SlotViewSet
from backend.views.globals import views as globalviews




router = DefaultRouter()
router.register(r'maps', MapViewSet)
router.register(r'image', TestImageViewSet)
router.register(r'slots', SlotViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('set_map_type/', globalviews.set_map_type, name='set_map_type'),
    path('set_map_state/', globalviews.set_map_state, name='set_map_state'),
    # path('set_map_state2/', globalviews.set_map_state2, name='set_map_state2'),
    path('get_globals/', globalviews.get_global_variables, name='get_globals'),
    #path('what_map/',globalviews.what_map, name='what_map')
]

