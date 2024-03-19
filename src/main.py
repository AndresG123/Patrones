class User:
    def __init__(self, user_id, user_type, email, password):
        self.user_id = user_id
        self.user_type = user_type
        self.email = email
        self.password = password

class BaseHandler:
    def __init__(self, successor=None):
        self._successor = successor

    def handle_request(self, request):
        if self._successor is not None:
            self._successor.handle_request(request)
           

class AuthenticationManager(BaseHandler):
    def handle_request(self, request):
        if request.get("email") == "usuario" and request.get("password") == "contraseña":
            print('------------------------')
            print("Autenticación exitosa.")
            print('------------------------\n')
            # return True
            super().handle_request(request)
        else:
            print("Autenticación fallida.")
            return False

class DataSanitization(BaseHandler):
    def handle_request(self, request):
        if all(key in request for key in ["email", "password"]):
            print("Datos válidos y saneados.")
            # return True
            super().handle_request(request)
        else:
            print("Datos inválidos.")
            return False

class BruteForceProtection(BaseHandler): 
    #2 -> ip address 3-> Numero de intentos
    failed_attempts = {2:3}

    def handle_request(self, request):
        ip = request.get("ip")
        if ip in BruteForceProtection.failed_attempts:
            if BruteForceProtection.failed_attempts[ip] >= 3:
                print("Se han excedido los intentos fallidos desde esta IP.")
                return False
            else:
                BruteForceProtection.failed_attempts[ip] += 1
                print("Intento de acceso fallido.")
                return True
        else:
            super().handle_request(request)


class CacheManager(BaseHandler):
    cache = {}

    def handle_request(self, request):
        if request.get("cache_key") in CacheManager.cache:
            print("Respuesta obtenida de la caché.")
            super().handle_request(request)
        else:
            CacheManager.cache[request.get("cache_key")] = {'usuario': request.get("id"),'email':request.get("email"), 'password':request.get('password')}
            print("Respuesta almacenada en caché.")


            super().handle_request(request)
    




def main():
    # Crear instancias de las clases
    user = User(user_id=1, user_type='admin', email='usuario', password='contraseña')
    authentication_manager = AuthenticationManager()
    data_sanitization = DataSanitization()
    brute_force_protection = BruteForceProtection()
    cache_manager = CacheManager()

    # Configurar la cadena de responsabilidad
    authentication_manager._successor = data_sanitization
    data_sanitization._successor = brute_force_protection
    brute_force_protection._successor = cache_manager


    request = {'id':user.user_id,'email':user.email, 'password':user.password, 'usuario_tipo':user.user_type,'cache_key':1,'ip':1}  # Aquí irían los datos de la solicitud
    authentication_manager.handle_request(request)

    request = {'id':user.user_id,'email':user.email, 'password':user.password, 'usuario_tipo':user.user_type,'cache_key':1,'ip':1}  # Aquí irían los datos de la solicitud
    authentication_manager.handle_request(request)
    
    request = {'id':user.user_id,'email':user.email, 'password':user.password, 'usuario_tipo':user.user_type,'cache_key':1,'ip':2}  # Aquí irían los datos de la solicitud
    authentication_manager.handle_request(request)


if __name__ == "__main__":
    main()