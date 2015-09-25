# coding: utf-8
u""" Module description.
"""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

# 3rdparty
from django.db import models

# Recordpack
from recordpack.provider import BaseProxy

# Employees
from models import Employee

#------------------------------------------------------------------------------
# Proxies
#------------------------------------------------------------------------------

class EmployeeListProxy(BaseProxy):
    def load(self, root):
        self.from_root()
        self.employee_full_name = root.employee.fullname
        self.position_name = root.position.pname


class EmployeeCardProxy(BaseProxy):
    def load(self, root):
        self.from_root()

    def save(self):
        employee_id = self.employee_id
        position_id = self.position_id
        person_model = models.get_model('demo', 'Person')
        position_model = models.get_model('positions', 'Position')

        try:
            new_employee = Employee(
                employee=person_model.objects.get(pk=employee_id),
                position=position_model.objects.get(pk=position_id),
            )
        except person_model.DoesNotExist:
            print "Trying to add employee_id that doesn't exist"
        except position_model.DoesNotExist:
            print "Trying to add position_id that doesn't exist"


        try:
            old_employee = Employee.objects.get(employee=new_employee.employee)
        except Employee.DoesNotExist:
            new_employee.save()
        else:
            old_employee.position = new_employee.position
            old_employee.save()
