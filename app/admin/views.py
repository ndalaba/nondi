from flask import render_template
from . import admin


@admin.route('/home')
def home():
    return render_template('admin/home.html')
