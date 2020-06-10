import math
import random
import copy
import functools


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

    def get_soft_conflicts(self):
        # Constraint to reduce the number of gaps between classes.
        # 0.1 Weight for soft constraints so its not getting superiority over hard constraints
        gaps = 0

        # Stores the max-min classes on each day of the week, for all student groups.
        # If this value is minimum, the number of classes on each day are roughly uniform
        diff_classes_sum = 0
        for k in range(len(self.student_groups)):
            max_cls = -math.inf
            min_cls = math.inf
            for i in range(self.n_days):
                start = -1
                n_cls = 0
                for j in range(self.n_class_per_day):
                    if self.timetable[i][j][k].subject.name != 'empty':
                        if start == -1:
                            start = i
                        else:
                            gaps += abs(j - start - 1)
                            start = j

                        n_cls += 1
                max_cls = max(max_cls, n_cls)
                min_cls = min(min_cls, n_cls)
            diff_classes_sum += (max_cls - min_cls)
        return gaps + diff_classes_sum

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
            subject_count = {s: 0 for s in self.subject_list}
            subject_count['empty'] = 0
            for i in range(self.n_days):
                for j in range(self.n_class_per_day):
                    subject_count[self.timetable[i][j][k].subject.name] += 1
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
                    if self.student_groups[k][cur_sub] != cur_teacher:
                        teacher_student_group_conflicts += 1

            # print(
            #     'Subject conflicts={}, room conflicts={}, teacher conflicts={}, Teacher-student group conflicts={},'
            #     ' gaps={}, diff={}'.format(
            #         subjects_conflicts, room_conflicts, teacher_conflicts, teacher_student_group_conflicts, gaps,
            #         diff_classes_sum))
        return subjects_conflicts + room_conflicts + teacher_conflicts + teacher_student_group_conflicts

    def get_fitness(self):
        """
        Fitness is the inverse of the number of conflicts.
        There are two types of conflicts:
        1. Two student groups occupying the same room at the same time.
        2. One teacher teaching two sets of student groups at the same time.
        """
        hard_conflicts = self.get_conflicts()
        soft_conflicts = self.get_soft_conflicts()
        hard_fitness = 1 / hard_conflicts if hard_conflicts != 0 else math.inf
        soft_fitness = 1 / soft_conflicts if soft_conflicts != 0 else math.inf
        return [hard_fitness, soft_fitness]

    def mutate(self):
        mutation_rate = 0.05
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
        self.population_size = 100
        self.n_generations = 100
        self.crossover_prob = 0.75

    def generate_init_population(self, day_list, class_list, subject_list, room_list, teacher_list, student_groups):
        self.population = [TimeTable(day_list, class_list, room_list,
                                     subject_list, teacher_list, student_groups) for i in range(self.population_size)]

    def get_least_fittest_index(self, lf):
        for i, gene in enumerate(self.population):
            if gene == lf:
                return i
        return None

    @staticmethod
    def __fitness_comp(a, b):
        a_hf, a_sf = a.get_fitness()
        b_hf, b_sf = b.get_fitness()

        if a_hf < b_hf:
            return -1
        elif b_hf < a_hf:
            return 1
        else:
            if a_sf < b_sf:
                return -1
            elif b_sf < a_sf:
                return 1
            else:
                return 0

    def avg_fitness(self):
        avg = [0, 0]
        for t in self.population:
            f = t.get_fitness()
            avg[0] += f[0]
            avg[1] += f[1]
        return avg[0] / self.population_size, avg[1] / self.population_size

    def run_algorithm(self, day_list, class_list, subject_list, room_list, teacher_list, student_group_map_list):
        student_groups = []
        fittest = None
        for stg_map in student_group_map_list:
            item = {Subject(s): Teacher(t) for s, t in stg_map.items()}
            student_groups.append(item)

        self.generate_init_population(
            day_list, class_list, subject_list, room_list, teacher_list, student_groups)
        for g in range(self.n_generations):
            # Selection
            sorted_population = sorted(self.population, key=functools.cmp_to_key(self.__fitness_comp))
            fittest = sorted_population[-1]
            new_population = [fittest]
            f = fittest.get_fitness()
            print('Generation {}. Max fitness={}, avg fitness={}'.format(g, f, self.avg_fitness()))
            if f[0] == math.inf and f[1] == math.inf:
                print('Reached max fitness at generation {}, stopping..'.format(g))
                return sorted_population[-1]

            while len(new_population) < self.population_size:
                parent1 = sorted_population[-1]
                parent2 = sorted_population[-2]
                # Crossover
                if random.uniform(0, 1) < self.crossover_prob:
                    offspring = crossover(parent1, parent2)
                else:
                    offspring = copy.deepcopy(parent1)
                # Mutation
                offspring.mutate()
                new_population.append(offspring)

            self.population = new_population

        return fittest

#
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
