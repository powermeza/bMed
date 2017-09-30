import csv

input_file_pacientes = "Pacientes.csv"
input_file_cirugias = "Cirugias.csv"
errors = 0
empty_dict = {}
empty_list = []

multichoiseseparator = ";"      #S
SPECVERSION = "3"               # Version 3.0 1 Feb 2017
SUBMITCODE = "ZZZ"              #SUBMITCODE-- get this code from ifso

output_file = "IFSO_" + SUBMITCODE + "_Baseline.txt"

IMPORTLINKID = 0                #IMPORTLINKID = Paciente #
DEMOGID = 0                     #IMPORTLINKID = Paciente #
DEMOGDATEOFBIRTH = "2017-01-01" #Fecha Nacimiento 01-06-1979

def convert_date(dob):           #Convert a date into a YYYY-MM-DD format from a MM-DD-YYYY
  dob_list = dob.split("-")
  return dob_list[2] + "-" + dob_list[0] + "-" + dob_list[1]

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

TYPE2DIABETES = "0"                                   # 0 - No, 1 - Yes
TYPEOFDIABETESMEDICATION = "1"                        # 1 - Oral therapy, 2 - Insulin
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
TYPEOFOPERATION = "1"                                 # 1 - Gastric band, 2 - Gastric bypass, 3 - Sleeve gastrectomy, 4 - Duodenal switch, 5 - Duodenal switch with sleeve 6 - Bilio-pancreatic diversion, 9 - Other
TYPEOFBYPASS = "1"                                    # 1 - Roux-en-Y, 2 - Single anastomosis, 3 - Banded gastric bypass
DETAILSOFOTHERPROCEDURE = "0"                         # 1 - Gastric plication, 2 - Single anastomosis duodeno-ileal surgery 3 - Vertical banded gastroplasty,9 - Other procedures
LEAKWITHIN30DAYSOFSURGERY = "0"                       # 0 - No, 1 - Yes
BLEEDWITHIN30DAYSOFSURGERY = "0"                      # 0 - No, 1 - Yes
OBSTRUCTIONWITHIN30DAYSOFSURGERY = "0"                # 0 - No, 1 - Yes
REOPERATIONWITHIN30DAYSOFSURGERY = "0"                # 0 - No, 1 - Yes
PATIENTSTATUSATDISCHARGE = "0"                        # 0 - Alive, 1 - Deceased
DATEOFDISCHARGEORDEATH = "2017-01-01"               #???

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


#input file
print "Input File: %s" % input_file_cirugias
f_cirugias = open(input_file_cirugias)
reade = csv.DictReader(f_cirugias, delimiter=',')

#Add an integrity check to ensure the input file has all the variables needed to genereate the output

#Output file
print "Output File: %s" % output_file
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
    f.write(TYPE2DIABETES + " ")
    f.write(TYPEOFDIABETESMEDICATION + " ")
    f.write(HYPERTENSIONONMEDICATION + " ")
    f.write(DEPRESSIONONMEDICATION + " ")
    f.write(INCREASEDRISKOFDVTORPE + " ")
    f.write(MUSCULOSKELETALPAINONMEDICATION + " ")
    f.write(CONFIRMEDSLEEPAPNOEA + " ")
    f.write(DYSLIPIDAEMIAONMEDICATION + " ")
    f.write(GERDGORD + " ")
    f.write(DATEOFOPERATION + " ")
    f.write(HASTHEPATIENTHADAPRIORGASTRICBALLOON + " ")
    f.write(WEIGHTATSURGERY + " ")
    f.write(HASTHEPATIENTHADBARIATRICSURGERYINTHEPAST + " ")
    f.write( OPERATIVEAPPROACH + " ")
    f.write(TYPEOFOPERATION + " ")
    f.write(TYPEOFBYPASS + " ")
    f.write(DETAILSOFOTHERPROCEDURE + " ")
    f.write(LEAKWITHIN30DAYSOFSURGERY + " ")
    f.write(BLEEDWITHIN30DAYSOFSURGERY + " ")
    f.write(OBSTRUCTIONWITHIN30DAYSOFSURGERY + " ")
    f.write(REOPERATIONWITHIN30DAYSOFSURGERY + " ")
    f.write(PATIENTSTATUSATDISCHARGE + " ")
    f.write(DATEOFDISCHARGEORDEATH + " ")
    f.write("\n")


f.close()
print errors, "errors"
