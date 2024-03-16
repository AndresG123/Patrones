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
        # lógica de autenticación
        print("Autenticando usuario...")
        #autenticación exitosa
        return True

class DataSanitization(BaseHandler):
    def handle_request(self, request):
        # lógica saneamiento de datos
        print("Validando y saneando datos...")
        return True

class BruteForceProtection(BaseHandler):
    def handle_request(self, request):
        # lógica de filtrado de solicitudes por IP
        print("Filtrando solicitudes por dirección IP...")
        return True

class CacheManager(BaseHandler):
    def handle_request(self, request):
        # lógica de gestión de caché
        print("Gestionando caché de respuestas...")
        return True

def main():
    # Crear instancias de las clases
    user = User(user_id=1, user_type='admin', email='example@example.com')
    authentication_manager = AuthenticationManager()
    data_sanitization = DataSanitization()
    brute_force_protection = BruteForceProtection()
    cache_manager = CacheManager()

    authentication_manager._successor = data_sanitization
    data_sanitization._successor = brute_force_protection
    brute_force_protection._successor = cache_manager

    #solicitud de orden
    request = {}  # datos de la solicitud pendientes
    if authentication_manager.handle_request(request):
        print("Solicitud procesada con éxito.")
    else:
        print("La solicitud ha sido rechazada.")

if __name__ == "__main__":
    main()
