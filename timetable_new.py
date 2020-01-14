import math
import random


class Room:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)


class Teacher:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)


class StudentGroup:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)


class Subject:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)


class Class:
    def __init__(self, no_class=True, std_grp=None, time_interval=None, subject=None, teacher=None, room=None):
        self.is_empty = no_class
        self.no_class = no_class
        self.std_grp = std_grp
        self.time_interval = time_interval
        self.subject = subject
        self.teacher = teacher
        self.room = room


class TimeTable:
    def __init__(self, day_list, class_times_list, std_grp_list, room_list, subject_list, teacher_list):
        self.n_days = len(day_list)
        self.n_class_per_day = len(class_list)
        self.n_std_grps = len(std_grp_list)

        self.day_list = day_list
        self.class_timings_list = class_list
        self.std_grp_list = std_grp_list
        self.room_list = room_list
        self.subject_list = subject_list
        self.teacher_list = teacher_list
        self.timetable = [[[Class() for i in range(self.n_class_per_day)]
                           for j in range(self.n_days)] for k in range(self.n_std_grps)]

    def get_fitness(self):
        """
        Fitness is the inverse of the number of conflicts.
        There are two types of conflicts:
        1. Two student groups occupying the same room at the same time.
        2. One teacher teaching two sets of student groups at the same time.
        """
        conflicts = 0
        for i in range(self.n_class_per_day):
            for j in range(self.n_days):
                room_set = set()
                teacher_set = set()
                for k in range(self.n_std_grps):
                    if self.timetable[i][j][k].room in room_set:
                        conflicts += 1
                    else:
                        room_set.add(self.timetable[i][j][k].room)
                    if self.timetable[i][j][k].teacher in teacher_set:
                        conflicts += 1
                    else:
                        room_set.add(self.timetable[i][j][k].teacher)

        if conflicts == 0:
            return math.inf
        else:
            return 1/conflicts

    def mutate(self):
        MUTATION_RATE = 0.01
        for i in range(self.n_class_per_day):
            for j in range(self.n_days):
                for k in range(self.n_std_grps):

                    if(random.uniform(0, 1) < MUTATION_RATE):
                        self.timetable[i][j][k].room = Room(
                            random.choice(self.room_list))

                    if(random.uniform(0, 1) < MUTATION_RATE):
                        self.timetable[i][j][k].teacher = Teacher(
                            random.choice(self.teacher_list))

                    if(random.uniform(0, 1) < MUTATION_RATE):
                        self.timetable[i][j][k].subject = Subject(
                            random.choice(self.subject_list))


    
# TODO: Start from here tmrw
class GeneticAlgorithm:

    def __init__(self):
        self.population = None

    def generate_init_population(self, population_size, class_list, std_grp_list, subject_list, room_list):
        pass

    def get_fittest(self):
        pass

    def run_algorithm(self, class_list, std_grp_list, subject_list, room_list):
        POPULATION_SIZE = 2000
        self.generate_init_population(POPULATION_SIZE, class_list, std_grp_list, subject_list, room_list)

    def crossover(self, timetable1: TimeTable, timetable2: TimeTable):
        # Randomly copy over some genes from either chromosome and return a new one
        timetable_crossed = TimeTable(
            timetable1.day_list, timetable1.class_times_list, timetable1.std_grp_list, timetable1.room_list, timetable1.subject_list, timetable1.subject_list)
        for i in range(timetable1.n_class_per_day):
            for j in range(timetable1.n_days):
                for k in range(timetable1.n_std_grps):
                    if bool(random.getrandbits(1)):
                        timetable_crossed.timetable[i][j][k].room = timetable1.timetable[i][j][k].room
                    else:
                        timetable_crossed.timetable[i][j][k].room = timetable2.timetable[i][j][k].room
                    
                    if bool(random.getrandbits(1)):
                        timetable_crossed.timetable[i][j][k].subject = timetable1.timetable[i][j][k].subject
                    else:
                        timetable_crossed.timetable[i][j][k].subject = timetable2.timetable[i][j][k].subject

                    if bool(random.getrandbits(1)):
                        timetable_crossed.timetable[i][j][k].teacher = timetable1.timetable[i][j][k].teacher
                    else:
                        timetable_crossed.timetable[i][j][k].teacher = timetable2.timetable[i][j][k].teacher

