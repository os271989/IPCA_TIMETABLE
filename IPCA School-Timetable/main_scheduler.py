
from enum import Enum
import sqlite3
from tabulate import tabulate
import random
rnd = random.randrange

POP_SIZE = 15
ELITE_NBR = 2
MUTATION_RATE = 0.1
TOURNAMENT_SIZE = 3

#Classe para importar dados da DB
class DBGenerator:
  def __init__(self):
    self._connector = sqlite3.connect('data.db')
    self._cursor = self._connector.cursor()
    self._rooms = self.select_rooms()
    self._teachers = self.select_teachers()
    self._subjects = self.select_subjects()
    self._scheduleTimes = self.select_scheduleTimes()
    self._courses = self.select_courses()
    self._teacherRestrictionsTimes = self.select_teacherRestTimes()
    self._nbrClass = 0
    self._nbrClass = len(self._subjects)*2
    
  #Metodos para importar dados da BD
  def select_rooms(self):
    self._cursor.execute("select * from room")
    rooms = self._cursor.fetchall()
    roomsList = []
    for i in range (0, len(rooms)): roomsList.append(Room(rooms[i][0], rooms[i][1], rooms[i][2]))
    return roomsList
    
  def select_teachers(self):
    self._cursor.execute("select * from teacher")
    teachers = self._cursor.fetchall()
    teachersList = []
    for i in range(0, len(teachers)):
      teachersList.append(Teacher(teachers[i][0], teachers[i][1], teachers[i][2]))
    return teachersList
    
  def select_subjects(self):
    self._cursor.execute("select * from subject")
    subjects = self._cursor.fetchall()
    subjectsList = []
    for i in range(0, len(subjects)):
      subjectsList.append(Subject(subjects[i][0], subjects[i][1], self.select_classTeacher(subjects[i][0])))
    return subjectsList

  def select_scheduleTimes(self):  
    self._cursor.execute("select * from scheduleTimes")
    times = self._cursor.fetchall()
    timesList = []
    for i in range(0, len(times)):
      timesList.append(ClassTime(times[i][0], times[i][1], times[i][2]))
    return timesList
  
  def select_courses(self):
    self._cursor.execute("select * from courses")
    courses = self._cursor.fetchall()
    coursesList = []
    for c in range(0, len(courses)):
      coursesList.append(Courses(courses[c][0], courses[c][1], courses[c][2]))
    return coursesList
  
  def select_teacherRestTimes(self):
    self._cursor.execute("select * from teacher_restrictionTimes")
    teacherRest = self._cursor.fetchall()
    teacherRestList = []
    for r in range(0, len(teacherRest)):
      teacherRestList.append(Teacher_RestrictionsTime(teacherRest[r][0], teacherRest[r][1]))
    
  
  def select_classTeacher(self, subjectID):
    self._cursor.execute("select * from class where subject_id == '" + subjectID + "'")
    subjectTeachers = self._cursor.fetchall()
    teachersId = []
    #Para cada professor que leciona a disciplina vamos guardar o seu id
    for i in range(0, len(subjectTeachers)):
      teachersId.append(subjectTeachers[i][1])  #Par cod_disc[0]/cod_prof[1]
    teachersList = []
    #Procurar e devolver a lista de professores com este ID
    for i in range(0, len(self._teachers)):
      if self._teachers[i].get_id() in teachersId:
        teachersList.append(self._teachers[i])
    return teachersList[0]
  
  def get_rooms(self): return self._rooms
  def get_teachers(self): return self._teachers
  def get_subjects(self): return self._subjects
  def get_scheduleTimes(self): return self._scheduleTimes
  def get_nbrClass(self): return self._nbrClass

#Classe aula agendada para instanciação
class Subject:
  def __init__(self, id, name, teacher):
      self._id = id
      self._name = name
      self._teacher = teacher
  #Metodos para cada atributo
  def get_id(self): return self._id
  def get_name(self): return self._name
  def get_teacher(self): return self._teacher
  def __str__(self): return self._name

#Classe professor para instanciação
class Teacher:
  def __init__(self, id, name, abrev):
    self._id = id
    self._name = name
    self._abrev = abrev
  #Metodos para cada atributo
  def get_id(self): return self._id
  def get_name(self): return self._name
  def get_abrev(self): return self._abrev
  def __str__(self): return self._name

#Classe sala para instanciação
class Room:
  def __init__(self, id, name, abrev):
    self._id = id
    self._name = name
    self._abrev = abrev
  #Metodos para cada atributo
  def get_id(self): return self._id
  def get_name(self): return self._name
  def get_abrev(self): return self._abrev
  
#Classe hora de aula para instanciação
class ClassTime:
  def __init__(self, block, hour, prev_Block):
    self._block = block
    self._hour = hour
    self._prev_Block = prev_Block
  #Metodos para cada atributo
  def get_block(self): return self._block
  def get_hour(self): return self._hour
  def get_prev_Block(self): return self._prev_Block
  
#Classe cursos para instanciação
class Courses:
  def __init__(self, id, name, abrev): 
    self._id = id
    self._name = name
    self._abrev = abrev
  #Metodos para cada atributo
  def get_id(self): return self._id
  def get_name(self): return self._name
  def get_abrev(self): return self._abrev
  
class Teacher_RestrictionsTime:
  def __init__(self, id_teacher, block):
    self._id_teacher = id_teacher
    self._block = block
  #Metodos para cada atributo  
  def get_self_id_teacher(self): return self._id_teacher
  def get_block(self): return self._block
  
#Classe bloco de aula para instanciação
class ClassBlock:
  def __init__(self, id, scheduledClass):
    self._id = id
    self._scheduledClass = scheduledClass
    self._teacher = None
    self._classTime = None
    self._room = None
  #Metodos para cada atributo
  def get_id(self): return self._id
  def get_scheduledClass(self): return self._scheduledClass
  def get_teacher(self): return self._teacher
  def get_classTime(self): return self._classTime
  def get_room(self): return self._room
  def set_teacher(self, teacher): self._teacher = teacher
  def set_classTime(self, classTime): self._classTime = classTime
  def set_room(self, room): self._room = room
  def __str__(self):
    #Converter e retornar para string todos os atributos do bloco de aula
    return str(self._scheduledClass.get_id()) + "," + str(self._room.get_id()) + "," + str(self._teacher.get_id()) + "," + str(self._classTime.get_block())

#Classe para restrições possíveis de instanciar
class Restriction:
  class RestrictionType(Enum):
    TEACHER_ASSIGNED = 1
    ROOM_OCCUPIED = 2
    TEACHER_CONSECUTIVE_CLASS = 3
    #tipo de restrição e entre que aulas existe essa restrição
  def __init__(self, restrictionType, restrictionBetweenClass): 
    self._restrictionType = restrictionType
    self._restrictionBetweenClass = restrictionBetweenClass
  def get_restrictionType(self): return self._restrictionType
  def get_restrictionBetweenClass(self): return self._restrictionBetweenClass
  def __str__(self): return str(self._restrictionType) +" "+str(" and ".join(map(str, self._restrictionBetweenClass)))

#Classe horário para instanciação
class Schedule:
  def __init__(self):
    self._classes = []
    self._restrictions = []
    self._fitness = -1
    self._classNbr = 0
    self._fitnessChanged = True
  def get_classes(self):
    self._fitnessChanged = True
    return self._classes
  def get_restrictions(self): return self._restrictions
  def get_fitness(self):
    if (self._fitnessChanged): #Se for verdadeiro então calcula a função fitness e altera para falso
      self._fitness = self.fitness_calculation()
      self._fitnessChanged = False
    return self._fitness
  #Atribuir todas as disciplinas
  def initClasses(self):
    subjects = dataMng.get_subjects()
    for s in range(0, len(subjects)):
      newClass = ClassBlock(self._classNbr, subjects[s])
      self._classNbr += 1
      #Atribuir bloco horário aleatório a partir do conjunto de blocos disponíveis
      newClass.set_classTime(dataMng.get_scheduleTimes()[rnd(0, len(dataMng.get_scheduleTimes()))])
      #Atribuir sala aleatória a partir do conjunto de salas disponíveis
      newClass.set_room(dataMng.get_rooms()[rnd(0, len(dataMng.get_rooms()))])
      #Atribuir professor aleatório a partir do conjunto de professores disponíveis
      newClass.set_teacher(subjects[s].get_teacher())
      self._classes.append(newClass)
    return self
  #Devolver todas os blocos de aulas associados a um professor
  def get_teacher_classTimes(self, teacher):
    classTimes = list()
    for s in range(0, len(self._classes)):
      #Procurar em blocos horários os que estão associados ao ID do professor
      if(self._classes[s].get_teacher().get_id() == teacher.get_id()):
        classTimes.append(self._classes[s].get_classTime().get_block())
    return classTimes
  #####################################################################
  #Calcular função Fitness
  def fitness_calculation(self):
    self._restrictions = []
    classes = self.get_classes()
    for c in range(0, len(classes)):
      teacherConsecutiveClassesRestr = list()
      teacherConsecutiveClassesRestr.append(classes[c])
      #Testar se tem aulas consecutivas
      if (classes[c].get_classTime().get_prev_Block() in self.get_teacher_classTimes(classes[c].get_teacher())):
        self._restrictions.append(Restriction(Restriction.RestrictionType.TEACHER_CONSECUTIVE_CLASS, teacherConsecutiveClassesRestr))
      for j in range(0, len(classes)):
        if j >= c:
          #Para todas as aulas diferentes no mesmo bloco horário
          if (classes[c].get_classTime() == classes[j].get_classTime() and classes[c].get_id() != classes[j].get_id()):
            #Testar se tem a mesma sala atribuida
            if (classes[c].get_room() == classes[j].get_room()):
              roomOccupiedRestr = list()
              roomOccupiedRestr.append(classes[c])
              roomOccupiedRestr.append(classes[j])
              self._restrictions.append(Restriction(Restriction.RestrictionType.ROOM_OCCUPIED, roomOccupiedRestr))
            #Testar se mesmo professor associado a duas disciplinas diferentes no mesmo horário
            if (classes[c].get_teacher() == classes[j].get_teacher()): 
              teacherAssignedRestr = list()
              teacherAssignedRestr.append(classes[c])
              teacherAssignedRestr.append(classes[j])
              self._restrictions.append(Restriction(Restriction.RestrictionType.TEACHER_ASSIGNED, teacherAssignedRestr))
    #Quanto mais restrições violadas maior a função fitness, o ideal é serem 0 para devolver 1
    return 1 / (1.0 * len(self._restrictions) + 1)
  #Retornar todas as aulas atribuidas deste horário
  def __str__(self):
    value = ""
    for i in range(0, len(self._classes)-1): value += str(self._classes[i]) + ", "
    value += str(self._classes[len(self._classes) -1])
    return value
       
#Classe população para receber conjunto de horários
class Population:
  def __init__(self, size):
    self._size = size
    self._schedules = []
    #Popular segundo tamanho definido
    for i in range(0, size): self._schedules.append(Schedule().initClasses())
  def get_schedules(self): return self._schedules
    
#Definição do algoritmo genético e sua manipulação  
class GeneticAlg:
  
  #Envolver toda uma população para cruzamentos e mutações
  def evolve(self, pop): return self.population_Mutation(self.population_Crossover(pop))
  #Cruzamento de todos os horários da população
  def population_Crossover(self, pop):
    pop_Cross = Population(0)
    for r in range(ELITE_NBR):
      pop_Cross.get_schedules().append(pop.get_schedules()[r])
    r = ELITE_NBR
    #Efetuar torneio de maneira a selecionar 2 horários para cruzar
    while r < POP_SIZE:
      option1 = self.select_Tournament(pop).get_schedules()[0]
      option2 = self.select_Tournament(pop).get_schedules()[0]
      pop_Cross.get_schedules().append(self.crossover_Schedules(option1, option2))
      r += 1
    return pop_Cross
  
  #Mutação de toda a população
  def population_Mutation(self, pop):
    for i in range(ELITE_NBR, POP_SIZE):
      self.schedule_Mutation(pop.get_schedules()[i])
    return pop
  
  #Mutação de um horário
  @staticmethod
  def schedule_Mutation(scheduleMutate):
    schedule = Schedule().initClasses()
    for i in range(0, len(scheduleMutate.get_classes())):
      if MUTATION_RATE > random.random(): scheduleMutate.get_classes()[i] = schedule.get_classes()[i]
    return scheduleMutate
  
  #Cruzamento de dois horários
  @staticmethod
  def crossover_Schedules(sch1, sch2):
    schedule_Cross = Schedule().initClasses()
    for i in range(0, len(schedule_Cross.get_classes())):
      if (random.random() > 0.5): schedule_Cross.get_classes()[i] = sch1.get_classes()[i]
      else: schedule_Cross.get_classes()[i] = sch2.get_classes()[i]
    return schedule_Cross

  #Metodo para torneio de população e seleção de horários a cruzar
  @staticmethod
  def select_Tournament(pop):
    pop_Tour = Population(0)
    i = 0
    while i < TOURNAMENT_SIZE:
      pop_Tour.get_schedules().append(pop.get_schedules()[rnd(0, POP_SIZE)])
      i += 1
    pop_Tour.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    return pop_Tour
    
#Metodo para encontrar a melhor solução entre a população    
def choose_fittestSolution():
  generationQty = 0
  print("\n===== Generation " + str(generationQty) + " =====")
  population = Population(POP_SIZE)
  #Ordenar população por horários com menor fitness -> crescente
  population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)

  #Mostrar geração, horário tabelado e restrições violadas
  OutManager.display_gen(population)
  OutManager.display_scheduleTable(population.get_schedules()[0])
  OutManager.display_Restrictions(population.get_schedules()[0])
  geneticAlg = GeneticAlg()
  
  while population.get_schedules()[0].get_fitness() != 1.0:
    generationQty += 1
    print("\n----- GENERATION " + str(generationQty) + " -----")
    population = geneticAlg.evolve(population)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    OutManager.display_gen(population)
    OutManager.display_scheduleTable(population.get_schedules()[0])
    OutManager.display_Restrictions(population.get_schedules()[0])
  print("\n\n Best Solution found after " + str(generationQty) + " Generations\n")
    
  return population.get_schedules()[0]
    
#Class para configuração de Output
class OutManager:
  #Invocação de todos os métodos para mostrar dados
  @staticmethod
  def display_data_input():
    print("\n========== DADOS CARREGADOS ==========\n")
    OutManager.display_Teachers()
    OutManager.display_Subjects()
    OutManager.display_classTimes()
    OutManager.display_rooms()
  
  #Metodo para mostrar professores existentes
  @staticmethod
  def display_Teachers():
    teachers = dataMng.get_teachers()
    rows = []
    for i in range(0, len(teachers)):
      rows.append((teachers[i].get_id(), teachers[i].get_name(), teachers[i].get_abrev()))
    print("========== TEACHERS ==========\n")
    print(tabulate(rows, headers=["ID", "Teacher", "Abrev"]))
    print("\n======================================\n")
    
  #Metodo para mostrar disciplinas existente
  @staticmethod
  def display_Subjects():
    subjects = dataMng.get_subjects()
    rows = []
    for i in range(0, len(subjects)):
      rows.append((subjects[i].get_id(), subjects[i].get_name(), subjects[i].get_teacher()))
    print("========== SUBJECTS ==========\n")
    print(tabulate(rows, headers=["ID", "Subject", "Teacher"]))
    print("\n======================================\n")
    
  #Metodo para mostrar blocos horários existentes
  @staticmethod
  def display_classTimes():
    times = dataMng.get_scheduleTimes()
    rows = []
    for i in range(0, len(times)):
      rows.append((times[i].get_block(), times[i].get_hour(), times[i].get_prev_Block()))
    print("========== TIMES ==========\n")
    print(tabulate(rows, headers=["BLOCK", "TIME", "Prev_BLOCK"]))
    print("\n======================================\n\n")
  
  #Metodo para mostrar salas existentes
  @staticmethod
  def display_rooms():
    rooms = dataMng.get_rooms()
    rows = []
    for i in range(0, len(rooms)):
      rows.append((rooms[i].get_id(), rooms[i].get_name(), rooms[i].get_abrev()))
    print("========== ROOMS ==========\n")
    print(tabulate(rows, headers=["ID", "ROOM_NAME", "ABREVIATURE"]))
    print("\n======================================\n\n")

  #Metodo para mostrar horário perspetiva das salas
  @staticmethod
  def display_RoomSchedule(schedule):
    print("\n============= ROOM PERSPECTIVE =============\n")
    #Carregar todas as salas
    rooms = dataMng.get_rooms()
    rows = []
    #Iterar todas as salas existentes
    for r in range(0, len(rooms)):
      roomSchedule = list()
      #Iterar todas as aulas do horário
      for s in range(0, len(schedule.get_classes())):
        #Se a sala da aula for igual ao horário desta iteração então adiciona á lista de aulas da sala
        if (schedule.get_classes()[s].get_room() == rooms[r]):
          roomSchedule.append(str(schedule.get_classes()[s]))
      rows.append(str(rooms[r].get_id(), rooms[r].get_abrev() ), str(roomSchedule))
      print(tabulate(rows, headers=["Room_ID", "1", "2", "3", "4", "5"]))

  #Metodo para mostrar horário perspetiva dos professores
  @staticmethod
  def display_TeacherSchedule(schedule):
    print("\n============= TEACHER PERSPECTIVE =============\n")
    #Carregar todas os professores
    teachers = dataMng.get_teachers()
    rows = []
    #Iterar todos os professores existentes
    for t in range(0, len(teachers)):
      teacherSchedule = list()
      #Iterar todas as aulas do horário
      for c in range(0, len(schedule.get_classes())):
        #Se a sala da aula for igual ao horário desta iteração então adiciona á lista de aulas da sala
        if (schedule.get_classes()[c].get_teacher() == teachers[t]):
          teacherSchedule.append(str(schedule.get_classes()[c]))
      rows.append((teachers[t].get_id(), teachers[t].get_abrev(), str(teacherSchedule)))  
    print(tabulate(rows, headers=["Room_ID", "1", "2", "3", "4", "5"]))

  #Metodo para mostrar gerações de população
  @staticmethod
  def display_gen(population):
    schedules = population.get_schedules()
    rows = []
    #Iterar cada horário da população
    for s in range(0, len(schedules)):
      #Adicionar nº horário, função fitness arre. a 3 casas, nº de restrições violadas e horário
      rows.append((str(s+1), round(schedules[s].get_fitness(), 3), len(schedules[s].get_restrictions()), str("(" + schedules[s].__str__() + ")")))
    print("\n\n ========== Schedule Table =========\n")
    print(tabulate(rows, headers=("Shedule_Nbr".ljust(20), "Fitness".ljust(10), "Nbr_Restrictions_Violated".ljust(30), "ClassBlocks".ljust(500))))

#Metodo para mostrar horário tabelado
  @staticmethod
  def display_scheduleTable(schedule):
    classes = schedule.get_classes()
    rows = []
    for c in range(0, len(classes)):
      rows.append((str(c +1), classes[c].get_scheduledClass().get_id() + " (" + classes[c].get_scheduledClass().get_name() + 
                  " )", classes[c].get_room().get_abrev(),
                  classes[c].get_teacher().get_id() + " (" + str(classes[c].get_teacher().get_abrev()) + ")",
                  str(classes[c].get_classTime().get_block()) + " (" + classes[c].get_classTime().get_hour() + ")"))
    print("\n========== Schedule_Table ==========\n")
    print(tabulate(rows, headers=("Class_ID", "Subject_ID", "Subject", "Teacher", "Time_Block\n" ), numalign="left"))

#Metodo para mostrar restrições violadas
  @staticmethod
  def display_Restrictions(schedule):
    restrictions = schedule.get_restrictions()
    rows = []
    for r in range(0, len(restrictions)):
      rows.append((str(restrictions[r].get_restrictionType()), 
                  str(" and ".join(map(str, restrictions[r].get_restrictionBetweenClass())))))
    if (len(restrictions) > 0): 
      print("\n========== Restrictions Table ==========\n")
      print(tabulate(rows, headers=("Restriction_Type", "Between Class_blocks")))
    
    
dataMng = DBGenerator()
OutManager.display_data_input()   
schedule = choose_fittestSolution()
print("\nTeacher Perspective\n")
OutManager.display_TeacherSchedule(schedule)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    