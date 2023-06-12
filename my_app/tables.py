import django_tables2 as tables
from .models import Users
from django_tables2.utils import A

class UsersTable(tables.Table):
    delete = tables.LinkColumn('delete_user', args=[A('pk')], attrs={
    'a': {'class': 'deletebtn'}
    })
    edit = tables.LinkColumn('edit_user', args=[A('pk')], attrs={
    'a': {'class': 'editbtn'}
    })
    confirm = tables.LinkColumn('confirm_user', args=[A('pk')], attrs={
    'a': {'class': 'confirmbtn'}
    })
    class Meta:
        model = Users