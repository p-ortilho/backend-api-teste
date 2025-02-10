from flask import jsonify, request
from database.db_config import create_app, db
from model.Servicos import Servicos
from model.Usuarios import Usuarios
from model.Atendimentos import Atendimentos
from middleware.Autenticar import token_required
import datetime
import jwt

app = create_app()

@app.route('/')
def index():
    try:
        if request.method not in ['GET']:
            return jsonify({
                'error': 'Método não permitido',
                'message': 'Apenas requisições GET são permitidas nesta rota'
            }), 405

        return jsonify({
            'status': 'success',
            'message': 'API de agendamento de serviços',
            'version': '1.0'
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Erro interno do servidor',
            'message': 'Ocorreu um erro ao processar sua requisição'
        }), 500

@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.json

    try:
        usuario = Usuarios(data['nome'], data['email'], data['senha'])
        db.session.add(usuario)
        db.session.commit()

        return jsonify({'message': 'Usuário registrado com sucesso!'})
    
    except Exception:
        return jsonify({'message': 'Erro ao registrar usuário!'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    try:
        usuario = Usuarios.query.filter_by(email=data['email']).first_or_404()

        if not usuario.check_password(data['senha']):
            return jsonify({'message': 'Senha inválida!'}), 401
    
        payload = {
            'id': usuario.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        }

        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token})
        
    except Exception:
        return jsonify({'message': 'Erro ao fazer login!'}), 401
       
@app.route('/auth/servicos', methods=['GET'])
@token_required
def get_servicos(current_user):
    servicos = Servicos.query.all()
    return jsonify([servico.to_dict() for servico in servicos])

@app.route('/auth/servicos/<string:email>', methods=['GET'])
@token_required
def get_servicos_user(current_user, email):
    try:
        # Primeiro busca o usuário pelo email
        usuario = Usuarios.query.filter_by(email=email).first_or_404()
        
        # Busca os atendimentos do usuário encontrado
        servicosUsuario = Atendimentos.query.filter_by(usuario_id=usuario.id)\
            .join(Servicos, Atendimentos.servico_id == Servicos.id)\
            .add_columns(
                Atendimentos.data,
                Servicos.nome.label('servico_nome')
            ).all()
        
        # Formata o resultado para retornar como JSON
        resultado = [{
            'data': atendimento.data.strftime('%Y-%m-%d'),
            'hora': atendimento.data.strftime('%H:%M'),
            'servico': atendimento.servico_nome
        } for atendimento in servicosUsuario]
        
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar serviços do usuário!'}), 404

@app.route('/auth/agendar', methods=['POST'])
@token_required
def agendar(current_user):
    data = request.json

    try:
        # Formata a data e hora recebidas e converte para objeto datetime
        dataFormatada = datetime.datetime.strptime(f'{data["data"]} {data["horario"]}', '%Y-%m-%d %H:%M')
        
        # Busca o usuário pelo email
        usuario = Usuarios.query.filter_by(email=data['email']).first_or_404()
        
        # Busca o serviço pelo nome
        servico = Servicos.query.filter_by(nome=data['servico']).first_or_404()
        
        # Cria o novo agendamento com os IDs corretos e o objeto datetime
        agendamento = Atendimentos(
            usuario_id=usuario.id,
            servico_id=servico.id,
            data=dataFormatada
        )
        
        db.session.add(agendamento)
        db.session.commit()

        return jsonify({'message': 'Agendamento realizado com sucesso!'})
    except Exception as e:
        return jsonify({'message': f'Erro ao agendar serviço: {str(e)}'}), 500

@app.route('/auth/meus-agendamentos', methods=['PUT'])
@token_required
def meus_agendamentos(current_user):
    if not request.is_json:
        return jsonify({
            'error': 'Content-Type deve ser application/json'
        }), 400
    
    dados = request.get_json()
    
    nome_servico = dados.get('servico')
    hora = dados.get('hora')
    data = dados.get('data')
    email = dados.get('email')
    
    try:
        # Busca o ID do serviço pelo nome
        servico = Servicos.query.filter_by(nome=nome_servico).first()
        if not servico:
            return jsonify({'error': 'Serviço não encontrado'}), 404
            
        # Busca o ID do usuário pelo email
        usuario = Usuarios.query.filter_by(email=email).first()
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        # Formata data e hora para datetime
        data_agendamento = datetime.datetime.strptime(f"{data} {hora}", "%Y-%m-%d %H:%M")
        
        # Busca o atendimento existente apenas por usuario_id e servico_id
        atendimento = Atendimentos.query.filter_by(
            usuario_id=usuario.id,
            servico_id=servico.id
        ).first()
        
        if atendimento:
            # Atualiza apenas a data do atendimento
            atendimento.data = data_agendamento
            
            db.session.commit()
            
            return jsonify({
                'message': 'Atendimento atualizado com sucesso!'
            }), 200
        else:
            return jsonify({
                'error': 'Atendimento não encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'error': 'Erro ao atualizar atendimento',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
