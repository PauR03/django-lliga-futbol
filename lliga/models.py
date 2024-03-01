from django.db import models

class Lliga(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"Lliga {self.nom}"

class Equip(models.Model):
    nom = models.CharField(max_length=100)
    lligues = models.ManyToManyField(Lliga)

    def __str__(self):
        return f"{self.nom}"

class Jugador(models.Model):
    nom = models.CharField(max_length=100)
    edat = models.IntegerField()
    nacionalitat = models.CharField(max_length=100)
    equip = models.ForeignKey(Equip, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom}"

class Partit(models.Model):
    class Meta:
        unique_together = ["local","visitant","lliga"]
    local = models.ForeignKey(Equip,on_delete=models.CASCADE, related_name="partits_local",null=True)
    visitant = models.ForeignKey(Equip,on_delete=models.CASCADE, related_name="partits_visitant",null=True)
    lliga = models.ForeignKey(Lliga, on_delete=models.CASCADE,null=True)
    detalls = models.TextField(null=True,blank=True)
    inici = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return "{} - {}".format(self.local,self.visitant)
    def gols_local(self):
        return self.event_set.filter(
            tipus=Event.EventType.GOL,equip=self.local).count()
    def gols_visitant(self):
        return self.event_set.filter(
            tipus=Event.EventType.GOL,equip=self.visitant).count()



class Event(models.Model):
    # el tipus d'event l'implementem amb algo tipus "enum"
    class EventType(models.TextChoices):
        GOL = "GOL"
        AUTOGOL = "AUTOGOL"
        FALTA = "FALTA"
        PENALTY = "PENALTY"
        MANS = "MANS"
        CESSIO = "CESSIO"
        FORA_DE_JOC = "FORA_DE_JOC"
        ASSISTENCIA = "ASSISTENCIA"
        TARGETA_GROGA = "TARGETA_GROGA"
        TARGETA_VERMELLA = "TARGETA_VERMELLA"
    partit = models.ForeignKey(Partit,on_delete=models.CASCADE)
    temps = models.TimeField()
    tipus = models.CharField(max_length=30,choices=EventType.choices)
    jugador = models.ForeignKey(Jugador,null=True, on_delete=models.SET_NULL, related_name="events_fets")
    equip = models.ForeignKey(Equip,null=True, on_delete=models.SET_NULL)
    # per les faltes
    jugador2 = models.ForeignKey(Jugador,null=True,blank=True, on_delete=models.SET_NULL, related_name="events_rebuts")
    detalls = models.TextField(null=True,blank=True)