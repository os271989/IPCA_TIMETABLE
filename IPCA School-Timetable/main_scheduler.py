
from enum import Enum
import sqlite3
from tabulate import tabulate
import random
import re
rnd = random.randrange

POP_SIZE =25   #Nº de horários a considerar em cada população quanto > menor o desempenho
ELITE_NBR = 3   #Nº de horários "elite" ou seja que não serão considerados para mutação
MUTATION_RATE = 0.02   #Taxa de mutação a considerar
CROSSOVER_RATE = 0.7   #Taxa de cruzamento dos cromossomas
TOURNAMENT_SIZE = 3   #Nº de horários a considerar para cada torneio
MAX_GENERATIONS = 3500  #Nº máximo de gerações a atingir

#Classe para importar dados da DB
class DBGenerator:
  def __init__(self):
    self._connector = sqlite3.connect('data.db')
    self._cursor = self._connector.cursor()
    self._teacherRestrictionsTimes = self.select_teacherRestTimes()
    self._rooms = self.select_rooms()
    self._teachers = self.select_teachers()
    self._subjects = self.select_subjects()
    self._scheduleTimes = self.select_scheduleTimes()
    self._courses = self.select_courses()
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
      subjectsList.append(Subject(subjects[i][0], subjects[i][1], subjects[i][2], self.select_classTeacher(subjects[i][0]), subjects[i][3]))
    return subjectsList

  def select_scheduleTimes(self):  
    self._cursor.execute("select * from scheduleTimes")
    times = self._cursor.fetchall()
    timesList = []
    for i in range(0, len(times)):
      timesList.append(ClassTime(times[i][0], times[i][1], times[i][2]))
    return timesList
  
  def select_courses(self):
    self._cursor.execute("select * from course")
    courses = self._cursor.fetchall()
    coursesList = []
    for c in range(0, len(courses)):
      coursesList.append(Course(courses[c][0], courses[c][1], courses[c][2]))
    return coursesList
  
  def select_teacherRestTimes(self):
    self._cursor.execute("select * from teacher_restrictionTimes")
    teacherRest = self._cursor.fetchall()
    teacherRestList = []
    for r in range(0, len(teacherRest)):
      teacherRestList.append(Teacher_RestrictionsTime(teacherRest[r][0], teacherRest[r][1]))
    return teacherRestList
  
  def select_classTeacher(self, subjectID):
    self._cursor.execute("select * from class_Teachers where subject_id == '" + subjectID + "'")
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
    return teachersList
  
  #Devolver todas as restrições horárias de um professor
  def set_teacher_Time_Restrictions(self):
    timeRestrictions = self.get_teacherRestrictions()
    teachers = self.get_teachers()
    teacherRestrictions = list()
    for t in range(0, len(teachers)):
      for r in range(0, len(timeRestrictions)):
        if(timeRestrictions[r].get_id_teacher() == teachers[t].get_id()):
          teachers[t].get_restrictions().append(timeRestrictions[t])
  
  def get_rooms(self): return self._rooms
  def get_teachers(self): return self._teachers
  def get_subjects(self): return self._subjects
  def get_scheduleTimes(self): return self._scheduleTimes
  def get_nbrClass(self): return self._nbrClass
  def get_teacherRestrictions(self): return self._teacherRestrictionsTimes
  def get_courses(self): return self._courses

#Classe aula agendada para instanciação
class Subject:
  def __init__(self, id, name, abrev, teacher, course):
      self._id = id
      self._name = name
      self._teacher = teacher
      self._course = course
      self._abrev = abrev
      self._assigned = 0
  #Metodos para cada atributo
  def get_id(self): return self._id
  def get_name(self): return self._name
  def get_teacher(self): return self._teacher
  def get_course(self): return self._course
  def get_abrev(self): return self._abrev
  def get_assigned(self): return self._assigned
  def set_assigned(self):
    if (self._assigned < 4): self._assigned += 2
  def __str__(self): return self._name

#Classe professor para instanciação
class Teacher:
  def __init__(self, id, name, abrev):
    self._id = id
    self._name = name
    self._abrev = abrev
    self._restrictions = []
    
  #Metodos para cada atributo
  def get_id(self): return self._id
  def get_name(self): return self._name
  def get_abrev(self): return self._abrev
  def get_restrictions(self): return self._restrictions
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
class Course:
  def __init__(self, id, name, abrev): 
    self._id = id
    self._name = name
    self._abrev = abrev
    self._freeDay = -1
  #Metodos para cada atributo
  def get_id(self): return self._id
  def get_name(self): return self._name
  def get_abrev(self): return self._abrev
  def get_freeDay(self): return self._freeDay
  def set_freeDay(self, value): self._freeDay = value
  def __str__(self): return self._name
  
#Classe restrições horárias para instanciação
class Teacher_RestrictionsTime:
  def __init__(self, id_teacher, block):
    self._id_teacher = id_teacher
    self._block = block
  #Metodos para cada atributo  
  def get_id_teacher(self): return self._id_teacher
  def get_block(self): return self._block
  
#Classe bloco de aula para instanciação
class ClassBlock:
  def __init__(self, id, subject, course):
    self._id = id
    self._subject = subject
    self._teacher = None
    self._classTime = None
    self._room = None
  #Metodos para cada atributo
  def get_id(self): return self._id
  def get_subject(self): return self._subject
  def get_teacher(self): return self._teacher
  def get_classTime(self): return self._classTime
  def get_room(self): return self._room
  def set_teacher(self, teacher): self._teacher = teacher
  def set_classTime(self, classTime): self._classTime = classTime
  def set_room(self, room): self._room = room
  def __str__(self):
    #Converter e retornar para string todos os atributos do bloco de aula
    return str(self._subject.get_abrev()) + ", " + str(self._room.get_abrev()) +  ", " + str(self._classTime.get_block())

#Classe para restrições possíveis de instanciar
class Restriction:
  class RestrictionType(Enum):
    TEACHER_ASSIGNED = 15    #Professor com sobreposição de aulas
    ROOM_OCCUPIED = 15       #Sala com sobreposição de aulas
    TEACHER_RESTRICTION_TIME = 5  #Restrição de horário do professor violada
    SUBJECT_TEACHERS_OVERLAP = 10  #Disciplina de um curso lecionada por mais de 1 professor
    COURSE_FREE_DAY = 7.5     #Curso sem nenhum dia livre
    TEACHER_FREE_DAY = 5    #Professor sem nenhum dia livre
    SUBJECT_QUANTITY = 10    #Disciplina sem as 4h semanais atribuidas
    DAY_OVERLOAD = 10    #Dia com mais de 3 blocos horários atribuídos
    SUBJECT_DAY_ASSIGNED = 10  #Aula já atribuída nesse dia
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
    
  def get_classNbr(self): return self._classNbr
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
      idTeacher = 0
      assigned = 0
      while (assigned != 4):
        newClass = ClassBlock(self._classNbr, subjects[s], subjects[s].get_course())
        subjects[s].set_assigned()
        self._classNbr += 1
        #Atribuir bloco horário aleatório a partir do conjunto de blocos disponíveis
        newClass.set_classTime(dataMng.get_scheduleTimes()[rnd(0, len(dataMng.get_scheduleTimes()))])
        #Atribuir sala aleatória a partir do conjunto de salas disponíveis
        newClass.set_room(dataMng.get_rooms()[rnd(0, len(dataMng.get_rooms()))])
        if (idTeacher == 0):
          #Atribuir professor aleatório a partir do conjunto de professores disponíveis para a disciplina
          newClass.set_teacher(subjects[s].get_teacher()[rnd(0, len(subjects[s].get_teacher()))])
          idTeacher = newClass.get_teacher()
        else:
          newClass.set_teacher(idTeacher)
        self._classes.append(newClass)
        assigned +=2
    return self
  
  #Devolver todas os blocos de aulas associados a um professor
  def get_teacher_classTimes(self, teacher):
    classTimes = list()
    for s in range(0, len(self._classes)):
      #Procurar em blocos horários os que estão associados ao ID do professor
      if(self._classes[s].get_teacher().get_id() == teacher.get_id()):
        classTimes.append(self._classes[s].get_classTime().get_block())
    return classTimes
    
   #Devolver todas os blocos horários de aulas associados a um curso
  def get_Course_classTimes(self, course):
    classTimes = list()
    for s in range(0, len(self._classes)):
      #Procurar em blocos horários os que estão associados ao ID do professor
      if(self._classes[s].get_subject().get_course() == course.get_id()):
        classTimes.append(self._classes[s].get_classTime().get_block())
    return classTimes
  
  #Devolver todas os blocos de aulas associados a um curso
  def get_Course_classBlocks(self, course):
    classes = list()
    for s in range(0, len(self._classes)):
      #Procurar em blocos horários os que estão associados ao ID do professor
      if(self._classes[s].get_subject().get_course() == course.get_id()):
        classes.append(self._classes[s])
    return classes
  
  #Procurar se o curso tem algum dia livre
  def verify_Course_FreeDay(self, courseClasses, course):
    #aux = ['BL12', 'BL15', 'BL21', 'BL23','BL24', 'BL35', 'BL42', 'BL43', 'BL33', 'BL14']
    weekDays = [11, 21, 31, 41, 51]   #1º bloco de cada dia da semana -> seg/sex
    aux = courseClasses
    #weekDays.reverse()
    aux.sort(key=lambda aux : list(map(int, re.findall(r'\d+', aux)))[0])   #ordenar por ordem crescente
    sliceObject = slice(2, 4 ,1)
    dayAux = int(aux[0][sliceObject]) #Retirar apenas a parte numérica do bloco horário
    
    for d in range(0, len(weekDays)):
      cont = 0
      for b in range(0, len(aux)):
        dayAux = int(aux[b][sliceObject])
        if(dayAux >= weekDays[d] and dayAux <= weekDays[d]+10): #Nunca mais de 10 blocos por dia pois os dias são de 10 em 10
          cont +=1
      if (cont == 0): 
        return d
        #course.set_freeDay(d)
        #return True
    #return False
    return -1
  
  #Verificar se cada curso apenas tem um máximo de 3 blocos diários    
  def verify_Hours_Day(sel, courseClasses):
    aux = courseClasses
    periods = dataMng.get_scheduleTimes()
    aux.sort(key=lambda aux : list(map(int, re.findall(r'\d+', aux)))[0])
    blockRestrictions = list()
    for c in range(0, len(aux)):
      blocks = 0
      for p in range(0, len(periods)):
        if(periods[p].get_block() == aux[c]):
          if (periods[p].get_prev_Block() != ""):
            blocks += 1
      if (blocks > 3):
        blockRestrictions.append(Restriction(Restriction.RestrictionType.DAY_OVERLOAD, aux[c]))    
    return blockRestrictions         
   
  #Procurar se o curso tem algum dia livre
  def verify_Course_SubjectDay(self, courseClasses):
    weekDays = [11, 21, 31, 41, 51]   #1º bloco de cada dia da semana -> seg/sex
    aux = courseClasses
    aux.sort(key=lambda x: x.get_classTime().get_block(), reverse=False)
    #aux.sort(key=lambda aux : list(map(int, re.findall(r'\d+', aux)))[0])   #ordenar por ordem crescente
    sliceObject = slice(2, 4 ,1)
    dayAux = int(aux[0].get_classTime().get_block()[sliceObject]) #Retirar apenas a parte numérica do bloco horário
    
    for d in range(0, len(weekDays)):
      cont = 0
      for b in range(0, len(aux)):
        dayAux = int(aux[b].get_classTime().get_block()[sliceObject])
        subAux = aux[d].get_subject().get_id()
        if(dayAux >= weekDays[d] and dayAux <= weekDays[d]+10): #Nunca mais de 10 blocos por dia pois os dias são de 10 em 10
          if(aux[b].get_subject().get_id() == subAux):
            cont +=1
      if (cont > 1): 
        return aux[d].get_subject().get_abrev()
        #course.set_freeDay(d)
        #return True
    #return False
    return 0 
  #####################################################################
  #Calcular função Fitness
  def fitness_calculation(self):
    self._restrictions = []
    classes = self.get_classes()
    teachers = dataMng.get_teachers()
    courses = dataMng.get_courses()
    #--------------------------------------- TESTES DE RESTRIÇÕES ------------------------------------#
    for c in range(0, len(classes)):
      #Testar se tem aulas em blocos indicados como indisponivel
      if (classes[c].get_classTime().get_block() in classes[c].get_teacher().get_restrictions()): 
        teacherTimeRestr = list()
        teacherTimeRestr.append(classes[c].get_classTime().get_name())       
        self._restrictions.append(Restriction(Restriction.RestrictionType.TEACHER_RESTRICTION_TIME, teacherTimeRestr))
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
        #Testar se mesma disciplina está a ser lecionada por professores diferentes
        if(classes[c].get_subject() == classes[j].get_subject() and classes[c].get_teacher() != classes[j].get_teacher()):
          teacherAlternate = list()
          teacherAlternate.append(classes[c])
          teacherAlternate.append(classes[j])
          self._restrictions.append(Restriction(Restriction.RestrictionType.SUBJECT_TEACHERS_OVERLAP, teacherAlternate))
          
      #Testar se não foram atribuidos os 2 blocos da disciplina
      if (classes[c].get_subject().get_assigned() != 4): 
        classAssigned = list()
        classAssigned.append(classes[c])
        self._restrictions.append(Restriction(Restriction.RestrictionType.SUBJECT_QUANTITY, classAssigned))
    #Testar se o curso tem algum dia livre
    for c in range(0,len(courses)):
      aux = self.get_Course_classTimes(courses[c])
      free = self.verify_Course_FreeDay(aux, courses[c])
      if (free  == -1 ):
        CourseFreeDay = list()
        CourseFreeDay.append(courses[c].get_abrev())
        self._restrictions.append(Restriction(Restriction.RestrictionType.COURSE_FREE_DAY, CourseFreeDay))
        #Verificar se não tem mais de 3 blocos horários por dia
        restrictions = self.verify_Hours_Day(aux)
        if (len(restrictions) > 0):
          for r in range(0, len(restrictions)):
            self._restrictions.append(restrictions[r])
      else: courses[c].set_freeDay(free)
      
      #Verificar se há alguma disciplina atribuida mais do que uma vez no mesmo dia
      subDay = self.verify_Course_SubjectDay(self.get_Course_classBlocks(courses[c]))
      if (subDay != 0):
        self._restrictions.append(Restriction(Restriction.RestrictionType.SUBJECT_DAY_ASSIGNED, subDay))
      
      #Cálculo de todos os pesos das restrições violadas neste horário 
      fitnessWeight = 0
    for r in range(0, len(self._restrictions)):
      fitnessWeight += self._restrictions[r].get_restrictionType().value
        
    #Quanto mais restrições violadas menor a função fitness (aprox de 0), o ideal é serem 0 para devolver 1
    #return 1 / (1.0 * len(self._restrictions) + 1)
    return 1 / (fitnessWeight + 1)
 
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
      if (random.random() > CROSSOVER_RATE): schedule_Cross.get_classes()[i] = sch1.get_classes()[i]
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
  print("\n===== GENERATION " + str(generationQty) + " =====")
  population = Population(POP_SIZE)
  #Ordenar população por horários com menor fitness -> crescente
  population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
  #Mostrar geração, horário tabelado e restrições violadas
  OutManager.display_Gen(population)
  geneticAlg = GeneticAlg()
  
  while (generationQty < MAX_GENERATIONS and population.get_schedules()[0].get_fitness() != 1.0):
    generationQty += 1
    print("\n===== GENERATION " + str(generationQty) + " =====")
    population = geneticAlg.evolve(population)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    OutManager.display_Gen(population)
    OutManager.display_Restrictions(population.get_schedules()[0])
  
  print("\n\n Best Solution found after " + str(generationQty) + " Generations\n")
  OutManager.display_Gen(population)
  OutManager.display_Restrictions(population.get_schedules()[0])
      
  return population.get_schedules()[0]
    
#Class para configuração de Output
class OutManager:
  #Invocação de todos os métodos para mostrar dados
  @staticmethod
  def display_data_input():
    print("\n========== DADOS CARREGADOS ==========\n")
    OutManager.display_Teachers()
    OutManager.display_TeachersRestrictions()
    OutManager.display_ClassTimes()
    OutManager.display_Courses()
    OutManager.display_Subjects()
    OutManager.display_Rooms()
  
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
      rows.append((subjects[i].get_id(), subjects[i].get_name(), ([str(item.get_name()) for item in subjects[i].get_teacher()])))
    print("========== SUBJECTS ==========\n")
    print(tabulate(rows, headers=["ID", "Subject", "Teacher"]))
    print("\n======================================\n")
    
  #Metodo para mostrar blocos horários existentes
  @staticmethod
  def display_ClassTimes():
    times = dataMng.get_scheduleTimes()
    rows = []
    for i in range(0, len(times)):
      rows.append((times[i].get_block(), times[i].get_hour(), times[i].get_prev_Block()))
    print("========== TIMES ==========\n")
    print(tabulate(rows, headers=["BLOCK", "TIME", "Prev_BLOCK"]))
    print("\n======================================\n\n")
  
  #Metodo para mostrar salas existentes
  @staticmethod
  def display_Rooms():
    rooms = dataMng.get_rooms()
    rows = []
    for i in range(0, len(rooms)):
      rows.append((rooms[i].get_id(), rooms[i].get_name(), rooms[i].get_abrev()))
    print("========== ROOMS ==========\n")
    print(tabulate(rows, headers=["ID", "ROOM_NAME", "ABREVIATURE"]))
    print("\n======================================\n\n")
    
  #Metodo para mostrar cursos existentes
  @staticmethod
  def display_Courses():
    courses = dataMng.get_courses()
    rows = []
    for i in range(0, len(courses)):
      rows.append((courses[i].get_id(), courses[i].get_name(), courses[i].get_abrev()))
    print("========== COURSES ==========\n")
    print(tabulate(rows, headers=["ID", "COURSE_NAME", "ABREVIATURE"]))
    print("\n======================================\n\n")

  @staticmethod
  def display_TeachersRestrictions():
    restrictions = dataMng.get_teacherRestrictions()
    teachers = dataMng.get_teachers()
    rows = []
    for t in range(0, len(teachers)):
      for r in range(0, len(restrictions)):
        if(restrictions[r].get_block() == teachers[t].get_id()):
          rows.append((teachers[t].get_name(),str(restrictions[r].get_id())))

    print("========== TEACHERS TIME RESTRICTIONS ==========\n")
    print(tabulate(rows, headers=("NAME", "BLOCK")))
    print("\n======================================\n")

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
    print(tabulate(rows, headers=["Room_ID", "Teacher", "Time_Blocks"]))
  
  #Metodo para mostrar dia livre de cada curso
  @staticmethod
  def display_CourseFreeDay(schedule):
    print("\n============= COURSES FREE DAY =============\n")
    courses = dataMng.get_courses()
    rows = []
    days = ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira"]
    for c in range(0, len(courses)):
      if (courses[c].get_freeDay() != -1):
        rows.append((courses[c].get_id(), courses[c].get_name(), days[courses[c].get_freeDay()]))
    print(tabulate(rows, headers=["Course_ID", "Name", "Free Day"]))

  #Metodo para mostrar gerações de população
  @staticmethod
  def display_Gen(population):
    schedules = population.get_schedules()
    rows = []
    #Iterar cada horário da população
    for s in range(0, len(schedules)):
      #Adicionar nº horário, função fitness arre. a 3 casas, nº de restrições violadas e horário
      rows.append((str(s+1), round(schedules[s].get_fitness(), 3), len(schedules[s].get_restrictions()), str(schedules[s].get_classNbr())))
      ''' str("(" + schedules[s].__str__() + ")"))) '''
    print("\n\n ========== Schedule Table =========\n")
    print(tabulate(rows, headers=("Shedule_Nbr", "Fitness", "Nbr_Restrictions_Violated", "ClassBlocks")))

#Metodo para mostrar horário tabelado
  @staticmethod
  def display_ScheduleTableClass(schedule):
    classes = schedule.get_classes()
    rows = []
    for c in range(0, len(classes)):
      rows.append((str(c +1), classes[c].get_subject().get_id() + " (" + classes[c].get_subject().get_name() + 
                  " )", classes[c].get_room().get_abrev(),
                  classes[c].get_teacher().get_id() + " (" + str(classes[c].get_teacher().get_abrev()) + ")",
                  str(classes[c].get_classTime().get_block()) + " (" + classes[c].get_classTime().get_block() + ")"))
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
      print("Restrições Violadas:")
      print(len(rows))
      print(tabulate(rows, headers=("Restriction_Type", "Between Class_blocks")))
    
    
dataMng = DBGenerator()
dataMng.set_teacher_Time_Restrictions()
OutManager.display_data_input()   
schedule = choose_fittestSolution()
print("\nTeacher Perspective\n")
OutManager.display_TeacherSchedule(schedule)
OutManager.display_ScheduleTableClass(schedule)
OutManager.display_CourseFreeDay(schedule)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    