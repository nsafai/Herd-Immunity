import random
import simulation
import logger
import virus


class Person(object):
    '''
    __init__(self, _id, is_vaccinated, infection=None):
        - self.alive should be automatically set to true during instantiation.
        - all other attributes for self should be set to their corresponding parameter
            passed during instantiation.
        - If person is chosen to be infected for first round of simulation, then
            the object should create a Virus object and set it as the value for
            self.infection.  Otherwise, self.infection should be set to None.
    '''

    def __init__(self, _id, is_vaccinated, infection=None):

        self._id = _id  # Int.  A unique ID assigned to each person.
        # Bool. Determines whether the person object is vaccinated against the disease in the simulation.
        self.is_vaccinated = is_vaccinated
        # Bool. All person objects begin alive (value set to true).  Changed to false if person object dies from an infection.
        self.is_alive = True
        # None or Virus object.  Set to None for people that are not infected. If a person is infected, will instead be set to the virus object the person is infected with.
        self.infection = infection


    '''
    did_survive_infection(self):
        - Only called if infection attribute is not None.
        - Takes no inputs.
        - Generates a random number between 0 and 1.
        - Compares random number to mortality_rate attribute stored in person's infection
            attribute.
            - If random number is smaller, person has died from disease.
                is_alive is changed to false.
            - If random number is larger, person has survived disease.  Person's
            is_vaccinated attribute is changed to True, and set self.infection to None.
    '''


    def did_survive_infection(self):
        random_number = random.random()
        if self.infection != None:
            if random_number < self.infection.mortality_rate:
                self.is_alive = False
                return False
            else:
                self.is_vaccinated = True
                self.infection = None
                return True
