from flask import Blueprint, render_template

admin = Blueprint('admin', __name__,
                     template_folder='templates',
                     static_folder='static'
                    )

@admin.route('/admin')
def admin_home():
    return render_template("home.html")

@admin.route('/admin/test')
def admin_test():
    return render_template("home.html")

