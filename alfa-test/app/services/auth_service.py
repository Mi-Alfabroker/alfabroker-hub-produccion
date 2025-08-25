import jwt
import bcrypt
from datetime import datetime, timedelta
from app.config import Config
from app.models.agente_model import Agente
from app.models.cliente_model import Cliente
from app import db

class AuthService:
    """Servicio de autenticación para manejo de JWT y contraseñas"""
    
    # Clave secreta para JWT (en producción debe estar en variables de entorno)
    JWT_SECRET_KEY = Config.SECRET_KEY
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = 24

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera un hash seguro de la contraseña
        
        Args:
            password (str): Contraseña en texto plano
            
        Returns:
            str: Hash de la contraseña
        """
        # Generar salt y hash de la contraseña
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña coincide con su hash
        
        Args:
            password (str): Contraseña en texto plano
            hashed_password (str): Hash almacenado
            
        Returns:
            bool: True si la contraseña es correcta
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def generate_token(user_data: dict, user_type: str) -> str:
        """
        Genera un token JWT con la información del usuario
        
        Args:
            user_data (dict): Datos del usuario (sin contraseña)
            user_type (str): Tipo de usuario ('agente' o 'cliente')
            
        Returns:
            str: Token JWT
        """
        # Preparar payload del token
        payload = {
            'user_id': user_data['id'],
            'user_type': user_type,  # 'agente' o 'cliente'
            'usuario': user_data['usuario'],
            'nombre': user_data.get('nombre'),
            'correo': user_data.get('correo'),
            'iat': datetime.utcnow(),  # Issued at
            'exp': datetime.utcnow() + timedelta(hours=AuthService.JWT_EXPIRATION_HOURS)  # Expiration
        }
        
        # Agregar campos específicos según el tipo de usuario
        if user_type == 'agente':
            payload['rol'] = user_data.get('rol')
            payload['activo'] = user_data.get('activo')
        elif user_type == 'cliente':
            payload['tipo_cliente'] = user_data.get('tipo_cliente')
            payload['razon_social'] = user_data.get('razon_social')
            payload['ciudad'] = user_data.get('ciudad')
        
        # Generar token
        token = jwt.encode(payload, AuthService.JWT_SECRET_KEY, algorithm=AuthService.JWT_ALGORITHM)
        return token

    @staticmethod
    def decode_token(token: str) -> dict:
        """
        Decodifica y valida un token JWT
        
        Args:
            token (str): Token JWT
            
        Returns:
            dict: Payload del token si es válido
            
        Raises:
            jwt.ExpiredSignatureError: Si el token ha expirado
            jwt.InvalidTokenError: Si el token no es válido
        """
        try:
            payload = jwt.decode(token, AuthService.JWT_SECRET_KEY, algorithms=[AuthService.JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token ha expirado")
        except jwt.InvalidTokenError:
            raise ValueError("Token inválido")

    @staticmethod
    def authenticate_agente(usuario: str, password: str) -> tuple:
        """
        Autentica un agente y genera token JWT
        
        Args:
            usuario (str): Nombre de usuario
            password (str): Contraseña
            
        Returns:
            tuple: (success: bool, data: dict, message: str)
        """
        try:
            # Buscar agente por usuario
            agente = Agente.query.filter_by(usuario=usuario).first()
            
            if not agente:
                return False, None, "Usuario no encontrado"
            
            # Verificar contraseña
            if not AuthService.verify_password(password, agente.clave):
                return False, None, "Contraseña incorrecta"
            
            # Verificar que el agente esté activo
            if not agente.activo:
                return False, None, "Cuenta desactivada"
            
            # Generar token
            user_data = agente.to_dict()
            token = AuthService.generate_token(user_data, 'agente')
            
            # Preparar respuesta (sin contraseña)
            response_data = user_data.copy()
            if 'clave' in response_data:
                del response_data['clave']
            
            return True, {
                'agente': response_data,
                'token': token,
                'expires_in': AuthService.JWT_EXPIRATION_HOURS * 3600  # en segundos
            }, "Login exitoso"
            
        except Exception as e:
            return False, None, f"Error en autenticación: {str(e)}"

    @staticmethod
    def authenticate_cliente(usuario: str, password: str) -> tuple:
        """
        Autentica un cliente y genera token JWT
        
        Args:
            usuario (str): Nombre de usuario
            password (str): Contraseña
            
        Returns:
            tuple: (success: bool, data: dict, message: str)
        """
        try:
            # Buscar cliente por usuario
            cliente = Cliente.query.filter_by(usuario=usuario).first()
            
            if not cliente:
                return False, None, "Usuario no encontrado"
            
            # Verificar contraseña
            if not AuthService.verify_password(password, cliente.clave):
                return False, None, "Contraseña incorrecta"
            
            # Generar token
            user_data = cliente.to_dict()
            token = AuthService.generate_token(user_data, 'cliente')
            
            # Preparar respuesta (sin contraseña)
            response_data = user_data.copy()
            if 'clave' in response_data:
                del response_data['clave']
            
            return True, {
                'cliente': response_data,
                'token': token,
                'expires_in': AuthService.JWT_EXPIRATION_HOURS * 3600  # en segundos
            }, "Login exitoso"
            
        except Exception as e:
            return False, None, f"Error en autenticación: {str(e)}"

    @staticmethod
    def refresh_token(token: str) -> tuple:
        """
        Refresca un token JWT válido
        
        Args:
            token (str): Token actual
            
        Returns:
            tuple: (success: bool, new_token: str, message: str)
        """
        try:
            # Decodificar token actual
            payload = AuthService.decode_token(token)
            
            # Verificar que no esté muy próximo a expirar (menos de 1 hora)
            exp_timestamp = payload.get('exp')
            if exp_timestamp:
                exp_datetime = datetime.fromtimestamp(exp_timestamp)
                if exp_datetime - datetime.utcnow() > timedelta(hours=1):
                    return False, None, "Token aún válido, no necesita renovación"
            
            # Buscar usuario actual
            user_type = payload.get('user_type')
            user_id = payload.get('user_id')
            
            if user_type == 'agente':
                user = Agente.query.get(user_id)
            elif user_type == 'cliente':
                user = Cliente.query.get(user_id)
            else:
                return False, None, "Tipo de usuario inválido"
            
            if not user:
                return False, None, "Usuario no encontrado"
            
            # Generar nuevo token
            user_data = user.to_dict()
            new_token = AuthService.generate_token(user_data, user_type)
            
            return True, new_token, "Token renovado exitosamente"
            
        except Exception as e:
            return False, None, f"Error al renovar token: {str(e)}" 