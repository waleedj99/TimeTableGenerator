import random
import math
from datetime import datetime, timedelta


class StudentGroup:
    count = 0

    def __init__(self, name):
        self.name = name
        self.id = StudentGroup.count
        StudentGroup.count += 1


class Room:
    count = 0

    def __init__(self, name):
        self.name = name
        self.id = Room.count
        Room.count += 1


class Instructor:
    count = 0

    def __init__(self, fullname):
        self.fullname = fullname
        self.id = Instructor.count
        Instructor.count += 1


class Course:

    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code


class Class:
    count = 0

    def __init__(self, id=None, course=None, type=None, instructor=None, student_group=None, allowed_room=None):
        if id is not None:
            self.id = id
        else:
            self.id = Class.count
            Class.count += 1
        self.course = course
        self.type = type
        self.instructor = instructor
        self.student_group = student_group
        self.allowed_room = allowed_room

    def is_room_allowed(self, room_id):
        if self.id == -1:
            return False
        return self.allowed_room.id == room_id

    def __str__(self):
        str_val = "Class id={}| course={}, type={}, instructor={}, student_group={}, allowed_room={}".format(self.id,
                                                                                                             self.course.name,
                                                                                                             self.type,
                                                                                                             self.instructor.fullname,
                                                                                                             self.student_group.name,
                                                                                                             self.allowed_room.name)
        return str_val


class Data:
    student_groups = []
    instructors = []
    rooms = []
    courses = []
    periods_per_day = 0
    days_per_week = 0
    working_days = []
    classes = []
    _periods = []

    @staticmethod
    def set_working_days(days_dict):
        Data.working_days = []
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for d in days:
            if days_dict.get(d):
                Data.days_per_week += 1
                Data.working_days.append(d.capitalize())

    @staticmethod
    def set_classes(classes):
        Data.classes = classes

    @staticmethod
    def get_class(id):
        for c in Data.classes:
            if c.id == id:
                return c
        return Class(-1)

    @staticmethod
    def get_room(id):
        for r in Data.rooms:
            if r.id == id:
                return r
        return None

    @staticmethod
    def set_periods(start_time_str, duration):
        start_time = datetime.strptime(start_time_str, "%H:%M")
        print('Starttime={}'.format(start_time))

        print('Endtime={}'.format(start_time + timedelta(hours=duration)))
        for i in range(Data.periods_per_day):

            # Break after 3 classes
            if i != 0 and i % 3 == 0:
                start_time += timedelta(hours=duration)

            period = "{}-{}".format(datetime.strftime(start_time, "%H:%M"),
                                    datetime.strftime(start_time + timedelta(hours=duration), "%H:%M"))
            Data._periods.append(period)
            start_time += timedelta(hours=duration)
        print('{} periods'.format(Data.periods_per_day))


class Chromosome:

    def __init__(self, pick_initial_slots: bool):
        self.chromosome_len = Data.days_per_week * Data.periods_per_day * len(Data.rooms)
        self.slots = [-1] * self.chromosome_len
        self.assigned_slots = {}  # <class_id, slot_id>
        self.fitness = 0
        if pick_initial_slots:
            for i in range(len(Data.classes)):

                slot_id = random.randint(0, self.chromosome_len - 1)

                # Find an empty slot
                while self.slots[slot_id] != -1:
                    slot_id = random.randint(0, self.chromosome_len - 1)
                class_id = Data.classes[i].id
                self.slots[slot_id] = class_id
                self.assigned_slots[class_id] = slot_id

    def calculate_fitness(self):
        qs = 0
        for k, v in self.assigned_slots.items():
            class_id = k
            slot_id = v
            qs += self.calculate_gene_score(class_id, slot_id)

        self.fitness = qs / (3.0 * len(self.assigned_slots))

    def calculate_gene_score(self, class_id, slot_id):
        gs = 0
        room_id = Data.rooms[(slot_id * len(Data.rooms) * Data.days_per_week // len(self.slots)) % len(Data.rooms)].id
        if Data.get_class(class_id).is_room_allowed(room_id):
            gs += 1
        if self.instructor_available(slot_id):
            gs += 1
        if self.student_group_available(slot_id):
            gs += 1
        return gs

    def set_gene(self, slot_id, class_id):
        self.slots[slot_id] = class_id
        if class_id != -1:
            self.assigned_slots[class_id] = slot_id

    def instructor_available(self, slot_id):
        ins = Data.get_class(self.slots[slot_id]).instructor
        instructor_cls_count = 0
        k = slot_id % Data.periods_per_day
        day_id = (slot_id * Data.days_per_week // self.chromosome_len) % Data.days_per_week
        k += day_id * (self.chromosome_len // Data.days_per_week)
        rc = len(Data.rooms)
        for i in range(rc):
            if self.slots[k] == -1:
                continue
            elif Data.get_class(self.slots[k]).instructor == ins:
                instructor_cls_count += 1
            k += Data.periods_per_day

        return True if instructor_cls_count == 1 else False

    def student_group_available(self, slot_id):
        std_grp = Data.get_class(self.slots[slot_id]).student_group
        student_group_count = 0
        k = slot_id % Data.periods_per_day
        day_id = (slot_id * Data.days_per_week // self.chromosome_len) % Data.days_per_week
        k += day_id * (self.chromosome_len // Data.days_per_week)
        rc = len(Data.rooms)
        for i in range(rc):
            if self.slots[k] == -1:
                continue
            elif Data.get_class(self.slots[k]).student_group == std_grp:
                student_group_count += 1
            k += Data.periods_per_day
        return True if student_group_count == 1 else False

    def __str__(self):
        str_value = ""
        for s in self.slots:
            str_value = str_value + str(s) + " "
        for k, v in self.assigned_slots.items():
            class_id = str(k)
            slot_id = str(v)
            str_value = str_value + " | " + class_id + " " + slot_id + " | "
        return str_value

    def is_class_set(self, class_id):
        return class_id in self.assigned_slots


class Population:

    def __init__(self, population_size):
        self.population_size = population_size
        self.population = []
        self.best_fitness_score = 0
        for i in range(population_size):
            self.population.append(Chromosome(pick_initial_slots=True))

    def get_fittest_chromosome(self):
        max_val = -math.inf
        max_idx = -1
        for i in range(self.population_size):
            if self.population[i].fitness > max_val:
                max_val = self.population[i].fitness
                max_idx = i
        return self.population[max_idx]

    def get_least_chromosome_index(self):
        min_val = math.inf
        min_idx = -1
        for i in range(self.population_size):
            if self.population[i].fitness < min_val:
                min_val = self.population[i].fitness
                min_idx = i
        return min_idx

    def get_second_fittest_chromosome(self):
        max_idx = 0
        smax_idx = 0

        for i in range(self.population_size):
            if self.population[i].fitness > self.population[max_idx].fitness:
                max_idx = i
            elif self.population[i].fitness > self.population[smax_idx].fitness:
                smax_idx = i

        return self.population[smax_idx]

    def calculate_fitnesses(self):
        for ch in self.population:
            ch.calculate_fitness()
        self.best_fitness_score = self.get_fittest_chromosome().fitness

    def get_average_fitness(self):
        total_score = 0
        for ch in self.population:
            total_score += ch.fitness
        return total_score / self.population_size

    def __str__(self):
        str_val = ""
        for c in self.population:
            str_val += str(c)
        str_val += 'average fitness: ' + str(self.get_average_fitness())
        return str_val


class Generator:

    def __init__(self):
        self.population = None
        self.fitttest_chromosome = None
        self.second_fittest_chromosome = None
        self.offstring = None
        self.population_size = 0

    def init_population(self, population_size):
        self.population_size = population_size
        self.population = Population(population_size)

    def selection(self):
        self.fitttest_chromosome = self.population.get_fittest_chromosome()
        self.second_fittest_chromosome = self.population.get_second_fittest_chromosome()

    def crossover(self):
        offspring = Chromosome(pick_initial_slots=False)
        parent1 = self.fitttest_chromosome
        parent2 = self.second_fittest_chromosome
        for i in range(len(parent1.slots)):
            parent1_gene = parent1.slots[i]
            parent2_gene = parent2.slots[i]
            if parent1_gene == parent2_gene:
                if parent1_gene != -1:
                    offspring.set_gene(i, parent1_gene)
            elif parent1 == -1 and not offspring.is_class_set(parent2_gene):
                offspring.set_gene(i, parent2_gene)

            elif parent2 == -1 and not offspring.is_class_set(parent1_gene):
                offspring.set_gene(i, parent1_gene)

            else:
                if offspring.is_class_set(parent2_gene) and not offspring.is_class_set(parent1_gene):
                    offspring.set_gene(i, parent1_gene)

                elif offspring.is_class_set(parent1_gene) and not offspring.is_class_set(parent2_gene):
                    offspring.set_gene(i, parent2_gene)

                elif offspring.is_class_set(parent1_gene) and offspring.is_class_set(parent2_gene):
                    offspring.set_gene(i, -1)

                else:
                    parent2_gs = parent2.calculate_gene_score(parent2_gene, i)
                    parent1_gs = parent2.calculate_gene_score(parent1_gene, i)
                    if parent2_gs > parent1_gs:
                        offspring.set_gene(i, parent2_gene)

                    else:
                        offspring.set_gene(i, parent1_gene)

        for i in range(len(Data.classes)):
            if not offspring.is_class_set(Data.classes[i].id):
                slot_id = random.randint(0, parent2.chromosome_len - 1)
                while offspring.slots[slot_id] != -1:
                    slot_id = random.randint(0, parent2.chromosome_len - 1)
                offspring.set_gene(slot_id, Data.classes[i].id)
        self.offstring = offspring

    def add_offspring(self):
        least_fit_index = self.population.get_least_chromosome_index()
        self.population.population[least_fit_index] = self.offstring

    def mutation(self, mutation_rate):
        for i in range(self.population_size):

            if random.uniform(0, 1) <= mutation_rate:
                slot_id = random.randint(0, self.population.population[0].chromosome_len - 1)
                while self.population.population[i].slots[slot_id] != -1:
                    slot_id = random.randint(0, self.population.population[0].chromosome_len - 1)
                rand_class = random.randint(0, len(Data.classes) - 1)
                class_id = Data.classes[rand_class].id
                old_slot_id = self.population.population[i].assigned_slots[class_id]
                self.population.population[i].set_gene(old_slot_id, -1)
                self.population.population[i].set_gene(slot_id, class_id)

    def get_fittest_chromosome(self):
        return self.fitttest_chromosome


class Driver:
    population_size = 20
    max_generations = 2500
    mutation_rate = 0.2

    def generate_timetable(self):
        gen = Generator()
        gen.init_population(population_size=Driver.population_size)
        gen.population.calculate_fitnesses()

        print(str(gen.population))

        generation_count = 0
        print("Generation: {}, average_fitness: {}, max_fitnesss: {}".format(generation_count,
                                                                             gen.population.get_average_fitness(),
                                                                             gen.population.best_fitness_score))

        while gen.population.best_fitness_score < 1 and generation_count < Driver.max_generations:
            generation_count += 1

            gen.selection()
            gen.crossover()
            gen.mutation(Driver.mutation_rate)
            gen.add_offspring()

            gen.population.calculate_fitnesses()

            print(str(gen.population))

            print("Generation: {}, average_fitness: {}, max_fitnesss: {}".format(generation_count,
                                                                                 gen.population.get_average_fitness(),
                                                                                 gen.population.best_fitness_score))
        if abs(gen.population.best_fitness_score - 1.0) < 1e-9:
            return gen.population.get_fittest_chromosome()
        else:
            # return None
            return gen.population.get_fittest_chromosome()

    def generate_timetable_response(self, best_chromosome: Chromosome):
        res = []
        for i in range(best_chromosome.chromosome_len):
            class_ = Data.get_class(i)
            course = class_.course
            day = Data.working_days[(i * Data.days_per_week // best_chromosome.chromosome_len) % Data.days_per_week]
            room = Data.rooms[(i * len(Data.rooms) // best_chromosome.chromosome_len) % len(Data.rooms)]
            period = i % Data.periods_per_day
            period_str = Data._periods[period]
            stg = class_.student_group
            if stg is not None:
                res.append({'day': day, 'period': period_str, 'student_group': stg.name, 'room': room.name,
                            'course': course.name})
        print(res)
        return res


if __name__ == '__main__':
    course0 = Course("MATH", "101")
    course1 = Course("CHEM", "103")
    course2 = Course("PIC", "104")
    course3 = Course("CAED", "105")
    course4 = Course("ELN", "106")
    course5 = Course("BCP", "107")

    ins0 = Instructor("Padma")
    ins1 = Instructor("Shiva")
    ins2 = Instructor("Harish")
    ins3 = Instructor("Shiv")
    ins4 = Instructor("Shobha")
    ins5 = Instructor("Rahul")
    ins6 = Instructor("Meena")

    ins7 = Instructor("Soumya")
    ins8 = Instructor("Uma")
    ins9 = Instructor("Deepak")
    ins10 = Instructor("Dhruva")

    room0 = Room("308")
    room1 = Room("309")

    stg0 = StudentGroup("1A")
    stg1 = StudentGroup("1B")

    c0 = Class(course=course0, type="Lec", instructor=ins0, student_group=stg0, allowed_room=room0)
    c1 = Class(course=course0, type="Lec", instructor=ins0, student_group=stg0, allowed_room=room0)
    c2 = Class(course=course0, type="Lec", instructor=ins0, student_group=stg0, allowed_room=room0)
    c3 = Class(course=course1, type="Lec", instructor=ins1, student_group=stg0, allowed_room=room0)
    c4 = Class(course=course1, type="Lec", instructor=ins1, student_group=stg0, allowed_room=room0)
    c5 = Class(course=course1, type="Lec", instructor=ins1, student_group=stg0, allowed_room=room0)
    c6 = Class(course=course2, type="Lec", instructor=ins2, student_group=stg0, allowed_room=room0)
    c7 = Class(course=course2, type="Lec", instructor=ins2, student_group=stg0, allowed_room=room0)
    c8 = Class(course=course2, type="Lec", instructor=ins2, student_group=stg0, allowed_room=room0)
    c9 = Class(course=course3, type="Lec", instructor=ins3, student_group=stg0, allowed_room=room0)
    c10 = Class(course=course3, type="Lec", instructor=ins3, student_group=stg0, allowed_room=room0)
    c11 = Class(course=course3, type="Lec", instructor=ins3, student_group=stg0, allowed_room=room0)
    c12 = Class(course=course4, type="Lec", instructor=ins4, student_group=stg0, allowed_room=room0)
    c13 = Class(course=course4, type="Lec", instructor=ins4, student_group=stg0, allowed_room=room0)
    c14 = Class(course=course4, type="Lec", instructor=ins4, student_group=stg0, allowed_room=room0)
    c15 = Class(course=course5, type="Lec", instructor=ins6, student_group=stg0, allowed_room=room0)
    c16 = Class(course=course5, type="Lec", instructor=ins6, student_group=stg0, allowed_room=room0)
    c17 = Class(course=course5, type="Lec", instructor=ins6, student_group=stg0, allowed_room=room0)

    c18 = Class(course=course0, type="Lec", instructor=ins0, student_group=stg1, allowed_room=room1)
    c19 = Class(course=course0, type="Lec", instructor=ins0, student_group=stg1, allowed_room=room1)
    c20 = Class(course=course0, type="Lec", instructor=ins0, student_group=stg1, allowed_room=room1)
    c21 = Class(course=course1, type="Lec", instructor=ins7, student_group=stg1, allowed_room=room1)
    c22 = Class(course=course1, type="Lec", instructor=ins7, student_group=stg1, allowed_room=room1)
    c23 = Class(course=course1, type="Lec", instructor=ins7, student_group=stg1, allowed_room=room1)
    c24 = Class(course=course2, type="Lec", instructor=ins8, student_group=stg1, allowed_room=room1)
    c25 = Class(course=course2, type="Lec", instructor=ins8, student_group=stg1, allowed_room=room1)
    c26 = Class(course=course2, type="Lec", instructor=ins8, student_group=stg1, allowed_room=room1)
    c27 = Class(course=course3, type="Lec", instructor=ins9, student_group=stg1, allowed_room=room1)
    c28 = Class(course=course3, type="Lec", instructor=ins9, student_group=stg1, allowed_room=room1)
    c29 = Class(course=course3, type="Lec", instructor=ins9, student_group=stg1, allowed_room=room1)
    c30 = Class(course=course4, type="Lec", instructor=ins10, student_group=stg1, allowed_room=room1)
    c31 = Class(course=course4, type="Lec", instructor=ins10, student_group=stg1, allowed_room=room1)
    c32 = Class(course=course4, type="Lec", instructor=ins10, student_group=stg1, allowed_room=room1)
    c33 = Class(course=course5, type="Lec", instructor=ins6, student_group=stg1, allowed_room=room1)
    c34 = Class(course=course5, type="Lec", instructor=ins6, student_group=stg1, allowed_room=room1)
    c35 = Class(course=course5, type="Lec", instructor=ins6, student_group=stg1, allowed_room=room1)


    Data.courses = [course0, course1]
    Data.set_working_days({'monday': True, 'tuesday': True, 'wednesday': True, 'thursday': True, 'friday': True,
                           'saturday': True})
    Data.rooms = [room0, room1]
    Data.instructors = [ins0, ins1, ins2, ins3, ins4, ins5, ins6, ins7, ins8, ins9, ins10]
    Data.student_groups = [stg0, stg1]
    Data.set_classes(
        [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c12, c14, c15, c16, c18, c19, c20, c21, c22, c23, c24,
         c25, c26, c27, c28, c29, c30, c32, c33, c34])
    Data.periods_per_day = 6
    Data.set_periods("9:00", 1)

    driver = Driver()
    ans = driver.generate_timetable()
    driver.generate_timetable_response(ans)
