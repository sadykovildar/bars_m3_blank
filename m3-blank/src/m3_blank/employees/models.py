# coding: utf-8
u"""
Модели приложения
"""
#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------


# 3rdparty
from django.db import models

#------------------------------------------------------------------------------
# Models
#------------------------------------------------------------------------------

class Employee(models.Model):
    u"""
    Сотрудник
    """

    employee = models.ForeignKey(
        'demo.Person',
        verbose_name=u'ФИО сотрудника')
    position = models.ForeignKey(
        'positions.Position',
        verbose_name=u'Должность')


    # def get_emp_fullname(self):
    #    return u'{fname} {sname} {mname}'.format(
    #        self.employee_full_name['fname'],
    #        self.employee_full_name.sname,
    #        self.employee_full_name.mname,
    #    ).rstrip()

    @property
    def pos_name(self):
      return u'{pname}'.format(
            pname=self.position.pname
      ).rstrip()


    # Meta
    # -----------------------------------------------------------------

    class Meta:
        verbose_name = u'Сотрудник'
        verbose_name_plural = u'Список сотрудников'
