import random
import sys
random.seed(42)
import person
from logger import Logger
import virus


'''
Main class that will run the herd immunity simulation program.  Expects initialization
parameters passed as command line arguments when file is run.

Simulates the spread of a virus through a given population.  The percentage of the
population that are vaccinated, the size of the population, and the amount of initially
infected people in a population are all variables that can be set when the program is run.

'''


class Simulation(object):

    '''
    __init__(population_size, vacc_percentage, virus_name, mortality_rate,
     basic_repro_num, initial_infected=1):
        -- All arguments will be passed as command-line arguments when the file is run.
        -- After setting values for attributes, calls self._create_population() in order
            to create the population array that will be used for this simulation.
    '''

    def __init__(self, population_size, vacc_percentage, virus, initial_infected=1, total_dead=0):

        # Int.  The size of the population for this simulation.
        self.population_size = population_size
        # [Person].  A list of person objects representing all people in the population.
        self.population = []
        # Int.  The running total of people that have been infected since the simulation began, including any people currently infected.
        self.total_infected = initial_infected
        # Int.  The number of currently people in the population currently infected with the disease in the simulation.
        self.current_infected = initial_infected
        # Int.  The next available id value for all created person objects. Each person should have a unique _id value.
        self.next_person_id = 0
        # Float between 0 and 1.  Represents the total percentage of population vaccinated for the given simulation.
        self.vacc_percentage = vacc_percentage
        # String.  The name of the virus for the simulation.  This will be passed to the Virus object upon instantiation.
        self.virus_name = virus.name
        # Float between 0 and 1.  This will be passed to the Virus object upon instantiation.
        self.mortality_rate = virus.mortality_rate
        # Float between 0 and 1.   This will be passed to the Virus object upon instantiation.
        self.basic_repro_num = virus.basic_repro_num
        self.virus = virus
        # Int.  The number of people that have died as a result of the infection during this simulation.  Starts at zero.
        self.total_dead = total_dead
        self.total_alive = population_size - total_dead
        self.total_interactions_between_vaccinated_and_infected = 0
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(virus.name, population_size, vacc_percentage, initial_infected)

        # TCreate a Logger object and bind it to self.logger to log all events of any importance during the simulation.
        self.logger = Logger(self.file_name)
        self.logger.write_metadata(population_size, vacc_percentage, virus.name, virus.mortality_rate, virus.basic_repro_num)

        # This attribute will be used to keep track of all the people that catch
        # the infection during a given time step. We'll store each newly infected
        # person's .ID attribute in here.  At the end of each time step, we'll call
        # self._infect_newly_infected() and then reset .newly_infected back to an empty
        # list.
        self.newly_infected = []
        # Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.
        self.population += self._create_population(initial_infected)

    '''
    _create_population(self, initial_infected):
        -- Expects initial_infected as an Int.
        -- Should be called only once, at the end of the __init__ method.
        -- Stores all newly created Person objects in a local variable, population.
        -- Creates all infected person objects first.  Each time a new one is created,
            increments infected_count variable by 1.
        -- Once all infected person objects are created, begins creating healthy
            person objects.  To decide if a person is vaccinated or not, generates
            a random number between 0 and 1.  If that number is smaller than
            self.vacc_percentage, new person object will be created with is_vaccinated
            set to True.  Otherwise, is_vaccinated will be set to False.
        -- Once len(population) is the same as self.population_size, returns population.
    '''

    def _create_population(self, initial_infected):
        #  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).
        population = []
        infected_count = 0
        while len(population) != pop_size:
            if infected_count != initial_infected:

                new_infected_person = person.Person(self.next_person_id, False, virus)
                population.append(new_infected_person)
                infected_count += 1
            else:
                # Every time a new person will be created, generate a random number between
                # 0 and 1.  If this number is smaller than vacc_percentage, this person
                # should be created as a vaccinated person. If not, the person should be
                # created as an unvaccinated person.
                chance_of_being_vaccinated = random.random()
                if chance_of_being_vaccinated < self.vacc_percentage:
                    population.append(person.Person(self.next_person_id, True))
                else:
                    population.append(person.Person(self.next_person_id, False))
                # After any Person object is created, whether sick or healthy,
                # you will need to increment self.next_person_id by 1. Each Person object's
                # ID has to be unique!
            self.next_person_id += 1

        return population

    def _simulation_should_continue(self):
        # This method should return True if the simulation
        # should continue, or False if it should not.  The simulation should end under
        # any of the following circumstances:
        #     - The entire population is dead.
        #     - There are no infected people left in the population.
        # In all other instances, the simulation should continue.

        # update counts
        alive_count = 0
        death_count = 0
        carriers_count = 0

        for person in self.population:
            if person.is_alive == True:
                alive_count += 1
                if person.infection is not None:
                    carriers_count += 1
            elif person.is_alive == False:
                death_count += 1

            self.total_dead = death_count
            self.total_alive = alive_count
            self.current_infected = carriers_count


        # print('next person id: {}'.format(self.next_person_id))
        print('__________________________________________________')
        print('population size: {}'.format(self.population_size))
        print('total alive: {}'.format(alive_count))
        print('total dead: {}'.format(self.total_dead))
        print('total_infected: {}'.format(self.total_infected))
        print('current_infected: {}'.format(self.current_infected))
        print('total interactions between vaccinated person and infected person {}'.format(self.total_interactions_between_vaccinated_and_infected))
        print('__________________________________________________')


        if self.total_dead == self.population_size or self.current_infected == 0:
            return False
        else:
            return True

    def run(self):
        # This method should run the simulation until
        # everyone in the simulation is dead, or the disease no longer exists in the
        # population. To simplify the logic here, we will use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # This method should keep track of the number of time steps that
        # have passed using the time_step_counter variable.  Make sure you remember to
        # the logger's log_time_step() method at the end of each time step, pass in the
        # time_step_counter variable!

        time_step_counter = 0

        should_continue = self._simulation_should_continue()
        print(should_continue)
        while should_continue:
            # for every iteration of this loop, call self.time_step() to compute another
            # round of this simulation.  At the end of each iteration of this loop, remember
            # to rebind should_continue to another call of self._simulation_should_continue()!
            self.time_step()
            print(time_step_counter)
            time_step_counter += 1
            self.logger.log_time_step(time_step_counter)
            should_continue = self._simulation_should_continue()

        print('The simulation has ended after {} turns.'.format(time_step_counter))
        self.logger.log_final_stats(self.total_dead, self.total_alive, self.total_infected, self.total_interactions_between_vaccinated_and_infected, self.population_size)

    def generate_random_alive_person(self, infected_person):
        random_person = random.choice(self.population)
        if random_person.is_alive and random_person != infected_person and random_person is not None:
            return random_person
        else:
            self.generate_random_alive_person(infected_person)


    def time_step(self):
        #  This method should contain all the basic logic
        # for computing one time step in the simulation.  This includes:
            # - For each infected person in the population:
            #        - Repeat for 100 total interactions:
            #             - Grab a random person from the population.
            #           - If the person is dead, continue and grab another new
            #                 person from the population. Since we don't interact
            #                 with dead people, this does not count as an interaction.
            #           - Else:
            #               - Call simulation.interaction(person, ra ndom_person)
            #               - Increment interaction counter by 1.

        for infected_person in self.population:
            if infected_person.infection is not None and infected_person.is_alive == True:
                interaction_counter = 0
                while interaction_counter < 100:
                    # grab a random person
                    random_alive_person = self.generate_random_alive_person(infected_person)
                    # print('infected person {} is interacting with {}'.format(infected_person, random_alive_person))
                    if random_alive_person is not None:
                        self.interaction(infected_person, random_alive_person)
                        interaction_counter += 1
                        # print('INTERACTION COUNTER: {}'.format(interaction_counter))
                if infected_person.did_survive_infection() == False:
                    infected_person.is_alive = False

        self._infect_newly_infected()


    def interaction(self, person, random_person):
        # This method should be called any time two living
        # people are selected for an interaction.  That means that only living people
        # should be passed into this method.  Assert statements are included to make sure
        # that this doesn't happen.
        assert person.is_alive == True
        assert random_person.is_alive == True

        if random_person.is_vaccinated is True:  # random_person is vaccinated:
            self.logger.log_interaction(person, random_person, person2_vacc=True)
            self.total_interactions_between_vaccinated_and_infected += 1
            return
        elif random_person.infection is not None:  # random_person is already infected
            self.logger.log_interaction(
                person, random_person, person2_sick=True)
            return
        else:  # random_person is healthy, but unvaccinated:
            # attribute can be changed to True at the end of the time step.
            # generate a random number between 0 and 1.
            random_number = random.random()
            if random_number < person.infection.basic_repro_num:  # If that number is smaller than basic_repro_num,
                # random person was infected via interaction
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(person, random_person, did_infect=True)
                return
            else:
                self.logger.log_interaction(person, random_person, did_infect=False)
                return

    def _infect_newly_infected(self):
        #  This method should be called at the end of
        # every time step.  This method should iterate through the list stored in
        # self.newly_infected, which should be filled with the IDs of every person
        # created.  Iterate though this list.
        # For every person id in self.newly_infected:
        #   - Find the Person object in self.population that has this corresponding ID.
        #   - Set this Person's .infected attribute to True.
        # Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list!

        for infected_person_id in self.newly_infected:
            for person in self.population:
                if person._id == infected_person_id:
                    person.infection = self.virus
        self.total_infected += len(self.newly_infected)
        print('newly infected: {}'.format(self.newly_infected))
        self.newly_infected = []


if __name__ == "__main__":
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1
    virus = virus.Virus(virus_name, mortality_rate, basic_repro_num)
    simulation = Simulation(pop_size, vacc_percentage, virus, initial_infected)
    simulation.run()
