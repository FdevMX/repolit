# Utilidad para manejar contraseñas
import hashlib
import os
import binascii

def hash_password(password):
    """Crea un hash seguro para una contraseña."""
    # Genera un salt aleatorio
    salt = os.urandom(32)
    # Crea un hash con el salt
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # Convierte a hexadecimal para almacenamiento
    return binascii.hexlify(salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
    # Convierte el hash almacenado de nuevo a bytes
    binary = binascii.unhexlify(stored_password)
    # Extrae el salt (primeros 32 bytes)
    salt = binary[:32]
    # Extrae el hash original
    stored_hash = binary[32:]
    # Calcula el hash de la contraseña proporcionada
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    # Compara los hashes
    return pwdhash == stored_hash