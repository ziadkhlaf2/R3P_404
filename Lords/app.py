from flask import Flask, render_template, request, redirect, session
from models import db, Player, HuntReport, TaskAdmin
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'R3P_lords'
migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lords.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        player_id = request.form.get('player_id')
        player=Player.query.filter_by(id=player_id).first()
        return render_template('search.html', result=player)
    return render_template('search.html', result=None)

@app.route('/add', methods=['GET', 'POST'])
def add_player():
    # 1. أول خطوة: التأكد من الصلاحية (الحارس)
    if not session.get('is_admin'):
        return redirect('/login') 

    if request.method == 'POST':
        p_id = request.form.get('player_id')
        p_name = request.form.get('player_name')
        p_spy = request.form.get('is_spy') == 'True'
        p_hunt = int(request.form.get('monster_hunt', 0))
        p_target = int(request.form.get('daily_target', 10))
        p_gf = int(request.form.get('gf_points', 0))
        p_dragon = int(request.form.get('dragon_count', 0))

        new_player = Player(
            id=p_id,
            name=p_name,
            is_spy=p_spy,
            monster_hunt=p_hunt,
            daily_target=p_target,
            guild_fest_points=p_gf,
            dragon_arena_count=p_dragon
        )
        db.session.add(new_player)
        db.session.commit()
        return redirect('/reports') # خليه يرجعك للتقارير بدل كلمة Done Save عشان تشوف النتيجة
        
    return render_template('add.html')

@app.route('/reports')
def reports():
    players = Player.query.all()
    return render_template('reports.html', players=players)

@app.route('/update/<id>', methods=['post'])
def update_player(id):
    player = Player.query.get(id)
    if player:
        player.monster_hunt = int(request.form.get('monster_hunt'))
        player.guild_fest_points= int(request.form.get('gf_points'))
        db.session.commit()
    return redirect('/report')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_player(id):
    player = Player.query.get(id)
    if request.method == 'POST':
        # تحديث كل الخانات
        player.name = request.form.get('player_name')
        player.is_spy = request.form.get('is_spy') == '1'
        player.monster_hunt = int(request.form.get('monster_hunt', 0))
        player.daily_target = int(request.form.get('daily_target', 10))
        player.guild_fest_points = int(request.form.get('gf_points', 0))
        player.dragon_arena_count = int(request.form.get('dragon_count', 0))
        
        db.session.commit()
        return redirect('/reports')
    
    return render_template('edit.html', player=player)


@app.route('/admins')
def admins_page():
    all_admins = TaskAdmin.query.all()
    return render_template('admins.html', admins=all_admins)

@app.route('/edit_admins', methods=['GET', 'POST'])
def edit_admins():
    if not session.get('is_admin'):
        return redirect('/login')
    
    tasks = ['البعثة', 'دبلوماسي', 'الصيد', 'الابطال', 'المهرجان', 'التنين']
    
    if request.method == 'POST':
        for task in tasks:
            new_name = request.form.get(task)
            admin_record = TaskAdmin.query.filter_by(task_name=task).first()
            
            if admin_record:
                admin_record.admin_name = new_name # تحديث لو موجودة
            else:
                new_admin = TaskAdmin(task_name=task, admin_name=new_name)
                db.session.add(new_admin)
        
        db.session.commit()
        return redirect('/admins') 
    
    current_admins = {a.task_name: a.admin_name for a in TaskAdmin.query.all()}
    return render_template('edit_admins.html', tasks=tasks, current_admins=current_admins)
#-----------------------------------------------------------------------------------------
ADMIN_USER = "admin"
ADMIN_PASS = "R3P lords"
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USER and request.form.get('password') == ADMIN_PASS:
            session['is_admin'] = True
            return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
