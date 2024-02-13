from flask import Blueprint
from auth.UserAuth import admin_required
import db.dashboard as database


dashboard= Blueprint(name="dashboard", import_name="dashboard")
@dashboard.route("/get_dashbord", methods=["GET"])
def get_dashboard():
    admin_required()
    

