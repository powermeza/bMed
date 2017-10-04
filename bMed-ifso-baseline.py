import csv, unicodedata

print ("")
print ("|-----------------[ bMed IFSO Baseline generator by Juan Meza ]-----------------|")
print ("|                                                                               |")

errors = 0
error_counter_bad_date = 0
lines_converted = 0
empty_dict = {}
empty_list = []

input_file_pacientes = "Pacientes.csv"
input_file_cirugias = "Cirugias.csv"
multichoiseseparator = ";"      #S
SPECVERSION = "3"               # Version 3.0 1 Feb 2017
SUBMITCODE = "ZZZ"              #SUBMITCODE-- get this code from ifso
output_file = "IFSO_" + SUBMITCODE + "_Baseline.txt"

print ("|    IFSO Version:     ", SPECVERSION )
print ("|    Submitter code:   ", SUBMITCODE )
print ("|    Multi Choise Sep: ", multichoiseseparator)
print ("|    Input File:        %s" % input_file_cirugias)
print ("|    Output File:       %s" % output_file)


IMPORTLINKID = 0                #IMPORTLINKID = Paciente #
DEMOGID = 0                     #IMPORTLINKID = Paciente #
DEMOGDATEOFBIRTH = "0001-01-01" #Fecha Nacimiento 01-06-1979

def convert_date(dob):           #Convert a date into a YYYY-MM-DD format from a MM-DD-YYYY
  date_out = "0001-01-01"
  if len(dob) == 10:
      dob_list = dob.split("-")
      date_out = dob_list[2] + "-" + dob_list[0] + "-" + dob_list[1]
#  else:
#      error_counter_bad_date = error_counter_bad_date + 1
#      print ("Bad Date: ", date_out)
  return date_out

GENDER = "U"                    #Sexo <-- M=Male, F=Female, U=Unkonw

def convert_sexo(sexo):
  GENDER ="U"
  if sexo == "Masculino":
    GENDER = "M"
  elif sexo == "Femenino":
    GENDER = "F"
  return GENDER



AGEATOPERATION = "0"                                  #Cirugias.Edad a la Fecha de Cirugia
HEIGHT = "0"                                          #Cirugias.Altura (Mts)
WEIGHTONENTRYTOTHEWEIGHTLOSSPROGRAM = "0"             #Peso al Iniciar el Protocolo (Kgs)
FUNDINGCATEGORY = "1"                                 # 1 - Publicly funded, 2 - Self-pay, 3 - Private insurer
                                                      #Tipo de Paciente, Particular, Seguridad Social, Fundacion (#accent), Aseguradora
def convert_tipodepaciente(tipodepaciente):
  FUNDINGCATEGORY = "1"
  if tipodepaciente == "Particular":
    FUNDINGCATEGORY = "2"
  elif tipodepaciente == "Seguridad Social":
    FUNDINGCATEGORY = "1"
  elif tipodepaciente == "Aseguradora":
    FUNDINGCATEGORY = "3"
  return FUNDINGCATEGORY

TYPE2DIABETES = "0"                                   # 0 - No, 1 - Yes   <--  Diabetes Tipo 2 con Medicamento, No,Si

def convert_SiNo(SiNo):
  YesNo = "0"
  Si_c = "S" + chr(237)
#  print ("Si_No: ",SiNo) #<--- Must check validation for Si with an accent
#  for c in SiNo:
#      print (ord(c))
#  print ("New Si: " + Si_c)
  elif SiNo == Si_c:    #<--- Must check validation for Si with an accent
    YesNo = "1"
  return YesNo


TYPEOFDIABETESMEDICATION = "1"                        # 1 - Oral therapy, 2 - Insulin <-- Tipo de Medicamento para Diabetes, Insulina, Oral

def convert_tipodemedicamento(Medicamento):
    TYPEOFDIABETESMEDICATION = "1"
    if Medicamento == "Oral":
        TYPEOFDIABETESMEDICATION = "1"
    elif Medicamento == "Insulina":
        TYPEOFDIABETESMEDICATION = "2"
    return TYPEOFDIABETESMEDICATION

HYPERTENSIONONMEDICATION = "0"                        # 0 - No, 1 - Yes
DEPRESSIONONMEDICATION = "0"                          # 0 - No, 1 - Yes
INCREASEDRISKOFDVTORPE = "0"                          # 0 - No, 1 - Yes
MUSCULOSKELETALPAINONMEDICATION = "0"                 # 0 - No, 1 - Yes
CONFIRMEDSLEEPAPNOEA = "0"                            # 0 - No, 1 - Yes
DYSLIPIDAEMIAONMEDICATION = "0"                       # 0 - No, 1 - Yes
GERDGORD = "0"                                        # 0 - No, 1 - Yes
DATEOFOPERATION = "2017-01-01"                      #????
HASTHEPATIENTHADAPRIORGASTRICBALLOON = "0"            # 0 - No, 1 - Yes
WEIGHTATSURGERY = "0"                                 #???
HASTHEPATIENTHADBARIATRICSURGERYINTHEPAST = "0"       # 0 - No, 1 - Yes

OPERATIVEAPPROACH = "1"                               # 1 - Laparoscopic, 2 - Lap converted to open, 3 - Endoscopic, 4 - Open

def convert_Abordaje_Quirurgico(Ab_Qui):
    Laparoscopica = "Laparosc" + chr(243) + "pica"
    Endoscopica = "Endosc" + chr(243) + "pica"
#    print ("Abordaje: ",Ab_Qui) #<--- Must check validation for accents
#    for c in Ab_Qui:
#        print (ord(c))
    OPERATIVEAPPROACH = "1"
    if Ab_Qui == "Laparoscopica":   #Option with out accents
        OPERATIVEAPPROACH = "1"
    elif Ab_Qui == Laparoscopica:   #Modified string with accents
        OPERATIVEAPPROACH = "1"
    elif Ab_Qui == "Laparoscopica Convertida":   #Option with out accents
        OPERATIVEAPPROACH = "2"
    elif Ab_Qui == (Laparoscopica + " Convertida"):   #Modified sring with accents
            OPERATIVEAPPROACH = "2"
    elif Ab_Qui == "Endoscopica":   #Modify to accept accents
        OPERATIVEAPPROACH = "3"
    elif Ab_Qui == Endoscopica:     #Modified sring with accents
        OPERATIVEAPPROACH = "3"
    elif Ab_Qui == "Abierta":
        OPERATIVEAPPROACH = "4"
#    print ("Result :", OPERATIVEAPPROACH)
    return OPERATIVEAPPROACH

TYPEOFOPERATION = "1"                                 # 1 - Gastric band, 2 - Gastric bypass, 3 - Sleeve gastrectomy, 4 - Duodenal switch, 5 - Duodenal switch with sleeve 6 - Bilio-pancreatic diversion, 9 - Other

def convert_tipodecirugia(tipodecirugia):
    TYPEOFOPERATION = "6"
    if tipodecirugia == "Banda Gastrica Ajustable":
        TYPEOFOPERATION = "1"
    elif tipodecirugia == "Bypass Gastrico":
        TYPEOFOPERATION = "2"
    elif tipodecirugia == "Gastresctomia en Manga":
        TYPEOFOPERATION = "3"
    elif tipodecirugia == "Switch Duodenal":
        TYPEOFOPERATION = "4"
    elif tipodecirugia == "Switch Duodenal con Manga":
        TYPEOFOPERATION = "5"
    elif tipodecirugia == "Derivacion Bilio-Pancreatica":
        TYPEOFOPERATION = "6"
    elif tipodecirugia == "Otra":
        TYPEOFOPERATION = "6"
    else:
        print ("|    Error bad data in field tipo de cirugia, this field is MANDATORY so it was assigned a default value = 6.")

    return TYPEOFOPERATION

TYPEOFBYPASS = "1"                                    # 1 - Roux-en-Y, 2 - Single anastomosis, 3 - Banded gastric bypass

def convert_tipodebypass(tipodebypass):
    TYPEOFBYPASS = " "
    if tipodebypass == "Y de Roux":
        TYPEOFBYPASS = "1"
    elif tipodebypass == "Una Anastomosis":
        TYPEOFBYPASS = "2"
    elif tipodebypass == "Bypass Gastrico Anillado":
        TYPEOFBYPASS = "3"
    else:
        TYPEOFBYPASS = " "   # This field is "desirable" and dependent in TYPEOFOPERATION so it can be blank
    return TYPEOFBYPASS

DETAILSOFOTHERPROCEDURE = "0"                         # 1 - Gastric plication, 2 - Single anastomosis duodeno-ileal surgery 3 - Vertical banded gastroplasty,9 - Other procedures

def convert_defdeprocedimiento(detprocedimiento):
    DETAILSOFOTHERPROCEDURE = " "
    if detprocedimiento == "Gastroplicatura":
        DETAILSOFOTHERPROCEDURE = "1"
    elif detprocedimiento == "Anastomosis Duodeno Ileal Simple":
        DETAILSOFOTHERPROCEDURE = "2"
    elif detprocedimiento == "Gastroplastia Vertical con Manga":
        DETAILSOFOTHERPROCEDURE = "3"
    elif detprocedimiento == "Otras":
        DETAILSOFOTHERPROCEDURE = "9"
    else:
        DETAILSOFOTHERPROCEDURE = " "   # This field is "desirable" and dependent in TYPEOFOPERATION (Option 6) so it can be blank
    return DETAILSOFOTHERPROCEDURE

LEAKWITHIN30DAYSOFSURGERY = "0"                       # 0 - No, 1 - Yes
BLEEDWITHIN30DAYSOFSURGERY = "0"                      # 0 - No, 1 - Yes
OBSTRUCTIONWITHIN30DAYSOFSURGERY = "0"                # 0 - No, 1 - Yes
REOPERATIONWITHIN30DAYSOFSURGERY = "0"                # 0 - No, 1 - Yes

PATIENTSTATUSATDISCHARGE = "0"                        # 0 - Alive, 1 - Deceased

def convert_estadodelpaciente(estadodelpaciente):
    PATIENTSTATUSATDISCHARGE = " "
    if estadodelpaciente == "Finado":
        PATIENTSTATUSATDISCHARGE = "1"
    elif estadodelpaciente == "Vivo":
        PATIENTSTATUSATDISCHARGE = "0"
    else:
        PATIENTSTATUSATDISCHARGE = " "   # This field is "desirable"
    return PATIENTSTATUSATDISCHARGE

DATEOFDISCHARGEORDEATH = "0001-01-01"               #???

#********* Pacientes.csv **********
#Paciente #,
#Nombre,
#Fecha Nacimiento,
#Sexo,
#CURP,
#Calle y Numero,
#Colonia,
#Ciudad,
#Estado,
#Codigo Postal,
#Telefono,
#Email,
#Add Cirugia,
#Cirugias,
#Date Created,
#Date Modified,
#Last Modified By,
#Record Owner,
#Religion,
#Codigo de Pais

#********** Cirugias.csv File Descriptions *********
#Status General,
#Paciente #,
#Nombre del Paciente,
#CURP del Paciente,
#Fecha Nacimiento,
#Medico #,
#Nombre del Medico,
#Grupo Medico,   <--- this field has an accent on Medico and it was removed so the interpreter does not trou and error
#Add Consulta,
#Agregar Documento,
#Add Evaluacion,
#Add Nota,
#Apnea Obstructiva del Sueno Confirmada,
#Aprobado para Cirugia,
#Calle y Numero,
#Abordaje Quirurgico Previo,
#Abordaje Quirurgico,
#Ciudad,
#Codigo Postal,
#Colonia,
#Comentarios Finales,
#Consentimiento Informado,
#Consultas,Coordinador,
#Cuestionario Medico Completo,
#Date Created,
#Date Modified,
#Decision del Paciente,
#Depresion con #Medicamento,
#Descripcion de la Tecnica,
#Diabetes Tipo 2 con Medicamento,
#Displidemia con Medicamento,
#Documentos,
#Dolor Osteomuscular con Medicamento,
#Email,
#Entrega del Calendario de Citas,
#Sistema de Endoscopia Utilizado,
#ERGE,
#Especialidad del Medico,
#Estado,
#Estado del Paciente al Darse de Alta,
#Estado del Paciente al Finalizar Cirugia,
#Evaluaciones,
#Evidencia Clinica de Malnutricion,
#Fecha de la Cirugia,   <--- this field has an accent on Cirugia and it was removed so the interpreter does not trou and error
#Fecha de la Consulta,
#Folleto Informacion General,
#Fuga en los Primeros 30 Dias,
#Hipertension Arterial
#Cintura al Iniciar el Protocolo (cms),
#Tipo de Cirugia,
#Telefono,
#Tipo de Paciente,
#Edad a la Fecha de Cirugia,
#Altura (Mts),
#Tipo de Medicamento para Diabetes,
#Hemoglobina Glicosilada HgbA1c,
#Insulina Serica (uUI/ml),
#Glucosa Serica (mg/dl),
#Peptido C,
#Refuerzo de Linea de Grapeo,
#Cobertura de Anastomosis,
#Duracion de Diabetes desde Diagnostico,
#Verificacion de Impermeabilidad,
#Instalacion de Drenajes,
#Anastomosis,
#Tipo de Calibracion de Manga,
#Cms (Anastomosis),
#Medida de Calibracion (Fr),
#Aviso de Privacidad #Entregado,
#Aviso de Privacidad Entregado2,
#Instalacion de Balon Previo a la Cirugia,
#Cirugia Bariatrica Previa,
#Exceso de Peso (Kgs),
#Peso Ideal (Kgs),
#Porcentaje de Grasa,
#Tipo de Bypass,
#Definicion de Procedimiento,
#Nombre de la Cirugia,
#Fecha de Alta o Fallecimiento,
#Peso Antes del Procedimiento (Kg),
#Otra Marca,Grapas,
#Add Grapa,
#Hallazgos Transoperatorios,
#Estudios y Auxiliares Transoperatorios,
#Tipo de Anestesia,
#Accidentes Transoperatorios,
#Descripcion de Accidentes,
#Incidentes #Transoperatorios,
#Descripcion de Incidentes,
#Envio de Muestras para Estudio Histopatologico,
#Descripcion de las Muestras,
#Clasificacion de Sitio Quirurgico,
#Profilaxis Antibiotico (1 Hr o Menos Previo Incision),
#Profilaxis Antitrombotica (Eparina 4 a 12 Hrs Antes Cirugia),
#Conteo de Material y Textiles,
#Estado Actual del Paciente,
#Descripcion del Plan,
#Pronostico,
#Participantes en el Procedimiento,
#Lugar del Procedimiento


from time import gmtime, strftime
print ("|    Start:            ", strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
print ("|    ------[Data integrity checks]------ ")

#input file
f_cirugias = open(input_file_cirugias)
reade = csv.DictReader(f_cirugias, delimiter=',')

#Add an integrity check to ensure the input file has all the variables needed to genereate the output

Fecha_de_Cirugia_headder = reade.fieldnames[44]
print ("|    Field Fecha de Cirugia = ", Fecha_de_Cirugia_headder)  # If this header is displaced the program will produce bad results as it is assumming the headders is in positon 44

#Output file
f = open(output_file,'w')
f.write("S SPECVERSION SUBMITCODE IMPORTLINKID DEMOGID DEMOGDATEOFBIRTH GENDER ")
f.write("AGEATOPERATION HEIGHT WEIGHTONENTRYTOTHEWEIGHTLOSSPROGRAM FUNDINGCATEGORY TYPE2DIABETES TYPEOFDIABETESMEDICATION ")
f.write("HYPERTENSIONONMEDICATION DEPRESSIONONMEDICATION INCREASEDRISKOFDVTORPE MUSCULOSKELETALPAINONMEDICATION ")
f.write("CONFIRMEDSLEEPAPNOEA DYSLIPIDAEMIAONMEDICATION GERDGORD ")
f.write("DATEOFOPERATION HASTHEPATIENTHADAPRIORGASTRICBALLOON WEIGHTATSURGERY HASTHEPATIENTHADBARIATRICSURGERYINTHEPAST ")
f.write("OPERATIVEAPPROACH ")
f.write("TYPEOFOPERATION TYPEOFBYPASS DETAILSOFOTHERPROCEDURE LEAKWITHIN30DAYSOFSURGERY BLEEDWITHIN30DAYSOFSURGERY OBSTRUCTIONWITHIN30DAYSOFSURGERY ")
f.write("REOPERATIONWITHIN30DAYSOFSURGERY PATIENTSTATUSATDISCHARGE DATEOFDISCHARGEORDEATH \n")


for line in reade:
    f.write(multichoiseseparator + " " + SPECVERSION + " " + SUBMITCODE + " " + line["Paciente #"] + " " + line["Paciente #"] + " ")
    f.write(convert_date(line["Fecha Nacimiento"]) + " ")
    f.write(convert_sexo(line["Sexo"]) + " ")
    f.write(line["Edad a la Fecha de Cirugia"] + " ")                           #AGEATOPERATION <-- Edad a la Fecha de Cirugia
    f.write(line["Altura (Mts)"] + " ")
    f.write(line["Peso al Iniciar el Protocolo (Kgs)"] + " ")                   #WEIGHTONENTRYTOTHEWEIGHTLOSSPROGRAM <-- Peso al Iniciar el Protocolo (Kgs)
    f.write(convert_tipodepaciente(line["Tipo de Paciente"]) + " ")             #FUNDINGCATEGORY <-- Tipo de Paciente
    f.write(convert_SiNo(line["Diabetes Tipo 2 con Medicamento"]) + " ")        #TYPE2DIABETES <-- Diabetes Tipo 2 con Medicamento
    f.write(convert_tipodemedicamento(line["Tipo de Medicamento para Diabetes"]) + " ")     #TYPEOFDIABETESMEDICATION <-- Tipo de Medicamento para Diabetes
    f.write(convert_SiNo(line["Hipertension Arterial con Medicamento"]) + " ")  #HYPERTENSIONONMEDICATION <-- Hipertension Arterial con Medicamento
    f.write(convert_SiNo(line["Depresion con Medicamento"])+ " ")               #DEPRESSIONONMEDICATION <-- Depresion con Medicamento
    f.write(convert_SiNo(line["Riesgo Elevado de TEP o TVP"]) + " ")            #INCREASEDRISKOFDVTORPE <-- Riesgo Elevado de TEP o TVP
    f.write(convert_SiNo(line["Dolor Osteomuscular con Medicamento"]) + " ")    #MUSCULOSKELETALPAINONMEDICATION <-- Dolor Osteomuscular con Medicamento
    f.write(convert_SiNo(line["Apnea Obstructiva del Sueno Confirmada"]) + " ") #CONFIRMEDSLEEPAPNOEA <-- Apnea Obstructiva del Sueno Confirmada
    f.write(convert_SiNo(line["Displidemia con Medicamento"]) + " ")            #DYSLIPIDAEMIAONMEDICATION <-- Displidemia con Medicamento
    f.write(convert_SiNo(line["ERGE"]) + " ")                                   #GERDGORD <-- ERGE
    f.write(convert_date(line[Fecha_de_Cirugia_headder]) + " ")                    #DATEOFOPERATION <-- Fecha de la Cirugía
    f.write(convert_SiNo(line["Instalacion de Balon Previo a la Cirugia"]) + " ")              #HASTHEPATIENTHADAPRIORGASTRICBALLOON <-- Instalacion de Balon Previo a la Cirugia
    f.write(line["Peso Antes del Procedimiento (Kg)"] + " ")                    #WEIGHTATSURGERY <-- Peso Antes del Procedimiento (Kg)
    f.write(convert_SiNo(line["Cirugia Bariatrica Previa"]) + " ")              #HASTHEPATIENTHADBARIATRICSURGERYINTHEPAST <-- Cirugia Bariatrica Previa
    f.write(convert_Abordaje_Quirurgico(line["Abordaje Quirurgico"])  + " ")    #OPERATIVEAPPROACH <-- Abordaje Quirurgico
    f.write(convert_tipodecirugia(line["Tipo de Cirugia"]) + " ")               #TYPEOFOPERATION <-- Tipo de Cirugia
    f.write(convert_tipodebypass(line["Tipo de Bypass"]) + " ")                 #TYPEOFBYPASS <-- Tipo de Bypass
    f.write(convert_defdeprocedimiento(line["Definicion de Procedimiento"]) + " ") #DETAILSOFOTHERPROCEDURE <-- Definicion de Procedimiento
    f.write(convert_SiNo(line["Fuga en los Primeros 30 Dias"]) + " ")           #LEAKWITHIN30DAYSOFSURGERY <-- Fuga en los Primeros 30 Dias
    f.write(convert_SiNo(line["Sangrado en los Primeros 30 Dias"]) + " ")       #BLEEDWITHIN30DAYSOFSURGERY < -- Sangrado en los Primeros 30 Dias
    f.write(convert_SiNo(line["Obstruccion en los Primeros 30 Dias"]) + " ")    #OBSTRUCTIONWITHIN30DAYSOFSURGERY < -- Obstruccion en los Primeros 30 Dias
    f.write(convert_SiNo(line["Re-Intervencion en los Primeros 30 Dias"]) + " ") #REOPERATIONWITHIN30DAYSOFSURGERY <-- Re-Intervencion en los Primeros 30 Dias
    f.write(convert_estadodelpaciente(line["Estado del Paciente al Darse de Alta"]) + " ") #PATIENTSTATUSATDISCHARGE <-- Estado del Paciente al Darse de Alta
    f.write(convert_date(line["Fecha de Alta o Fallecimiento"]) + " ")          #DATEOFDISCHARGEORDEATH <-- Fecha de Alta o Fallecimiento
    f.write("\n")
    lines_converted = lines_converted + 1


f.close()

from time import gmtime, strftime
print ("|    End:             ", strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
print ("|    Lines processed: ", lines_converted)
print ("|    Errors:          ", errors)
print ("|    Bad Dates:       ", error_counter_bad_date)
print ("|-------------------------------------------------------------------------------|")

