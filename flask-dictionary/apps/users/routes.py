from apps.users import blueprint
from flask import render_template
from flask_login import login_required
from werkzeug.local import LocalProxy
from flask import current_app
from apps.database.models import Users, Roles
logger = LocalProxy(lambda: current_app.logger)

@blueprint.route('/users',methods=['GET'])
@login_required
def list_users():
    logger.info("View all users")
    user_list=Users.objects()
    return render_template('users/users.html', segment='users',users=user_list)


@blueprint.route('/roles',methods=['GET'])
@login_required
def list_roles():
    logger.info("View all roles")
    role_list=Roles.objects()
    return render_template('users/roles.html', segment='roles',roles=role_list)
