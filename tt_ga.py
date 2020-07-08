import prettytable as prettytable
import random as rnd

# Number of chromosomes in each generation - meaning the number of solutions
POPULATION_SIZE = 9 

# Number of the best schedules (fittest) in each generation
NUM_OF_ELITE_SCHEDULES = 1

# Number of solutions we consider in the tournament selection
TOURNAMENT_SELECTION_SIZE = 3

# The mutation rate
MUTATION_PROBABILITY = 0.1

### Time-Tabling DATA ###
# Rooms for classes - id, seating capacity
ROOMS = [["R1",25], ["R2",45], ["R3",35]]

# Meeting times - id, day & time
MEETING_TIMES = [["MT1", "MWF 09:00 - 10:00"],
                   ["MT2", "MWF 10:00 - 11:00"],
                   ["MT3", "TTH 09:00 - 10:30"],
                   ["MT4", "TTH 10:30 - 12:00"]]

# Instructors - id, full name
INSTRUCTORS = [["I1", "Dr. James Web"],
                  ["I2", "Mr. Mike Brown"],
                  ["I3", "Dr Steve Day"],
                  ["I4", "Mrs Jane Doe"]]


class Data:
    # Initialization of the data
    def __init__(self):
        self._rooms = []; self._meeting_times = []; self._instructors = []
        # Adding ROOMS to the data
        for i in range (0, len(ROOMS)):
            self._rooms.append(Room(ROOMS[i][0], ROOMS[i][1]))
        # Adding MEETING_TIMES to the data
        for i in range (0, len(MEETING_TIMES)):
            self._meeting_times.append(MeetingTime(MEETING_TIMES[i][0], MEETING_TIMES[i][1]))
        # Adding INSTRUCTORS to the data
        for i in range (0, len(INSTRUCTORS)):
            self._instructors.append(Instructor(INSTRUCTORS[i][0], INSTRUCTORS[i][1]))
        # Creating courses and assigning instructors to them    
        course1 = Course("C1", "325K", [self._instructors[0], self._instructors[1]], 25)
        course2 = Course("C2", "319K", [self._instructors[0], self._instructors[1], self._instructors[2]], 35)
        course3 = Course("C3", "462K", [self._instructors[0], self._instructors[1]], 25)
        course4 = Course("C4", "464K", [self._instructors[2], self._instructors[3]], 30)
        course5 = Course("C5", "360C", [self._instructors[3]], 35)
        course6 = Course("C6", "303K", [self._instructors[0], self._instructors[2]], 45)
        course7 = Course("C7", "303L", [self._instructors[1], self._instructors[3]], 45)
        # Adding courses to the data
        self._courses = [course1, course2, course3, course4, course5, course6, course7]
        # Creating departments and assigning courses to them
        dept1 = Department("MATH", [course1, course3])
        dept2 = Department("EE", [course2, course4, course5])
        dept3 = Department("PHY", [course6, course7])
        # Adding departments to the data
        self._depts = [dept1, dept2, dept3]
        self._num_of_classes = 0
        for i in range(0, len(self._depts)):
            self._num_of_classes += len(self._depts[i].get_courses())
    def get_rooms(self): return self._rooms
    def get_instructors(self): return self._instructors
    def get_courses(self): return self._courses
    def get_depts(self): return self._depts
    def get_meeting_times(self): return self._meeting_times
    def get_num_of_classes(self): return self._num_of_classes
class Schedule:
    def __init__(self):
        self._data = Data()
        self._classes = []
        self._num_of_conflicts = 0
        self._fitness = -1
        self._class_num = 0
        self._is_fitness_changed = True
    def get_num_of_conflicts(self):
        return self._num_of_conflicts
    def get_classes(self): 
        self._is_fitness_changed = True
        return self._classes
    def get_fitness(self): 
        if (self._is_fitness_changed == True):
            self._fitness = self.calculate_fitness()
            self._is_fitness_changed = False
        return self._fitness
    # Initialization of the schedule
    def initialize(self):
        # Getting the departments from the data
        depts = self._data.get_depts()
        # Iterating over the departments
        for i in range(0, len(depts)):
            # For each department, take the courses list
            courses = depts[i].get_courses()
            # Iterating over the courses of each department
            for j in range(0, len(courses)):
                # Creating an instance of Class for each course
                new_class = Class(self._class_num, depts[i], courses[j])
                self._class_num += 1
                # Setting a meeting time randomly from a given set of meeting times (in the data)
                new_class.set_meeting_time(data.get_meeting_times()[rnd.randrange(0, len(data.get_meeting_times()))])
                # Setting a room randomly from a given set of rooms (in the data)
                new_class.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                # Setting an instructor randomly from a given set of instructors of the specifuc ciyrse (in the data)
                new_class.set_instructor(courses[j].get_instructors()[rnd.randrange(0, len(courses[j].get_instructors()))])
                self._classes.append(new_class)
        return self
    def calculate_fitness(self):
        self._num_of_conflicts = 0
        classes = self.get_classes()
        for i in range(0, len(classes)):
            # Conflict #1 - the room's seating capacity is lower than the max num of students in the course
            if (classes[i].get_room().get_seating_capacity() < classes[i].get_course().get_max_num_of_students()):
                self._num_of_conflicts += 1
            for j in range(0, len(classes)):
                if (j >= i):
                    if (classes[i].get_meeting_time() == classes[j].get_meeting_time() and classes[i].get_id() != classes[j].get_id()):
                        # Conflict #2 - in the same meeting time there is a room which is occupied by 2 classes
                        if (classes[i].get_room() == classes[j].get_room()): 
                            self._num_of_conflicts += 1
                        # Conflict #3 - in the same meeting time there is an instructor who's assigned to 2 classes    
                        if (classes[i].get_instructor() == classes[j].get_instructor()): 
                            self._num_of_conflicts += 1
        return 1 / ((1.0*self._num_of_conflicts + 1))
    def __str__(self):
        return_value = ""
        for i in range(0, len(self._classes)-1):
            return_value += str(self._classes[i]) + ", "
        return_value += str(self._classes[len(self._classes)-1])
        return return_value
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
        for i in range(0, len(crossoverSchedule.get_classes())):
            if (rnd.random() > 0.5): crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else: crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule
    def _mutate_schedule(self, mutate_schedule):
        schedule = Schedule().initialize()
        for i in range(0, len(mutate_schedule.get_classes())):
            if (MUTATION_PROBABILITY > rnd.random()): mutate_schedule.get_classes()[i] = schedule.get_classes()[i]
        return mutate_schedule
    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop
class Course: 
    def __init__(self, number, name, instructors, max_num_of_students):
        self._number = number
        self._name = name
        self._instructors = instructors
        self._max_num_of_students = max_num_of_students
    def get_number(self): return self._number
    def get_name(self): return self._name
    def get_instructors(self): return self._instructors
    def get_max_num_of_students(self): return self._max_num_of_students
    def __str__(self): return self._name
class Instructor:
    def __init__(self, id, name):
        self._id = id
        self._name = name
    def get_id(self): return self._id
    def get_name(self): return self._name
    def __str__(self): return self._name
class Room:
    def __init__(self, number, seating_capacity):
        self._number = number
        self._seating_capacity = seating_capacity
    def get_number(self): return self._number
    def get_seating_capacity(self): return self._seating_capacity
class MeetingTime:
    def __init__(self, id, time):
        self._id = id
        self._time = time
    def get_id(self): return self._id
    def get_time(self): return self._time
class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses
    def get_name(self): return self._name
    def get_courses(self): return self._courses
class Class:
    def __init__(self, id, dept, course):
        self._id = id
        self._dept = dept
        self._course = course
        self._instructor = None
        self._meeting_time = None
        self._room = None
    def get_id(self): return self._id
    def get_dept(self): return self._dept
    def get_course(self): return self._course
    def get_instructor(self): return self._instructor
    def get_meeting_time(self): return self._meeting_time
    def get_room(self): return self._room
    def set_instructor(self, instructor): self._instructor = instructor
    def set_meeting_time(self, meeting_time): self._meeting_time = meeting_time
    def set_room(self, room): self._room = room
    def __str__(self):
        return str(self._dept.get_name()) + "," + str(self._course.get_number()) + "," + \
               str(self._room.get_number()) + "," + str(self._instructor.get_id()) + "," + str(self._meeting_time.get_id()) 
class DisplayMgr:
    def print_available_data(self):
        print("> All Available Data")
        self.print_dept()
        self.print_course()
        self.print_room()
        self.print_instructor()
        self.print_meeting_times()
    def print_dept(self):
        depts = data.get_depts()
        available_depts_table = prettytable.PrettyTable(['dept', 'courses'])
        for i in range(0, len(depts)):
            courses = depts.__getitem__(i).get_courses()
            tempStr = "["
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + ", "
            tempStr += courses[len(courses) - 1].__str__() + "]"
            available_depts_table.add_row([depts.__getitem__(i).get_name(), tempStr])
        print(available_depts_table)
    def print_course(self):
        available_courses_table = prettytable.PrettyTable(['id', 'course #', 'max # of students', 'instructors'])
        courses = data.get_courses()
        for i in range(0, len(courses)):
            instructors = courses[i].get_instructors()
            tempStr = ""
            for j in range(0, len(instructors) - 1):
                tempStr += instructors[j].__str__() + ", "
            tempStr += instructors[len(instructors) - 1].__str__()
            available_courses_table.add_row(
                [courses[i].get_number(), courses[i].get_name(), str(courses[i].get_max_num_of_students()), tempStr])
        print(available_courses_table)
    def print_instructor(self):
        available_instructors_table = prettytable.PrettyTable(['id', 'instructor'])
        instructors = data.get_instructors()
        for i in range(0, len(instructors)):
            available_instructors_table.add_row([instructors[i].get_id(), instructors[i].get_name()])
        print(available_instructors_table)
    def print_room(self):
        available_rooms_table = prettytable.PrettyTable(['room #', 'max seating capacity'])
        rooms = data.get_rooms()
        for i in range(0, len(rooms)):
            available_rooms_table.add_row([str(rooms[i].get_number()), str(rooms[i].get_seating_capacity())])
        print(available_rooms_table)
    def print_meeting_times(self):
        available_meeting_times_table = prettytable.PrettyTable(['id', 'Meeting Time'])
        meeting_times = data.get_meeting_times()
        for i in range(0, len(meeting_times)):
            available_meeting_times_table.add_row([meeting_times[i].get_id(), meeting_times[i].get_time()])
        print(available_meeting_times_table)
    def print_generation(self, population):
        table1 = prettytable.PrettyTable(['schedule #', 'fitness', '# of conflicts', 'classes [dept,class,room,instructor]'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([str(i), round(schedules[i].get_fitness(), 3), schedules[i].get_num_of_conflicts(), schedules[i]])
        print(table1)
    def print_schedule_as_table(self, schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(['Class #', 'Dept', 'Course (number, max # of students)', 'Room (Capacity)', 'Instructor (name, id)', 'Meeting Time (time, id)'])
        for i in range(0, len(classes)):
            table.add_row([str(i), classes[i].get_dept().get_name(), classes[i].get_course().get_name() + "(" +
                          classes[i].get_course().get_number() + ", " +
                          str(classes[i].get_course().get_max_num_of_students()) + ")",
                          classes[i].get_room().get_number() + " (" + str(classes[i].get_room().get_seating_capacity()) + ")",
                          classes[i].get_instructor().get_name() + " (" + str(classes[i].get_instructor().get_id()) + ")",
                          classes[i].get_meeting_time().get_time() + " (" + str(classes[i].get_meeting_time().get_id()) + ")"])
        print(table)
# Creating the data
data = Data()
# Creating an instance of the display manager
displayMgr = DisplayMgr()
displayMgr.print_available_data()
generation_number = 0
print("\n> Generation # " + str(generation_number))
# Creating the population - random solutions
population = Population(POPULATION_SIZE)
# Sorting them by the fitness value
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
displayMgr.print_generation(population)
displayMgr.print_schedule_as_table(population.get_schedules()[0])
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
    displayMgr.print_schedule_as_table(population.get_schedules()[0])
print("\n\n")