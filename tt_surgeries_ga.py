import prettytable as prettytable
import random as rnd

# Number of chromosomes in each generation - meaning the number of solutions
POPULATION_SIZE = 5

# Number of the best schedules (fittest) in each generation
NUM_OF_ELITE_SCHEDULES = 1

# Number of solutions we consider in the tournament selection
TOURNAMENT_SELECTION_SIZE = 3

# The mutation rate
MUTATION_PROBABILITY = 0.1

### Time-Tabling DATA ###
# Operatiog rooms - id, surgery types allowed
OPERATING_ROOMS = [["R1", "A1"], ["R2", "A2"], ["R3", "A3"]]

# Operations times - id, day & time
OPERATIONS_TIMES = [["OT1", "MWF 09:00 - 10:00"],
                   ["OT2", "MWF 10:00 - 11:00"],
                   ["OT3", "TTH 09:00 - 10:30"],
                   ["OT4", "TTH 10:30 - 12:00"]]

# Surgeons - id, full name                   
SURGEONS = [["Su1", "Dr. Captain America"],
            ["Su2", "Dr. Tony Stark"],
            ["Su3", "Dr. Black Panther"],
            ["Su4", "Prof. Thanos"]]

class Data:
    # Initialization of the data
    def __init__(self):
        self._operatingRooms = []; self._operationTimes = []; self._surgeons = []
        # Adding OPERATION ROOMS to the data
        for i in range (0, len(OPERATING_ROOMS)):
            self._operatingRooms.append(OperationRoom(OPERATING_ROOMS[i][0], OPERATING_ROOMS[i][1]))
        # Adding MEETING_TIMES to the data
        for i in range (0, len(OPERATIONS_TIMES)):
            self._operationTimes.append(OperationTime(OPERATIONS_TIMES[i][0], OPERATIONS_TIMES[i][1]))
        # Adding INSTRUCTORS to the data
        for i in range (0, len(SURGEONS)):
            self._surgeons.append(Surgeon(SURGEONS[i][0], SURGEONS[i][1]))
        # Creating surgeries and assigning surgeons to them
        surgery1 = Surgery("S1", "321K", [self._surgeons[0], self._surgeons[1]], "A1")
        surgery2 = Surgery("S2", "323K", [self._surgeons[0], self._surgeons[1], self._surgeons[2]], "A1")
        surgery3 = Surgery("S3", "461K", [self._surgeons[0], self._surgeons[1]], "A2")
        surgery4 = Surgery("S4", "464K", [self._surgeons[2], self._surgeons[3]], "A2")
        surgery5 = Surgery("S5", "360C", [self._surgeons[3]], "A2")
        surgery6 = Surgery("S6", "303K", [self._surgeons[0], self._surgeons[2]], "A3")
        surgery7 = Surgery("S7", "303L", [self._surgeons[2], self._surgeons[3]], "A3")
        # Adding surgeries to the data
        self._surgeries = [surgery1, surgery2, surgery3, surgery4, surgery5, surgery6, surgery7]
        # Creating wards and assigning surgeries to them
        ward1 = Ward("Orthopedic", [surgery1, surgery3])
        ward2 = Ward("Surgical", [surgery2, surgery4, surgery5])
        ward3 = Ward("Kids", [surgery6, surgery7])
        # Adding departments to the data
        self._wards = [ward1, ward2, ward3]
        self._numOfSurgeries = 0
        for i in range(0, len(self._wards)):
            self._numOfSurgeries += len(self._wards[i].get_surgeries())
    def get_operatingRooms(self): return self._operatingRooms
    def get_surgeons(self): return self._surgeons
    def get_surgeries(self): return self._surgeries
    def get_wards(self): return self._wards
    def get_operationTimes(self): return self._operationTimes
    def get_numOfSurgeries(self): return self._numOfSurgeries
class Schedule:
    def __init__(self):
        self._data = Data()
        self._operations = []
        self._numOfConflicts = 0
        self._fitness = -1
        self._operationNum = 0
        self._isFitnessChanged = True
    def get_numOfConflicts(self):
        return self._numOfConflicts
    def get_operations(self): 
        self._isFitnessChanged = True
        return self._operations
    def get_fitness(self): 
        if (self._isFitnessChanged == True):
            self._fitness = self.calculateFitness()
            self._isFitnessChanged = False
        return self._fitness
    # Initialization of the schedule
    def initialize(self):
        # Getting the wards from the data
        wards = self._data.get_wards()
        # Iterating over the wards
        for i in range(0, len(wards)):
            # For each ward, take the surgeries list
            surgeries = wards[i].get_surgeries()
            # Iterating over the courses of each department
            for j in range(0, len(surgeries)):
                # Creating an instance of Class for each course
                newOperation = Operation(self._operationNum, wards[i], surgeries[j])
                self._operationNum += 1
                # Setting a meeting time randomly from a given set of meeting times (in the data)
                newOperation.set_operationTime(data.get_operationTimes()[rnd.randrange(0, len(data.get_operationTimes()))])
                # Setting a room randomly from a given set of rooms (in the data)
                newOperation.set_operationRoom(data.get_operatingRooms()[rnd.randrange(0, len(data.get_operatingRooms()))])
                # Setting an instructor randomly from a given set of instructors of the specifuc ciyrse (in the data)
                newOperation.set_surgeon(surgeries[j].get_surgeons()[rnd.randrange(0, len(surgeries[j].get_surgeons()))])
                self._operations.append(newOperation)
        return self
    def calculateFitness(self):
        self._numOfConflicts = 0
        operations = self.get_operations()
        for i in range(0, len(operations)):
            # Conflict #1 - the operationRoom's surgery type doesn't fit the surgery type we assigned
            if (operations[i].get_operationRoom().get_surgeryType() != operations[i].get_surgery().get_surgeryType()):
                self._numOfConflicts += 1
            for j in range(0, len(operations)):
                # if (j >= i):
                if (operations[i].get_operationTime().get_time() == operations[j].get_operationTime().get_time() and operations[i].get_id() != operations[j].get_id()):
                    # Conflict #2 - in the same operation time there is a room which is occupied by 2 operations
                    if (operations[i].get_operationRoom() == operations[j].get_operationRoom()): 
                        self._numOfConflicts += 1
                    # Conflict #3 - in the same operation time there is an surgeon who's assigned to 2 operations
                    if (operations[i].get_surgeon().get_name() == operations[j].get_surgeon().get_name()): 
                        self._numOfConflicts += 1
        if (self._numOfConflicts == 0):
            print(self)
            print(self)
        return 1 / ((1.0*self._numOfConflicts + 1))
    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._operations)-1):
            returnValue += str(self._operations[i]) + ", "
        returnValue += str(self._operations[len(self._operations)-1])
        return returnValue
class Population:
    # Initialization of the first population, meaning random schedules
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []
        for _ in range(0, size): self._schedules.append(Schedule().initialize())
    def get_schedules(self): return self._schedules
class GeneticAlgorithm:
    def evolve(self, population): return self._mutate_population(self._crossover_population(population))
    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUM_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUM_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop
    def _mutate_population(self, population):
        for i in range(NUM_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population
    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_operations())):
            if (rnd.random() > 0.5): crossoverSchedule.get_operations()[i] = schedule1.get_operations()[i]
            else: crossoverSchedule.get_operations()[i] = schedule2.get_operations()[i]
        return crossoverSchedule
    def _mutate_schedule(self, mutate_schedule):
        schedule = Schedule().initialize()
        for i in range(0, len(mutate_schedule.get_operations())):
            if (MUTATION_PROBABILITY > rnd.random()): mutate_schedule.get_operations()[i] = schedule.get_operations()[i]
        return mutate_schedule
    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop
class Surgery:
    def __init__(self, number, name, surgeons, surgeryType):
        self._number = number
        self._name = name
        self._surgeons = surgeons
        self._surgeryType = surgeryType
    def get_number(self): return self._number
    def get_name(self): return self._name
    def get_surgeons(self): return self._surgeons
    def get_surgeryType(self): return self._surgeryType
    def __str__(self): return self._name
class Surgeon:
    def __init__(self, id_1, name):
        self._id = id_1
        self._name = name
    def get_id(self): return self._id
    def get_name(self): return self._name
    def __str__(self): return self._name
class OperationRoom:
    def __init__(self, number, surgeryType):
        self._number = number
        self._surgeryType = surgeryType
    def get_number(self): return self._number
    def get_surgeryType(self): return self._surgeryType
class OperationTime:
    def __init__(self, id_1, time):
        self._id = id_1
        self._time = time
    def get_id(self): return self._id
    def get_time(self): return self._time
class Ward:
    def __init__(self, name, surgeries):
        self._name = name
        self._surgeries = surgeries
    def get_name(self): return self._name
    def get_surgeries(self): return self._surgeries
class Operation:
    def __init__(self, id_1, ward, surgery):
        self._id = id_1
        self._ward = ward
        self._surgery = surgery
        self._surgeon = None
        self._operationTime = None
        self._operationRoom = None
    def get_id(self): return self._id
    def get_ward(self): return self._ward
    def get_surgery(self): return self._surgery
    def get_surgeon(self): return self._surgeon
    def get_operationTime(self): return self._operationTime
    def get_operationRoom(self): return self._operationRoom
    def set_surgeon(self, surgeon): self._surgeon = surgeon
    def set_operationTime(self, operationTime): self._operationTime = operationTime
    def set_operationRoom(self, operationRoom): self._operationRoom = operationRoom
    def __str__(self):
        return str(self._ward.get_name()) + "," + str(self._surgery.get_number()) + "," + \
               str(self._operationRoom.get_number()) + "," + str(self._surgeon.get_id()) + "," + str(self._operationTime.get_id()) 
class DisplayMgr:
    def printAvailableData(self):
        print("> All Available Data")
        self.print_ward()
        self.print_surgery()
        self.print_operationRoom()
        self.print_instructor()
        self.print_operationTimes()
    def print_ward(self):
        wards = data.get_wards()
        availableWardsTable = prettytable.PrettyTable(['ward', 'surgeries'])
        for i in range(0, len(wards)):
            surgeries = wards.__getitem__(i).get_surgeries()
            tempStr = "["
            for j in range(0, len(surgeries) - 1):
                tempStr += surgeries[j].__str__() + ", "
            tempStr += surgeries[len(surgeries) - 1].__str__() + "]"
            availableWardsTable.add_row([wards.__getitem__(i).get_name(), tempStr])
        print(availableWardsTable)
    def print_surgery(self):
        availableWardsTable = prettytable.PrettyTable(['id', 'surgery #', 'Type of surgery', 'surgeons'])
        surgeries = data.get_surgeries()
        for i in range(0, len(surgeries)):
            surgeons = surgeries[i].get_surgeons()
            tempStr = ""
            for j in range(0, len(surgeons) - 1):
                tempStr += surgeons[j].__str__() + ", "
            tempStr += surgeons[len(surgeons) - 1].__str__()
            availableWardsTable.add_row(
                [surgeries[i].get_number(), surgeries[i].get_name(), str(surgeries[i].get_surgeryType()), tempStr])
        print(availableWardsTable)
    def print_instructor(self):
        availableWardsTable = prettytable.PrettyTable(['id', 'surgeon'])
        surgeons = data.get_surgeons()
        for i in range(0, len(surgeons)):
            availableWardsTable.add_row([surgeons[i].get_id(), surgeons[i].get_name()])
        print(availableWardsTable)
    def print_operationRoom(self):
        availableWardsTable = prettytable.PrettyTable(['room #', 'surgery type allowed'])
        operatingRooms = data.get_operatingRooms()
        for i in range(0, len(operatingRooms)):
            availableWardsTable.add_row([str(operatingRooms[i].get_number()), str(operatingRooms[i].get_surgeryType())])
        print(availableWardsTable)
    def print_operationTimes(self):
        availableWardsTable = prettytable.PrettyTable(['id', 'Operation Time'])
        operationTimes = data.get_operationTimes()
        for i in range(0, len(operationTimes)):
            availableWardsTable.add_row([operationTimes[i].get_id(), operationTimes[i].get_time()])
        print(availableWardsTable)
    def print_generation(self, population):
        table1 = prettytable.PrettyTable(['schedule #', 'fitness', '# of conflicts', 'Operations [ward,surgery,room,surgeon]'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([str(i), round(schedules[i].get_fitness(), 3), schedules[i].get_numOfConflicts(), schedules[i]])
        print(table1)
    def printScheduleAsTable(self, schedule):
        operations = schedule.get_operations()
        table = prettytable.PrettyTable(['Operation #', 'Ward', 'Surgery (number, surgery type)', 'Operation Room (Surgery Type)', 'Surgeon (name, id)', 'Operation Time (time, id)'])
        for i in range(0, len(operations)):
            table.add_row([str(i), operations[i].get_ward().get_name(), operations[i].get_surgery().get_name() + "(" +
                          operations[i].get_surgery().get_number() + ", " +
                          str(operations[i].get_surgery().get_surgeryType()) + ")",
                          operations[i].get_operationRoom().get_number() + " (" + str(operations[i].get_operationRoom().get_surgeryType()) + ")",
                          operations[i].get_surgeon().get_name() + " (" + str(operations[i].get_surgeon().get_id()) + ")",
                          operations[i].get_operationTime().get_time() + " (" + str(operations[i].get_operationTime().get_id()) + ")"])
        print(table)
# Creating the data
data = Data()
# Creating an instance of the display manager
displayMgr = DisplayMgr()
displayMgr.printAvailableData()
generation_number = 0
print("\n> Generation # " + str(generation_number))
# Creating the population - random solutions
population = Population(POPULATION_SIZE)
# Sorting them by the fitness value
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
displayMgr.print_generation(population)
displayMgr.printScheduleAsTable(population.get_schedules()[0])
# Creating an instance of the genetic algorithm class
geneticAlgorithm = GeneticAlgorithm()
# While we haven't gotten to 0 conflicts
while (population.get_schedules()[0].get_fitness() != 1.0):
    generation_number += 1
    print("\n> Generation # " + str(generation_number))
    # Mutate & Crossover
    population = geneticAlgorithm.evolve(population)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    displayMgr.print_generation(population)
    displayMgr.printScheduleAsTable(population.get_schedules()[0])
print("\n\n")