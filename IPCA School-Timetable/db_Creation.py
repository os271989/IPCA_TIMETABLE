import sqlite3 as sql

connector = sql.connect("data.db")
cursor = connector.cursor()

#Criação da tabela disciplinas 
cursor.execute("""create table subject (id text, name text, abrev text)""")
cursor.execute("insert into subject values"
                "('400', 'Fundamentos de Medicina I', 'FMI'  ),"
                "('401', 'Programacao Imperativa', 'PI' ),"
                "('402', 'Matemática Discreta e Algebra Linear', 'MDAL' ),"
                "('403', 'Cálculo', 'CAL' ),"
                "('404', 'Teoria dos Circuitos Elétricos', 'TCE' ),"
                "('405', 'Fundamentos de Medicina II', 'FMII' ),"
                "('406', 'Estrutura de Dados Avançada', 'EDA' ),"
                "('407', 'Redes de Computadores', 'RC' ),"
                "('408', 'Bioeletricidade', 'BIOELEC' ),"
                "('409', 'Bioestatística', 'BIOESTA' ),"
                "('410', 'Gestão de Sistemas de Informação', 'GSI' ),"
                "('411', 'Inteligência Artificial', 'IA' ),"
                "('412', 'Registo Clínico Eletrónico', 'RCE' ),"
                "('413', 'Análise de Séries Temporais', 'AST' ),"
                "('414', 'Integração de Sistemas Clínicos', 'ISC' ),"
                "('415', 'Cálculo', 'CAL' ),"
                "('416', 'Álgebra Linear', 'ALG' ),"
                "('417', 'Redes de Computadores', 'RC' ),"
                "('418', 'Laboratórios de Informática', 'LI' ),"
                "('419', 'Programação Orientada a Objetos', 'POO' ),"
                "('420', 'Análise e Modelação de Software', 'AMS' ),"
                "('421', 'Fundamentos de Física', 'FFIS' ),"
                "('422', 'Projeto de Engenharia de Software', 'PES' ),"
                "('423', 'Armazenamento e Acesso a Dados', 'AAD' ),"
                "('424', 'Programação de Dispositivos Móveis', 'PDM' ),"
                "('425', 'Integração de Sistemas de Informação', 'ISI' ),"
                "('426', 'Inteligência Artificial', 'IA' ),"
                "('427', 'Sistemas Embebidos e de Tempo Real', 'SETR' ),"
                "('428', 'Projeto Aplicado', 'PA' ),"
                "('429', 'Teoria dos Circuitos Elétricos', 'TCE' ),"
                "('430', 'Sistemas Digitais', 'SD' ),"
                "('431', 'Matemática Discreta e Algebra Linear', 'MDAL' ),"
                "('432', 'Cálculo', 'CAL' ),"
                "('433', 'Teoria de Sistemas e Controlo', 'TSC' ),"
                "('434', 'Arquitetura de Sistemas Computacionais', 'ASC' ),"
                "('435', 'Programação Orientada a Objetos', 'POO' ),"
                "('436', 'Eletrónica II', 'ELECII' ),"
                "('437', 'Processamento de Sinal', 'PS' ),"
                "('438', 'Instrumentação e Medidas', 'IM' ),"
                "('439', 'Robótica', 'ROB' ),"
                "('440', 'Instalações Eléctricas', 'IE' ),"
                "('441', 'Redes de Computadores e Sistemas Distribuídos', 'RCSD' ),"
                "('442', 'Análise de Matemática', 'AM' ),"
                "('443', 'Ciência e Engenharia dos Materiais', 'CEM' ),"
                "('444', 'Processos Industriais de Fabrico I', 'PIFI' ),"
                "('445', 'Algoritmos e Estruturas de Dados', 'AED' ),"
                "('446', 'Introdução à Engenharia e Gestão Industrial', 'IEGI' ),"
                "('447', 'Mecânica dos Materiais em Engenharia', 'MME' ),"
                "('448', 'Teoria de Sistemas e Controlo', 'TSC' ),"
                "('449', 'Processos Industriais de Fabrico II', 'PIFII' ),"
                "('450', 'Armazenamento e Acesso a Dados', 'AAD' ),"
                "('451', 'Estatística', 'ESTA' ),"
                "('452', 'Projetos de investimento', 'PINV' ),"
                "('453', 'Gestão da Qualidade e Segurança', 'GQS' ),"
                "('454', 'Tecnologias industriais avançadas', 'TIA' ),"
                "('455', 'Gestão de operações', 'GOP' ),"
                "('456', 'Logistica', 'LOG' )"
                
                ) 

#Criação da tabela professores
cursor.execute("""create table teacher(id text, name text, abrev text)""")
cursor.execute("insert into teacher values "
                "('300', 'André Carvalho', 'André C.'),"
                "('301', 'Andreia Monteiro', 'Andreia M.'),"
                "('302', 'António Rocha', 'António R.'),"
                "('303', 'Bruno Oliveira', 'Bruno O.'),"
                "('304', 'Carlos Plácido', 'Carlos P.'),"
                "('305', 'Vinícius Silva', 'Vinícius S.'),"
                "('306', 'Célio Carvalho', 'Célio C.'),"
                "('307', 'Daniel Miranda', 'Daniel M.'),"
                "('308', 'Estela Vilhena', 'Estela V.'),"
                "('309', 'Gabriela Viana', 'Gabriela V'),"
                "('310', 'Helena Torres', 'Helena T.'),"
                "('311', 'João Oliveira', 'João O.'),"
                "('312', 'João Pedro Silva', 'João P.S.'),"
                "('313', 'João Pinto', 'João P.'),"
                "('314', 'Joaquim Gonçalves', 'Joaquim G.'),"
                "('315', 'Joaquim Silva', 'Joaquim S.'),"
                "('316', 'José Brito', 'José B.'),"
                "('317', 'Luis Ferreira', 'Luis F'),"
                "('318', 'Luís Moreira', 'Luís M.'),"
                "('319', 'Manuela Cunha', 'Manuela C.'),"
                "('320', 'Martinha Pereira', 'Martinha P.'),"
                "('321', 'Natália Rego', 'Natália R.'),"
                "('322', 'Nuno Costa', 'Nuno C.'),"
                "('323', 'Nuno Lopes', 'Nuno L.'),"
                "('324', 'Nuno Mendes', 'Nuno M.'),"
                "('325', 'Nuno Rodrigues', 'Nuno R.'),"
                "('326', 'Óscar Ribeiro', 'Óscar R.'),"
                "('327', 'Patrícia Leite', 'Patrícia L.'),"
                "('328', 'Paulo Macedo', 'Paulo M.'),"
                "('329', 'Paulo Teixeira', 'Paulo T'),"
                "('330', 'Pedro Morais', 'Pedro M.'),"
                "('331', 'Rui Abreu', 'Rui A.'),"
                "('332', 'Sandro Carvalho', 'Sandro C.'),"
                "('333', 'Sara Cruz', 'Sara C.'),"
                "('334', 'Sérgio Pereira', 'Sérgio P.'),"
                "('335', 'Teresa Abreu', 'Teresa A.')"
                )

#Criação da tabela salas
cursor.execute("""create table room(id text, name text, abrev text)""")
cursor.execute("insert into room values "
                "('100', 'Auditorio EST', 'Audit EST'),"
                "('101', 'Lab de Automacao', 'Lab de Autom.'),"
                "('102', 'Lab Eletronica', 'Lab Eletr'),"
                "('103', 'Lab Internet of things', 'Lab IoT'),"
                "('104', 'Lab Redes', 'Lab Redes'),"
                "('105', 'Sala 4', 'Sala 4'),"
                "('106', 'Sala A', 'Sala A'),"
                "('107', 'Sala C', 'Sala C'),"
                "('108', 'Sala E', 'Sala E'),"
                "('109', 'Sala N', 'Sala N'),"
                "('110', 'Sala T', 'Sala T')"
                )

#Criação da tabela aulas com o par disciplina/professor
cursor.execute("""create table class_Teacher(subject_id text, id_tea text, id_course text)""")
cursor.execute("insert into class_Teacher values"
                "('400', '311', '200'),"
                "('401', '306', '200'),"
                "('402', '335', '200'),"
                "('403', '301', '200'),"
                "('404', '309', '200'),"
                "('405', '311', '201'),"
                "('406', '306', '201'),"
                "('407', '323', '201'),"
                "('408', '321', '201'),"
                "('409', '308', '201'),"
                "('410', '327', '202'),"
                "('411', '314', '202'),"
                "('412', '312', '202'),"
                "('413', '308', '202'),"
                "('414', '306', '202'),"
                "('415', '320', '203'),"
                "('416', '335', '203'),"
                "('417', '328', '203'),"
                "('418', '326', '203'),"
                "('419', '306', '204'),"
                "('420', '315', '204'),"
                "('421', '307', '204'),"
                "('422', '315', '204'),"
                "('423', '314', '204'),"
                "('424', '317', '205'),"
                "('425', '317', '205'),"
                "('426', '314', '205'),"
                "('427', '328', '205'),"
                "('428', '327', '205'),"
                "('429', '310', '206'),"
                "('430', '316', '206'),"
                "('431', '335', '206'),"
                "('432', '308', '206'),"
                "('433', '316', '207'),"
                "('434', '326', '207'),"
                "('435', '313', '207'),"
                "('436', '334', '207'),"
                "('437', '331', '208'),"
                "('438', '313', '208'),"
                "('439', '303', '208'),"
                "('440', '331', '208'),"
                "('441', '323', '208'),"
                "('442', '307', '209'),"
                "('443', '307', '209'),"
                "('444', '304', '209'),"
                "('445', '325', '209'),"
                "('446', '305', '209'),"
                "('447', '309', '210'),"
                "('448', '305', '210'),"
                "('449', '300', '210'),"
                "('450', '329', '210'),"
                "('451', '333', '210'),"
                "('452', '304', '211'),"
                "('453', '319', '211'),"
                "('454', '300', '211'),"
                "('455', '319', '211'),"
                "('456', '302', '211')"
                )

#Criação dos blocos de aulas de 2h especificos para cada dia da semana
cursor.execute("""create table scheduleTimes(block text, hour text, prev_Block)""")
cursor.execute("insert into scheduleTimes values"
                "('BL01', 'Segunda 09:00 - 11:00', ''),"
                "('BL02', 'Segunda 11:00 - 13:00', 'BL01'),"
                "('BL03', 'Segunda 14:00 - 16:00', 'BL02'),"
                "('BL04', 'Segunda 16:00 - 18:00', 'BL03'),"
                "('BL05', 'Segunda 18:00 - 20:00', 'BL04'),"
                "('BL06', 'Terça 09:00 - 11:00', ''),"
                "('BL07', 'Terça 11:00 - 13:00', 'BL06'),"
                "('BL08', 'Terça 14:00 - 16:00', 'BL07'),"
                "('BL09', 'Terça 16:00 - 18:00', 'BL08'),"
                "('BL10', 'Terça 18:00 - 20:00', 'BL09'),"
                "('BL11', 'Quarta 09:00 - 11:00', ''),"
                "('BL12', 'Quarta 11:00 - 13:00', 'BL11'),"
                "('BL13', 'Quarta 14:00 - 16:00', 'BL12'),"
                "('BL14', 'Quarta 16:00 - 18:00', 'BL13'),"
                "('BL15', 'Quarta 18:00 - 20:00', 'BL14'),"
                "('BL16', 'Quinta 09:00 - 11:00', ''),"
                "('BL17', 'Quinta 11:00 - 13:00', 'BL16'),"
                "('BL18', 'Quinta 14:00 - 16:00', 'BL17'),"
                "('BL19', 'Quinta 16:00 - 18:00', 'BL18'),"
                "('BL20', 'Quinta 18:00 - 20:00', 'BL19'),"
                "('BL21', 'Sexta 09:00 - 11:00', ''),"
                "('BL22', 'Sexta 11:00 - 13:00', 'BL21'),"
                "('BL23', 'Sexta 14:00 - 16:00', 'BL22'),"
                "('BL24', 'Sexta 16:00 - 18:00', 'BL23'),"
                "('BL25', 'Sexta 18:00 - 20:00', 'BL24')"
                )     
 
 #Criação da tabela cursos
cursor.execute("""create table course(id text, name text, abrev text)""")
cursor.execute("insert into course values "
                "('200', 'Engenharia Informatica Médica', 'EIM_1'),"
                "('201', 'Engenharia Informatica Médica', 'EIM_1'),"
                "('202', 'Engenharia Informatica Médica', 'EIM_1'),"
                "('203', 'Engenharia de Sistemas Informáticos', 'ESI_1'),"
                "('204', 'Engenharia de Sistemas Informáticos', 'ESI_2'),"
                "('205', 'Engenharia de Sistemas Informáticos', 'ESI_3'),"
                "('206', 'Engenharia Eletrotécnica e de Computadores', 'EEC_1'),"
                "('207', 'Engenharia Eletrotécnica e de Computadores', 'EEC_2'),"
                "('208', 'Engenharia Eletrotécnica e de Computadores', 'EEC_3'),"
                "('209', 'Engenharia e Gestão Industrial', 'EGI_1'),"
                "('210', 'Engenharia e Gestão Industrial', 'EGI_2'),"
                "('211', 'Engenharia e Gestão Industrial', 'EGI_3')"
                )

cursor.execute("""create table teacher_restrictionTimes(id_teacher text, block_id text)""")
cursor.execute("insert into teacher_restrictionTimes values "
                "('301', 'BL09'),"
                "('301', 'BL10'),"
                "('301', 'BL11'),"
                "('302', 'BL12'),"
                "('302', 'BL13'),"
                "('303', 'BL05'),"
                "('303', 'BL06'),"
                "('307', 'BL20'),"
                "('308', 'BL04'),"
                "('308', 'BL05'),"
                "('311', 'BL16'),"
                "('311', 'BL17'),"
                "('311', 'BL18'),"
                "('311', 'BL19'),"
                "('311', 'BL20'),"
                "('311', 'BL21'),"
                "('311', 'BL22'),"
                "('311', 'BL23'),"
                "('311', 'BL24'),"
                "('311', 'BL25'),"
                "('314', 'BL23'),"
                "('314', 'BL24'),"
                "('314', 'BL25'),"
                "('315', 'BL18'),"
                "('315', 'BL19'),"
                "('315', 'BL20'),"
                "('317', 'BL13'),"
                "('317', 'BL14'),"
                "('317', 'BL15'),"
                "('321', 'BL15'),"
                "('321', 'BL20'),"
                "('321', 'BL25'),"
                "('324', 'BL25'),"
                "('327', 'BL23'),"
                "('327', 'BL24'),"
                "('327', 'BL25'),"
                "('328', 'BL06'),"
                "('328', 'BL11'),"
                "('328', 'BL16'),"
                "('328', 'BL17'),"
                "('331', 'BL11'),"
                "('331', 'BL12'),"
                "('332', 'BL06'),"
                "('332', 'BL07'),"
                "('332', 'BL25'),"
                "('333', 'BL09'),"
                "('333', 'BL19'),"
                "('333', 'BL20'),"
                "('334', 'BL03'),"
                "('334', 'BL04'),"
                "('334', 'BL10')"

                )

connector.commit()
cursor.close()
connector.close()               
          