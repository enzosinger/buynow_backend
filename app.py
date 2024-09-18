from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Model para o usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Rota principal com cadastro e listagem de usuários
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica se o usuário já existe
        if User.query.filter_by(username=username).first():
            flash('Usuário já cadastrado!')
        else:
            # Cria e adiciona o novo usuário
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Cadastro realizado com sucesso!')

        return redirect('/')

    # Lista todos os usuários cadastrados
    users = User.query.all()
    return render_template('index.html', users=users)

# Rota para editar um usuário existente
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)  # Busca o usuário pelo ID
    if request.method == 'POST':
        user.username = request.form['username']
        user.password = request.form['password']
        db.session.commit()
        flash('Usuário atualizado com sucesso!')
        return redirect('/')
    return render_template('edit.html', user=user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas
    app.run(host='0.0.0.0', port=5000, debug=True)  # Alterar o host para '0.0.0.0'
