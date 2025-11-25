from django.db import models

class Propietario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    direccion_propietario = models.CharField(max_length=255)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class ClienteInmobiliaria(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    preferencias_propiedad = models.TextField(blank=True, null=True)
    presupuesto_maximo = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class AgenteInmobiliario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    licencia_agente = models.CharField(max_length=50, unique=True)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    comision_porcentaje = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Propiedad(models.Model):
    # Relación Muchos a Uno con Propietario
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='propiedades')
    
    direccion = models.CharField(max_length=255)
    tipo_propiedad = models.CharField(max_length=50)  # Podrías usar choices=... aquí
    num_habitaciones = models.IntegerField()
    num_banos = models.IntegerField()
    superficie_m2 = models.DecimalField(max_digits=10, decimal_places=2)
    # Permitimos null/blank porque una propiedad podría ser solo venta o solo alquiler
    precio_venta = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    precio_alquiler = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    estado_propiedad = models.CharField(max_length=50)
    fecha_publicacion = models.DateField()
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_propiedad} en {self.direccion}"

class VisitaPropiedad(models.Model):
    # Relaciones Muchos a Uno
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, related_name='visitas')
    cliente = models.ForeignKey(ClienteInmobiliaria, on_delete=models.CASCADE, related_name='visitas')
    agente = models.ForeignKey(AgenteInmobiliario, on_delete=models.SET_NULL, null=True, related_name='visitas_gestionadas')
    
    fecha_visita = models.DateField()
    hora_visita = models.TimeField()
    comentarios_cliente = models.TextField(blank=True, null=True)
    calificacion_propiedad = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Visita a {self.propiedad} por {self.cliente}"

class ContratoVenta(models.Model):
    # Relación Uno a Uno con Propiedad
    propiedad = models.OneToOneField(Propiedad, on_delete=models.PROTECT, related_name='contrato_venta')
    # Relaciones Muchos a Uno
    propietario = models.ForeignKey(Propietario, on_delete=models.PROTECT)
    cliente = models.ForeignKey(ClienteInmobiliaria, on_delete=models.PROTECT)
    agente = models.ForeignKey(AgenteInmobiliario, on_delete=models.PROTECT)
    
    fecha_contrato = models.DateField()
    precio_final = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_cierre = models.DateField(null=True, blank=True)
    estado_contrato = models.CharField(max_length=50)
    comision_agente = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta - {self.propiedad.direccion}"

class ContratoAlquiler(models.Model):
    # Relación Uno a Uno con Propiedad
    propiedad = models.OneToOneField(Propiedad, on_delete=models.PROTECT, related_name='contrato_alquiler')
    # Relaciones Muchos a Uno
    propietario = models.ForeignKey(Propietario, on_delete=models.PROTECT)
    cliente = models.ForeignKey(ClienteInmobiliaria, on_delete=models.PROTECT)
    agente = models.ForeignKey(AgenteInmobiliario, on_delete=models.PROTECT)
    
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    monto_alquiler_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    estado_contrato = models.CharField(max_length=50)
    deposito_garantia = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Alquiler - {self.propiedad.direccion}"
