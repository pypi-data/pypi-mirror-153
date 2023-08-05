from flask import Blueprint, jsonify
from velero.utils import velero

profile = Blueprint("settings", __name__)


@profile.route("/location/backup")
def backup():
    location = velero("backup-location get")
    # current_app.logger.error(f"Backup list: {list}")
    return jsonify(location)


@profile.route("/location/snapshot")
def snapshot():
    location = velero("snapshot-location get")
    # current_app.logger.error(f"Backup list: {list}")
    return jsonify(location)