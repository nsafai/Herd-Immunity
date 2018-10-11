import unittest
import person
from virus import Virus

class PersonTest(unittest.TestCase):
   def test_is_alive_and_is_vaccinated(self):
       testPerson = person.Person(1, True)
       assert testPerson.is_vaccinated == True
       assert testPerson.is_alive == True

   def test_is_alive_and_is_not_vaccinated(self):
       testPerson = person.Person(1, False)
       assert testPerson.is_vaccinated == False
       assert testPerson.is_alive == True

   def test_died_from_infection(self):
       infection = Virus("SuperDeadlyVirus", 1.1, 0.1) # Virus(name, mortality_rate, reproduction_rate)
       testPerson = person.Person(1, False, infection)
       testPerson.did_survive_infection()
       assert testPerson.is_alive == False

   def test_did_not_die_from_infection(self):
       infection = Virus("UselessVirus", 0, 0.1) # Virus(name, mortality_rate, reproduction_rate)
       testPerson = person.Person(1, False, infection)
       testPerson.did_survive_infection()
       assert testPerson.is_alive == True
