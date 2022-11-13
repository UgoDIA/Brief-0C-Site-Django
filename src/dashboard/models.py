from django.db import models

# Create your models here.
class Projet(models.Model):
    codePr = models.AutoField(primary_key=True)
    initial = models.CharField(max_length=10)
    url = models.TextField()

    def __str__(self):
        return self.initial

class Histo(models.Model):
    projetId = models.ForeignKey(Projet, on_delete=models.CASCADE)
    idHisto = models.AutoField(primary_key=True)
    dateRel = models.DateField()
    nbThreadsRel = models.BigIntegerField()
    nbCommRel = models.BigIntegerField()
    status = models.BooleanField()

    def __int__(self):
        return self.idHisto

class Threads(models.Model):
    projetId = models.ForeignKey(Projet, on_delete=models.CASCADE)
    idThread = models.AutoField(primary_key=True)
    nomThread = models.TextField()

    def __str__(self):
        return self.nomThread

class Comments(models.Model):
    threadId = models.ForeignKey(Threads,  on_delete=models.CASCADE)
    idCom = models.AutoField(primary_key=True)
    comment = models.TextField()

    def __str__(self):
        return self.comment

class Statut(models.Model):
    idStatut = models.AutoField(primary_key=True)
    projetId = models.ForeignKey(Projet, on_delete=models.CASCADE)
    statut = models.TextField()

    def __str__(self):
        return self.statut
    
class Stopgo(models.Model):
    idStopgo = models.AutoField(primary_key=True)
    statutStopgo = models.TextField()

    def __str__(self):
        return self.statutStopgo
#Remplacer idStopgo par codeProjet pour dynamisme