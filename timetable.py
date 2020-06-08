import math
import random
import copy


class Room:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return str(self.name)


class Teacher:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return str(self.name)


class Subject:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return str(self.name)

    @staticmethod
    def random_subject(classes_per_sub, subject_list, class_times_list, day_list):
        prob_not_empty = (classes_per_sub * len(subject_list)) / \
                         (len(class_times_list) * len(day_list))
        if random.uniform(0, 1) < prob_not_empty:
            return Subject(random.choice(subject_list))
        else:
            return Subject("empty")


class StudentGroup:

    def __init__(self, name, subject_teacher_map):
        self.subject_teacher_map = subject_teacher_map
        self.group_name = name

    def __hash__(self):
        return hash(self.group_name)

    def __getitem__(self, item):
        return self.subject_teacher_map[item]

    def __eq__(self, other):
        return self.group_name == other.group_name

    def __repr__(self):
        return str(self.group_name)


class Class:
    def __init__(self, subject=None, room=None, student_group=None):
        self.subject = subject
        self.teacher = student_group[subject]
        self.room = room
        self.student_group = student_group

    def __str__(self):
        return str(self.subject) + " " + str(self.student_group) + " " + str(self.teacher) + " " + str(self.room)

    def __repr__(self):
        return str(self.subject) + " " + str(self.student_group) + " " + str(self.teacher) + " " + str(self.room)


class TimeTable:
    def __init__(self, day_list, class_times_list, room_list, subject_list, teacher_list, student_groups):
        self.n_days = len(day_list)
        self.n_class_per_day = len(class_times_list)

        self.per_subject_count = 3
        self.day_list = day_list
        self.class_timings_list = class_times_list
        self.room_list = room_list
        self.subject_list = subject_list
        self.teacher_list = teacher_list
        self.student_groups = [StudentGroup(str(i), stg) for i, stg in enumerate(student_groups)]
        self.timetable = [[[Class(student_group=stg,
                                  subject=Subject.random_subject(self.per_subject_count, self.subject_list,
                                                                 self.class_timings_list, self.day_list),
                                  room=self.random_room(room_list)) for stg
                            in self.student_groups]
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
                for k in range(len(self.student_groups)):
                    if self.timetable[i][j][k].subject.name != 'empty' and self.timetable[i][j][k].room in room_set:
                        room_conflicts += 1
                    else:
                        room_set.add(self.timetable[i][j][k].room)
                    if self.timetable[i][j][k].subject.name != 'empty' and self.timetable[i][j][
                        k].teacher in teacher_set:
                        teacher_conflicts += 1
                    else:
                        teacher_set.add(self.timetable[i][j][k].teacher)
        subjects_conflicts = 0

        for k in range(len(self.student_groups)):
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
                    sc = sc + abs(subject_freq - self.per_subject_count)
            subjects_conflicts += sc
        teacher_student_group_conflicts = 0
        for k in range(len(self.student_groups)):
            for i in range(self.n_days):
                for j in range(self.n_class_per_day):
                    cur_sub = self.timetable[i][j][k].subject
                    cur_teacher = self.timetable[i][j][k].teacher
                    if cur_sub.name != 'empty' and self.student_groups[k][cur_sub] != cur_teacher:
                        teacher_student_group_conflicts += 1

        # print(
        #     'Subject conflicts={}, room conflicts={}, teacher conflicts={}, Teacher-student group conflicts={}'.format(
        #         subjects_conflicts, room_conflicts, teacher_conflicts, teacher_student_group_conflicts))
        return subjects_conflicts + room_conflicts + teacher_conflicts + teacher_student_group_conflicts

    def get_fitness(self):
        """
        Fitness is the inverse of the number of conflicts.
        There are two types of conflicts:
        1. Two student groups occupying the same room at the same time.
        2. One teacher teaching two sets of student groups at the same time.
        """
        conflicts = self.get_conflicts()
        if conflicts == 0:
            return math.inf
        else:
            return 1 / conflicts

    def mutate(self):
        mutation_rate = 0.04
        for i in range(self.n_days):
            for j in range(self.n_class_per_day):
                for k in range(len(self.student_groups)):

                    if random.uniform(0, 1) < mutation_rate:
                        self.timetable[i][j][k].room = Room(
                            random.choice(self.room_list))

                    if random.uniform(0, 1) < mutation_rate:
                        self.timetable[i][j][k].subject = Subject.random_subject(
                            self.per_subject_count, self.subject_list, self.class_timings_list, self.day_list)
                        self.timetable[i][j][k].teacher = self.timetable[i][j][k].student_group[
                            self.timetable[i][j][k].subject]


def crossover(timetable1: TimeTable, timetable2: TimeTable):
    # Randomly copy over some genes from either chromosome and return a new one
    timetable_crossed = TimeTable(
        timetable1.day_list, timetable1.class_timings_list, timetable1.room_list,
        timetable1.subject_list, timetable1.teacher_list, timetable1.student_groups)
    for i in range(timetable1.n_days):
        for j in range(timetable1.n_class_per_day):
            for k in range(len(timetable1.student_groups)):
                if bool(random.getrandbits(1)):
                    timetable_crossed.timetable[i][j][k].room = timetable1.timetable[i][j][k].room
                else:
                    timetable_crossed.timetable[i][j][k].room = timetable2.timetable[i][j][k].room

                if bool(random.getrandbits(1)):
                    timetable_crossed.timetable[i][j][k].subject = timetable1.timetable[i][j][k].subject
                    timetable_crossed.timetable[i][j][k].teacher = timetable1.timetable[i][j][k].student_group[
                        timetable1.timetable[i][j][k].subject]
                else:
                    timetable_crossed.timetable[i][j][k].subject = timetable2.timetable[i][j][k].subject
                    timetable_crossed.timetable[i][j][k].teacher = timetable2.timetable[i][j][k].student_group[
                        timetable2.timetable[i][j][k].subject]

                # if bool(random.getrandbits(1)):
                #     timetable_crossed.timetable[i][j][k].teacher = timetable1.timetable[i][j][k].teacher
                # else:
                #     timetable_crossed.timetable[i][j][k].teacher = timetable2.timetable[i][j][k].teacher
    return timetable_crossed


class GeneticAlgorithm:

    def __init__(self, n_days, n_class_per_day):
        self.population = None
        self.n_days = n_days
        self.n_class_per_day = n_class_per_day
        self.population_size = 20
        self.n_generations = 100
        self.crossover_prob = 0.75

    def generate_init_population(self, day_list, class_list, subject_list, room_list, teacher_list, student_groups):
        self.population = [TimeTable(day_list, class_list, room_list,
                                     subject_list, teacher_list, student_groups) for i in range(self.population_size)]

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
        return avg / self.population_size

    def run_algorithm(self, day_list, class_list, subject_list, room_list, teacher_list, student_group_map_list):
        student_groups = []
        for stg_map in student_group_map_list:
            item = {Subject(s): Teacher(t) for s, t in stg_map.items()}
            student_groups.append(item)

        self.generate_init_population(
            day_list, class_list, subject_list, room_list, teacher_list, student_groups)
        for g in range(self.n_generations):
            # Selection
            new_population = [self.get_fittest()]
            while len(new_population) < self.population_size:
                parent1 = self.get_fittest()
                parent2 = self.get_second_fittest()
                # Crossover
                if random.uniform(0, 1) < self.crossover_prob:
                    offspring = crossover(parent1, parent2)
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


# ga = GeneticAlgorithm(5, 8)
# fittest = ga.run_algorithm(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri'],
#                            ['9-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17'],
#                            ['math', 'science', 'social', 'history', 'english', 'hindi', 'computers'],
#                            ['400', '401'], # List of rooms
#                            ['T1', 'T2', 'T3', 'T4', 'T5', 'T6'], # List of teachers
#                            [{'math': 'T1', 'science': 'T2', 'social': 'T3', 'history': 'T4', 'english': 'T5',
#                              'hindi': 'T6', 'computers': 'T3', 'empty': '-'},
#                             {'math': 'T1', 'science': 'T2', 'social': 'T3', 'history': 'T4', 'english': 'T5', # List
#                              'hindi': 'T6', 'computers': 'T3', 'empty': '-'}])
# print(fittest.timetable)
