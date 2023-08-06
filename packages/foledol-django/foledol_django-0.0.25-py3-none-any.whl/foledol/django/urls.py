from django.conf.urls import url

from foledol.django import auth
from foledol.django.views import logs, grids, grid, columns, column, conditions, condition

app_name = "django"

urlpatterns = [
    url(r'user_login/', auth.user_login, name='user_login'),
    url(r'user_logout/', auth.user_logout, name='user_logout'),

    url(r'logs', logs.log_list, name='logs'),
    url(r'log_plot_today', logs.log_plot_today, name='log_plot_today'),
    url(r'log_plot', logs.log_plot, name='log_plot'),
    url(r'log_events', logs.log_events, name='log_events'),
    url(r'log_update/(?P<pk>\d+)', logs.log_update, name='log_update'),

    url(r'grids', grids.grid_list, name='grids'),
    url(r'grid_create/', grid.grid_create, name='grid_create'),
    url(r'grid_update/(?P<pk>\d+)', grid.grid_update, name='grid_update'),
    url(r'grid_delete/(?P<pk>\d+)', grid.grid_delete, name='grid_delete'),
    url(r'grid_view/(?P<pk>\d+)', grid.grid_view, name='grid_view'),

    url(r'columns', columns.column_list, name='columns'),
    url(r'column_create/', column.column_create, name='column_create'),
    url(r'column_update/(?P<pk>\d+)', column.column_update, name='column_update'),
    url(r'column_delete/(?P<pk>\d+)', column.column_delete, name='column_delete'),

    url(r'conditions', conditions.condition_list, name='conditions'),
    url(r'condition_create/', condition.condition_create, name='condition_create'),
    url(r'condition_update/(?P<pk>\d+)', condition.condition_update, name='condition_update'),
    url(r'condition_delete/(?P<pk>\d+)', condition.condition_delete, name='condition_delete'),
]


