import person
from string import Template
import simulation
# looked at Wenzel's code for inspiration for this file https://github.com/lowewenzel/CS-1.1-Programming-Fundamentals/blob/master/Herd_Immunity_Project/logger.py


class Logger(object):
    '''
    Utility class responsible for logging all interactions of note during the
    simulation.
    '''

    def __init__(self, file_name):
        # Finish this initialization method.  The file_name passed should be the
        # full file name of the file that the logs will be written to.
        # file_name: the name of the file that the logger will be writing to.
        self.file_name = file_name

    '''
        write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
            basic_repro_num):
            - Writes the first line of a logfile, which will contain metadata on the
                parameters for the simulation.
    '''

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        # Finish this method.  The simulation class should use this method
        # immediately upon creation, to log the specific parameters of the simulation
        # as the first line of the file.  This line of metadata should be tab-delimited
        # (each item separated by a '\t' character).

        # ince this is the first method called, it will create the text file
        # that we will store all logs in.  Be sure to use 'w' mode when you open the file.
        # For all other methods, we'll want to use the 'a' mode to append our new log to the end,
        # since 'w' overwrites the file.
        # Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
        new_file = open(self.file_name, 'w')
        log_template = Template('''Virus Simulation Logger \n \tVirus Name: ${name} \nMortality rate: ${mortality}\nBasic Reproductive Rate: ${reproduction}\n\tPopulation: ${pop_size} \nNumber Vaccinated: ${vacc}\n''')
        new_file.write(log_template.substitute(name=virus_name, mortality=mortality_rate, reproduction=basic_repro_num, pop_size=pop_size, vacc=vacc_percentage))

        new_file.close()

    '''
    log_interaction(self, person1, person2, did_infect=None, person2_vacc=None, person2_sick=None):
        - Expects person1 and person2 as person objects.
        - Expects did_infect, person2_vacc, and person2_sick as Booleans, if passed.
        - Between the values passed with did_infect, person2_vacc, and person2_sick, this method
            should be able to determine exactly what happened in the interaction and create a String
            saying so.
        - The format of the log should be "{person1.ID} infects {person2.ID}", or, for other edge
            cases, "{person1.ID} didn't infect {person2.ID} because {'vaccinated' or 'already sick'}"
        - Appends the interaction to logfile.
    '''

    def log_interaction(self, person1, person2, did_infect = None,
                        person2_vacc =None, person2_sick=None):
        # Finish this method.  The Simulation object should use this method to
        # log every interaction a sick individual has during each time step.  This method
        # should accomplish this by using the information from person1 (the infected person),
        # person2 (the person randomly chosen for the interaction), and the optional
        # keyword arguments passed into the method.  See documentation for more info
        # on the format of the logs that this method should write.
        # You'll need to think
        # about how the booleans passed (or not passed) represent
        # all the possible edge cases!
        # Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
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

    '''
        log_infection_survival(self, person, did_die_from_infection):
            - Expects person as Person object.
            - Expects bool for did_die_from_infection, with True denoting they died from
                their infection and False denoting they survived and became immune.
            - The format of the log should be "{person.ID} died from infection" or
                "{person.ID} survived infection."
            - Appends the results of the infection to the logfile.
    '''

    def log_infection_survival(self, person, did_die_from_infection):
        # Finish this method.  The Simulation object should use this method to log
        # the results of every call of a Person object's .resolve_infection() method.
        # If the person survives, did_die_from_infection should be False.  Otherwise,
        # did_die_from_infection should be True.  See the documentation for more details
        # on the format of the log.
        # Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
        new_file= open(self.file_name, 'a')
        if did_die_from_infection:
            new_file.write(
                "\n***Person {} died from infection.***\n".format(person._id))
        else:
            new_file.write(
                "\n***Person {} survived infection. They are now immunized (=vaccinated).***\n".format(person._id))
        new_file.close()

    '''
    log_time_step(self, time_step_number):
        - Expects time_step_number as an Int.
        - This method should write a log telling us when one time step ends, and
            the next time step begins.  The format of this log should be:
                "Time step {time_step_number} ended, beginning {time_step_number + 1}..."
        - STRETCH CHALLENGE DETAILS:
            - If you choose to extend this method, the format of the summary statistics logged
                are up to you.  At minimum, it should contain:
                    - The number of people that were infected during this specific time step.
                    - The number of people that died on this specific time step.
                    - The total number of people infected in the population, including the newly
                        infected
                    - The total number of dead, including those that died during this time step.
    '''

    def log_time_step(self, time_step_number):
        # TODO: Finish this method.  This method should log when a time step ends, and a
        # new one begins.  See the documentation for more information on the format of the log.
        # NOTE: Stretch challenge opportunity! Modify this method so that at the end of each time
        # step, it also logs a summary of what happened in that time step, including the number of
        # people infected, the number of people dead, etc.  You may want to create a helper class
        # to compute these statistics for you, as a Logger's job is just to write logs!
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
        new_file= open(self.file_name, 'a')
        new_file.write(
            "\n---------------------FINISH TIME STEP---------------------")
        new_file.write("\n------------------ No:" + str(time_step_number) + "---------------------\n")
        new_file.close()
