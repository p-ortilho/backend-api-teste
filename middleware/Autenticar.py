from functools import wraps
from flask import request, current_app
from model.Usuarios import Usuarios
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Verifica se existe Authorization no header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        
        # Se não existir, retorna mensagem de erro
        if not token:
            return {'message': 'Você não tem permissão para acessar essa rota!'}, 403

        # Se existir, verifica se o token é válido
        if 'Bearer' not in token:
            return {'message': 'Token inválido!'}, 401
        
        try:
            # Separa o token do Bearer
            token_puro = token.replace('Bearer ', '')
            
            # Decodifica o token
            decode_token = jwt.decode(token_puro, current_app.config['SECRET_KEY'], algorithms=['HS256'])

            # Id do usuario
            current_user = Usuarios.query.get(decode_token['id'])

            if current_user is None:
                return {'message': 'Usuário não encontrado!'}, 404
            
        except jwt.ExpiredSignatureError:
            return {'message': 'Token expirado!'}, 401
        
        except jwt.InvalidTokenError:
            return {'message': 'Token inválido!'}, 401
        
        return f(current_user=current_user, *args, **kwargs)
    
    return decorated