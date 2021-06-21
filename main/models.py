# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Perfume(models.Model):
    nombre = models.CharField("Nombre", max_length=100)
    cantidad = models.CharField("Cantidad", max_length=100)
    precio = models.CharField("Precio", max_length=100)

    def __str__(self):
        return self.nombre + " (" + self.cantidad + ')'


class Usuario(models.Model):
    anyo_nacimiento = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2021)])
    pais = models.CharField("País", max_length=100)

    def __str__(self):
        return self.anyo_nacimiento + " " + self.pais


class Puntuacion(models.Model):
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    perfume_id = models.ForeignKey(Perfume, on_delete=models.CASCADE)
    puntuacion = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return str(self.puntuacion)
