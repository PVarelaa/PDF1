from django.db import models

class PDF(models.Model):
    nombre = models.CharField(max_length=100,blank=True, null=True)
    materia = models.CharField(max_length=100,blank=True, null=True)
    condicion= models.CharField(max_length=20,blank=True, null=True)
    carrera = models.CharField(max_length=100,blank=True, null=True)     
    curso= models.CharField(max_length=20,blank=True, null=True)
    semestre = models.CharField(max_length=20, null=True, blank=True)
    requisitos= models.CharField(max_length=100,blank=True, null=True)
    codigo = models.CharField(max_length=20,blank=True, null=True)
    cargasemanal= models.CharField(max_length=100,blank=True, null=True)
    cargasemestral= models.CharField(max_length=100,blank=True, null=True)
    
    fundamentacion= models.TextField(null=True, blank=True)
    objetivos = models.TextField(null=True, blank=True)#Para textos largos como fundamentos, bibliografia, etc
    contenido= models.TextField(null=True, blank=True)
    metodologia =models.TextField(null=True, blank=True)
    evaluacion =models.TextField(null=True, blank=True)
    bibliografia=models.TextField(null=True, blank=True)

    def __str__(self):
        return self.archivo
