from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# جدول اللاعب
class Player(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    old_names = db.Column(db.Text)
    is_spy = db.Column(db.Boolean, default=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    monster_hunt = db.Column(db.Integer, default=0)
    hunt_level = db.Column(db.Integer, default=1)
    daily_target = db.Column(db.Integer, default=0)
    guild_fest_points = db.Column(db.Integer, default=0)
    dragon_arena_count = db.Column(db.Integer, default=0)

#تقارير الصيد
class HuntReport(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.String(20), db.ForeignKey('player.id'))
    monster_lvl = db.Column(db.Integer)
    hunt_date = db.Column(db.DateTime, default=datetime.utcnow)

#المسؤولين
class TaskAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), unique=True)
    admin_name = db.Column(db.String(50))
