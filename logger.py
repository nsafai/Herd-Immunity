import person
from string import Template
import simulation
# looked at Wenzel's code for inspiration for the file below, see his code here: https://github.com/lowewenzel/CS-1.1-Programming-Fundamentals/blob/master/Herd_Immunity_Project/logger.py


class Logger(object):
    # Utility class responsible for logging all interactions of note during the simulation.

    def __init__(self, file_name):

        self.file_name = file_name


    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        new_file = open(self.file_name, 'w')
        log_template = Template('''Virus Simulation Logger \n \tVirus Name: ${name} \nMortality rate: ${mortality}\nBasic Reproductive Rate: ${reproduction}\n\tPopulation: ${pop_size} \nNumber Vaccinated: ${vacc}\n''')
        new_file.write(log_template.substitute(name=virus_name, mortality=mortality_rate, reproduction=basic_repro_num, pop_size=pop_size, vacc=vacc_percentage))

        new_file.close()

    def log_interaction(self, person1, person2, did_infect = None,
                        person2_vacc =None, person2_sick=None):
        new_file= open(self.file_name, 'a')
        person1_id= str(person1._id)
        person2_id= str(person2._id)

        if person2_vacc == True:
            interaction_str= "Nothing happened because Person " + person2_id + " is vaccinated"
        elif person2_sick:
            interaction_str = "Nothing happened because Person " + person2_id + " is already infected"
        else:
            interaction_str = "Person " + person1_id + " INFECTED Person " + person2_id

        if did_infect:
            infect_str= "NOW INFECTED"
        else:
            infect_str= "SAFE"

        log_template= Template('''\n* Person $person1id interacts with Person ${person2id}\n* ${interaction_str}\n* Person $person2id is ${infect_str}\n''')
        final_string = log_template.substitute(person1id = person1_id, person2id = person2_id, interaction_str = interaction_str, infect_str =infect_str)
        new_file.write(final_string)
        new_file.close()

    def log_infection_survival(self, person, did_die_from_infection):
        new_file= open(self.file_name, 'a')
        if did_die_from_infection:
            new_file.write(
                "\n***Person {} died from infection.***\n".format(person._id))
        else:
            new_file.write(
                "\n***Person {} survived infection. They are now immunized (=vaccinated).***\n".format(person._id))
        new_file.close()

    def log_time_step(self, time_step_number):
        new_file= open(self.file_name, 'a')
        new_file.write(
            "\n---------------------FINISH TIME STEP---------------------")
        new_file.write("\n------------------ No:" + str(time_step_number) + "---------------------\n")
        new_file.close()

    def log_final_stats(self, total_dead, total_alive, total_infected, total_interactions_between_vaccinated_and_infected, population_size):
        new_file= open(self.file_name, 'a')
        new_file.write(
            "\n---------------------FINAL STATS---------------------\n")
        new_file.write("Starting Population Size: {}\n".format(population_size))
        new_file.write("Total Deaths: {}\nTotal Alive: {}\nTotal Infected (at some point): {}\n".format(total_dead, total_infected, total_infected))
        new_file.write("Total Interactions between someone vaccinated and someone infected: {}\n".format(total_interactions_between_vaccinated_and_infected))
        new_file.close()
