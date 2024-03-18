class User:
    def __init__(self, user_id, user_type, email):
        self.user_id = user_id
        self.user_type = user_type
        self.email = email

class BaseHandler:
    def __init__(self, successor=None):
        self._successor = successor

    def handle_request(self, request):
        if self._successor is not None:
            return self._successor.handle_request(request)
        return True

class AuthenticationManager(BaseHandler):
    def handle_request(self, request):
        if request.get("email") == "usuario" and request.get("password") == "contraseña":
            print("Autenticación exitosa.")
            return True
        else:
            print("Autenticación fallida.")
            return False

class DataSanitization(BaseHandler):
    def handle_request(self, request):
        if all(key in request for key in ["email", "password"]):
            print("Datos válidos y saneados.")
            return True
        else:
            print("Datos inválidos.")
            return False

class BruteForceProtection(BaseHandler):
    def __init__(self):
        self.failed_attempts = {}

    def handle_request(self, request):
        ip = request.get("ip")
        if ip in self.failed_attempts:
            if self.failed_attempts[ip] >= 3:
                print("Se han excedido los intentos fallidos desde esta IP.")
                return False
            else:
                self.failed_attempts[ip] += 1
                print("Intento de acceso fallido.")
                return True
        else:
            self.failed_attempts[ip] = 1
            print("Intento de acceso fallido.")
            return True

class CacheManager(BaseHandler):
    def __init__(self):
        self.cache = {}

    def handle_request(self, request):
        if request.get("cache_key") in self.cache:
            print("Respuesta obtenida de la caché.")
            return True
        else:
            self.cache[request.get("cache_key")] = request.get("response")
            print("Respuesta almacenada en caché.")
            return True

def main():
    # Crear instancias de las clases
    user = User(user_id=1, user_type='admin', email='example@example.com')
    authentication_manager = AuthenticationManager()
    data_sanitization = DataSanitization()
    brute_force_protection = BruteForceProtection()
    cache_manager = CacheManager()

    # Configurar la cadena de responsabilidad
    authentication_manager._successor = data_sanitization
    data_sanitization._successor = brute_force_protection
    brute_force_protection._successor = cache_manager

    request = {}  # Aquí irían los datos de la solicitud
    if authentication_manager.handle_request(request):
        print("Solicitud procesada con éxito.")
    else:
        print("La solicitud ha sido rechazada.")

if __name__ == "__main__":
    main()
