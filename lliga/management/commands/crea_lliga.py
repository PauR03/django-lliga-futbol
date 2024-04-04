from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from random import randint
    
from lliga.models import *
    
faker = Faker(["es_CA","es_ES"])
    
class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'
    
    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)
    
    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        lliga = Lliga.objects.filter(nom=titol_lliga)
        if lliga.count()>0:
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return
    
        print("Creem la nova lliga: {}".format(titol_lliga))
        lliga = Lliga(nom=titol_lliga)
        lliga.save()
    
        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
        for i in range(20):
            prefix = prefixos[randint(0,len(prefixos)-1)]
            if prefix:
                prefix += " "
            nom =  prefix + faker.city()
            equip = Equip(nom=nom)
            #print(equip)
            equip.save()
            equip.lligues.add(lliga)
    
            print("Creem jugadors de l'equip "+nom)
            for j in range(25):
                nom = faker.first_name()
                cognom1 = faker.last_name()
                cognom2 = faker.last_name()
                nomComplet = nom + " " + cognom1 + " " + cognom2
                edat = randint(18,40)
                jugador = Jugador(nom=nomComplet,edat=edat,equip=equip)
                #print(jugador)
                jugador.save()
    
        print("Creem partits de la lliga")
        for local in lliga.equip_set.all():
            for visitant in lliga.equip_set.all():
                if local!=visitant:
                    partit = Partit(local=local,visitant=visitant)
                    partit.local = local
                    partit.visitant = visitant
                    partit.lliga = lliga
                    partit.save()

                    gols_local = randint(0, 10)
                    gols_visitant = randint(0, 10)
                    for i in range(0,gols_local):
                        jugador = local.jugador_set.all()[randint(0,24)]
                        gol = Event(
                            tipus=Event.EventType.GOL,
                            jugador=jugador,
                            equip=local,
                            temps=timezone.now(),
                            partit=partit

                        )
                        gol.save()
                        partit.event_set.add(gol)
                    for i in range(0,gols_visitant):
                        jugador = visitant.jugador_set.all()[randint(0,24)]
                        gol = Event(
                            tipus=Event.EventType.GOL,
                            jugador=jugador,
                            equip=visitant,
                            temps=timezone.now(),
                            partit=partit
                        )
                        gol.save()

                        partit.event_set.add(gol)


