"""An amazing sample package!"""

__version__ = "0.1.1"

from flask import Flask, render_template
from logging.config import dictConfig
from velero.views import dashboard
from velero.views.settings import settings
from velero.views.backup import backup_index
from velero.views.backup import backup_get
from velero.views.backup import backup_describe
from velero.views.backup import backup_logs
from velero.views.backup import backup_delete
from velero.views.restore import restore_get
from velero.views.schedule import schedule_get

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

app.config.from_object("config")
app.config["SECRET_KEY"]

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(403)
def insufficient_permissions(e):
    return render_template("403.html"), 403

app.register_blueprint(dashboard.profile)
app.register_blueprint(settings.profile)
app.register_blueprint(backup_index.profile)
app.register_blueprint(backup_get.profile)
app.register_blueprint(backup_describe.profile)
app.register_blueprint(backup_logs.profile)
app.register_blueprint(backup_delete.profile)
app.register_blueprint(restore_get.profile)
app.register_blueprint(schedule_get.profile)
