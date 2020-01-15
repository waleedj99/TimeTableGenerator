import math
import random
import copy


class Room:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return str(self.name)


class Teacher:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return str(self.name)


class Subject:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return str(self.name)

    @staticmethod
    def random_subject(classes_per_sub, subject_list, class_times_list, day_list):
        prob_not_empty = (classes_per_sub*len(subject_list)) / \
            ((len(class_times_list)*len(day_list)))
        if random.uniform(0, 1) < prob_not_empty:
            return Subject(random.choice(subject_list))
        else:
            return Subject("empty")


class Class:
    def __init__(self, std_grp=None, subject=None, teacher=None, room=None):
        self.std_grp = std_grp
        self.subject = subject
        self.teacher = teacher
        self.room = room

    def __str__(self):
        return str(self.subject)+" "+str(self.std_grp)+" "+str(self.teacher)+" "+str(self.room)

    def __repr__(self):
        return str(self.subject)+" "+str(self.std_grp)+" "+str(self.teacher)+" "+str(self.room)


class TimeTable:
    def __init__(self, day_list, class_times_list, std_grp_list, room_list, subject_list, teacher_list):
        self.n_days = len(day_list)
        self.n_class_per_day = len(class_times_list)
        self.n_std_grps = len(std_grp_list)

        self.per_subject_count = 3
        self.day_list = day_list
        self.class_timings_list = class_times_list
        self.std_grp_list = std_grp_list
        self.room_list = room_list
        self.subject_list = subject_list
        self.teacher_list = teacher_list
        self.timetable = [[[Class(std_grp=std_grp_list[stg], subject=Subject.random_subject(self.per_subject_count, self.subject_list, self.class_timings_list, self.day_list), teacher=self.random_teacher(teacher_list), room=self.random_room(room_list)) for stg in range(self.n_std_grps)]
                           for j in range(self.n_class_per_day)] for i in range(self.n_days)]

    @staticmethod
    def random_room(room_list):
        return Room(random.choice(room_list))

    @staticmethod
    def random_teacher(teacher_list):
        return Teacher(random.choice(teacher_list))

    def get_conflicts(self):
        room_conflicts = 0
        teacher_conflicts = 0
        for i in range(self.n_days):
            for j in range(self.n_class_per_day):
                room_set = set()
                teacher_set = set()
                for k in range(self.n_std_grps):
                    if self.timetable[i][j][k].subject.name != 'empty' and self.timetable[i][j][k].room in room_set:
                        room_conflicts += 1
                    else:
                        room_set.add(self.timetable[i][j][k].room)
                    if self.timetable[i][j][k].subject.name != 'empty' and self.timetable[i][j][k].teacher in teacher_set:
                        teacher_conflicts += 1
                    else:
                        room_set.add(self.timetable[i][j][k].teacher)
        subjects_conflicts = 0

        for k in range(self.n_std_grps):
            sc = 0
            subject_count = {}
            for i in range(self.n_days):
                for j in range(self.n_class_per_day):
                    if not subject_count.get(self.timetable[i][j][k].subject.name):
                        subject_count[self.timetable[i][j][k].subject.name] = 1
                    else:
                        subject_count[self.timetable[i]
                                      [j][k].subject.name] += 1
            for subject_name, subject_freq in subject_count.items():

                if subject_name != 'empty':
                    # print('Subject={}, freq={}'.format(subject_name, subject_freq))
                    sc = sc + abs(subject_freq-self.per_subject_count)
            subjects_conflicts += sc
        print('Subject conflicts={}, room conflicts={}, teacher conflicts={}'.format(
            subjects_conflicts, room_conflicts, teacher_conflicts))

    def get_fitness(self):
        """
        Fitness is the inverse of the number of conflicts.
        There are two types of conflicts:
        1. Two student groups occupying the same room at the same time.
        2. One teacher teaching two sets of student groups at the same time.
        """
        conflicts = 0
        room_conflicts = 0
        teacher_conflicts = 0
        for i in range(self.n_days):
            for j in range(self.n_class_per_day):
                room_set = set()
                teacher_set = set()
                for k in range(self.n_std_grps):
                    if self.timetable[i][j][k].subject.name != 'empty' and self.timetable[i][j][k].room in room_set:
                        room_conflicts += 1
                    else:
                        room_set.add(self.timetable[i][j][k].room)
                    if self.timetable[i][j][k].subject.name != 'empty' and self.timetable[i][j][k].teacher in teacher_set:
                        teacher_conflicts += 1
                    else:
                        room_set.add(self.timetable[i][j][k].teacher)
        subjects_conflicts = 0

        for k in range(self.n_std_grps):
            sc = 0
            subject_count = {}
            for i in range(self.n_days):
                for j in range(self.n_class_per_day):
                    if not subject_count.get(self.timetable[i][j][k].subject.name):
                        subject_count[self.timetable[i][j][k].subject.name] = 1
                    else:
                        subject_count[self.timetable[i]
                                      [j][k].subject.name] += 1
            for subject_name, subject_freq in subject_count.items():

                if subject_name != 'empty':
                    # print('Subject={}, freq={}'.format(subject_name, subject_freq))
                    sc = sc + abs(subject_freq-self.per_subject_count)
            subjects_conflicts += sc
        conflicts = subjects_conflicts+room_conflicts+teacher_conflicts
        # print('Subject conf={}, room con={}, teacher conf={}'.format(subjects_conflicts, room_conflicts, teacher_conflicts))
        if conflicts == 0:
            return math.inf
        else:
            return 1/conflicts

    def mutate(self):
        MUTATION_RATE = 0.05
        for i in range(self.n_days):
            for j in range(self.n_class_per_day):
                for k in range(self.n_std_grps):

                    if(random.uniform(0, 1) < MUTATION_RATE):
                        self.timetable[i][j][k].room = Room(
                            random.choice(self.room_list))

                    if(random.uniform(0, 1) < MUTATION_RATE):
                        self.timetable[i][j][k].teacher = Teacher(
                            random.choice(self.teacher_list))

                    if(random.uniform(0, 1) < MUTATION_RATE):
                        self.timetable[i][j][k].subject = Subject.random_subject(
                            self.per_subject_count, self.subject_list, self.class_timings_list, self.day_list)


# TODO: Start from here tmrw
class GeneticAlgorithm:

    def __init__(self, n_days, n_class_per_day):
        self.population = None
        self.n_days = n_days
        self.n_class_per_day = n_class_per_day
        self.population_size = 20
        self.n_generations = 100
        self.crossover_prob = 0.75

    def generate_init_population(self, day_list, class_list, std_grp_list, subject_list, room_list, teacher_list):
        self.population = [TimeTable(day_list, class_list, std_grp_list, room_list,
                                     subject_list, teacher_list) for i in range(self.population_size)]

    def get_fittest(self):
        max_fitness = -math.inf
        fittest = None
        for timetable in self.population:
            fitness = timetable.get_fitness()
            if fitness > max_fitness:
                max_fitness = fitness
                fittest = timetable
        return fittest

    def get_least_fittest_index(self):
        min_fitness = math.inf
        least_fit_index = None
        for i in range(len(self.population)):
            timetable = self.population[i]
            fitness = timetable.get_fitness()
            if fitness < min_fitness:
                min_fitness = fitness
                least_fit_index = i
        return least_fit_index

    def get_second_fittest(self):
        max_fitness = -math.inf
        second_fittest = None
        fittest = self.get_fittest()

        for timetable in self.population:
            fitness = timetable.get_fitness()
            if fitness > max_fitness and fittest != second_fittest:
                max_fitness = fitness
                second_fittest = timetable
        return second_fittest

    def avg_fitness(self):
        avg = 0
        for t in self.population:
            avg += t.get_fitness()
        return avg/self.population_size

    def run_algorithm(self, day_list, class_list, std_grp_list, subject_list, room_list, teacher_list):
        self.generate_init_population(
            day_list, class_list, std_grp_list, subject_list, room_list, teacher_list)
        for g in range(self.n_generations):
            # Selection
            new_population = []
            new_population.append(self.get_fittest())
            while len(new_population)<self.population_size:
                parent1 = self.get_fittest()
                parent2 = self.get_second_fittest()
                # Crossover
                if(random.uniform(0, 1) < self.crossover_prob):
                    offspring = self.crossover(parent1, parent2)
                else:
                    offspring = copy.deepcopy(parent1)
                # Mutation
                offspring.mutate()
                new_population.append(offspring)

            self.population = new_population
            f = self.get_fittest().get_fitness()
            
            print('Generation {}. Max fitness={}, avg fitness={}'.format(g,
                                                                         f, self.avg_fitness()))
            if f == math.inf:
                print('Reached max fitness at generation {}, stopping..'.format(g))
                return self.get_fittest()

        return self.get_fittest()

    def crossover(self, timetable1: TimeTable, timetable2: TimeTable):
        # Randomly copy over some genes from either chromosome and return a new one
        timetable_crossed = TimeTable(
            timetable1.day_list, timetable1.class_timings_list, timetable1.std_grp_list, timetable1.room_list, timetable1.subject_list, timetable1.subject_list)
        for i in range(timetable1.n_days):
            for j in range(timetable1.n_class_per_day):
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
        return timetable_crossed


ga = GeneticAlgorithm(5, 8)
fittest = ga.run_algorithm(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri'], ['9-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17'], ['A', 'B', 'C'], ['math',
                                                                                                                                                              'science', 'social', 'history', 'english', 'hindi', 'computers'], ['400', '401', '402', '404', '405'], ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10'])
print(fittest.timetable)
