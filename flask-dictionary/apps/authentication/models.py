# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

from apps import login_manager
from apps.database.models import Users
from apps.authentication.util import hash_pass

@login_manager.user_loader
def user_loader(id):
    print("Load user: {}".format(id))
    return Users.objects(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    print("Req Load user: {}".format(username))
    user = Users.objects(username=username).first()
    return user if user else None
