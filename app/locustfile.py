from locust import HttpUser, task, between

class ClienteBehavior(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """ Simula la autenticación de un usuario cliente al iniciar la prueba. """
        self.client.post("/inicio_sesion/", {
            "username": "testuser", 
            "password": "testpass"
        })

    @task(2)
    def ver_productos(self):
        self.client.get("/productos/")

    @task(1)
    def solicitar_articulo(self):
        self.client.post("/solicitarArticulo/", {"product_id": 1})

    @task(3)
    def añadir_al_carrito(self):
        self.client.post("/add-to-cart/1/")

    @task(1)
    def realizar_pago(self):
        self.client.post("/process-payment/", {"order_id": 1})

    @task(1)
    def gestionar_perfil(self):
        self.client.post("/editar-usuario/", {
            "email": "testuser@example.com",
            "phone": "1234567890"
        })

    @task(1)
    def ver_ordenes(self):
        self.client.get("/orders/")

    @task(1)
    def reporte_productos_vendidos(self):
        self.client.get("/most-sold-products/")

    @task(1)
    def gestionar_entregas(self):
        self.client.get("/manage-deliveries/")

    @task(1)
    def actualizar_entrega(self):
        self.client.post("/update-delivery-status/1/", {"status": "Delivered"})

    @task(1)
    def gestionar_inventario(self):
        self.client.get("/inventory/")
