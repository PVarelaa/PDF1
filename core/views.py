
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import PDF
import PyPDF2
import re

def import_success(request):
    return render(request, 'import_success.html')

def eliminar_cabecera(texto):

    patron_eliminar = r'Carrera\s+de\sIngeniería\s+(?:en\s+)?(?:Civil|Eléctrica|Electrónica|In[ ]?formática)\s+Facultad\s+de\s+Ciencias\s+y\s+Tecnol[ ]?ogías'

    texto_sin_cabecera = re.sub(patron_eliminar, "", texto)

    return texto_sin_cabecera


def importar_pdf(request):
    if request.method == 'POST' and request.FILES.getlist('pdf_files'):
        pdf_files = request.FILES.getlist('pdf_files')
    
        for pdf_file in pdf_files:
            with pdf_file.open(mode='rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page = pdf_reader.pages[0]
                #text = page.extract_text()
                text =""
                # Iterar sobre todas las páginas del PDF

                for no_page in range(len(pdf_reader.pages)):
                    info_page = pdf_reader._get_page(no_page)
                    texto_pagina = info_page.extract_text()
                    texto_sincab = eliminar_cabecera(texto_pagina)
                    text += texto_sincab

            #page = pdf_reader.pages[0]
            #text = page.extract_text()
            print(text)
            nombre_archivo = pdf_file.name
            materia = None
            codigo = None
            condicion = None
            carrera = None
            curso = None
            semestre = None
            requisitos = None
            cargasemanal = None
            cargasemestral = None
            
            fundamentacion_text = None
            objetivos_text = None
            contenido_text = None
            metodologia_text = None
            evaluacion_text = None
            bibliografia_text = None

            # Extraer datos del PDF
       
       
            #Estructura realizada por el "ayudante" poco conocido (ChatGPT)
            materia_match = re.search(r'Nombre\s*de\s*la\s*Materia\s*:\s*(.*)', text, re.IGNORECASE)
            #VER 281     
                     
            if not materia_match:
                materia_match = re.search(r'Nom[ ]?bre\s*de\s*la\s*Materia\s*:\s*(.*)', text,re.IGNORECASE)
            
            if materia_match:
                    materia = materia_match.group(1).strip() if materia_match else None
                    materia = re.sub(r'\.\s*$', '', materia) if materia else None
            else:
                materia=None

            codigo_match = re.search(r'Código\s*:\s*(.*)', text, re.IGNORECASE)
            codigo = codigo_match.group(1).strip().replace(" ", "") if codigo_match else None
            codigo = re.sub(r'\.\s*$', '', codigo) if codigo else None

            condicion_match = re.search(r'Condici[oóó]n\s*:\s*(.*)', text, re.IGNORECASE)
            if not condicion_match:
             condicion_match = re.search(r'Condici[oóó]?[ ]?n\s*:\s*(.*)', text, re.IGNORECASE)
            if not condicion_match:
                condicion = None
            else:
                condicion = condicion_match.group(1).strip().replace(" ", "")
                condicion = re.sub(r'\.\s*$', '', condicion) if condicion else None

            carrera_match = re.search(r'Carrera\s*:\s*(.*)', text)
            carrera = carrera_match.group(1).strip() if carrera_match else None
            carrera = re.sub(r'\.\s*$', '', carrera) if carrera else None

            curso_match = re.search(r'Curso\s*:\s*(.*)', text)
            curso = curso_match.group(1).strip().replace(" ", "") if curso_match else None
            curso = re.sub(r'\.\s*$', '', curso) if curso else None

            semestre_match = re.search(r'Semestre\s*:\s*(.*)', text)
            if not semestre_match:
                semestre_match = re.search(r'Semes[ ]?tre\s*:\s*(.*)', text, re.IGNORECASE)
       
            if semestre_match:
                semestre = semestre_match.group(1).strip().replace(" ", "")
                semestre = re.sub(r'\.\s*$', '', semestre) if semestre else None
            else:
                semestre = None

            requisitos_match = re.search(r'Requi[ ]?sitos\s*:\s*(.*)', text)
            if requisitos_match:
                requisitos = requisitos_match.group(1).strip() if requisitos_match else None
                requisitos = re.sub(r'\.\s*$', '', requisitos) if requisitos else None
            else:
                requisitos= None
            
            cargasemanal_match = re.search(r'Carga\s+horaria\s+semanal\s*:\s*(.*)', text)
            if not cargasemanal_match:
             cargasemanal_match=re.search(r'Cargar\s+horaria\s+semanal\s*:\s*(.*)',text)
            if not cargasemanal_match:
                    cargasemanal_match=re.search(r'Carga\s+horari[ ]?a\s*:\s*(.*)',text)
            if not cargasemanal_match:
                cargasemanal_match = re.search(r'Carga\s+h[ ]?oraria\s*:\s*(.*)', text)
            if not cargasemanal_match:
                cargasemanal_match=re.search(r'Carga\s+horaria\s+Semanal\s*:\s*(.*)', text)

            if cargasemanal_match:
                cargasemanal = cargasemanal_match.group(1).strip() if cargasemanal_match else None
                cargasemanal = re.sub(r'\.\s*$', '', cargasemanal) if cargasemanal else None
            else:
                    cargasemanal= None

            #Estructura original.
            cargasemestral_match = re.search(r'Carga\s+horaria\s+semestral\s*:\s*(.*)', text)
            if cargasemestral_match is not None:
                cargasemestral = cargasemestral_match.group(1).strip() if cargasemestral_match else None
                cargasemestral = re.sub(r'\.\s*$', '', cargasemestral) if cargasemestral else None
            else:  
               cargasemestral_match = re.search(r'Cargar\s+horaria\s+semestral\s*:\s*(.*)', text)
               if cargasemestral_match is not None:
                 cargasemestral = cargasemestral_match.group(1).strip() if cargasemestral_match else None
                 cargasemestral = re.sub(r'\.\s*$', '', cargasemestral) if cargasemestral else None
               else:
                  cargasemestral_match = re.search(r'Total\s*:\s*(.*)', text)
                  if cargasemestral_match is not None:
                    cargasemestral = cargasemestral_match.group(1).strip() if cargasemestral_match else None
                    cargasemestral = re.sub(r'\.\s*$', '', cargasemestral) if cargasemestral else None
                  else:
                   cargasemestral_match = re.search(r'Carga\s+h[ ]?oraria\s*:\s*(.*)', text)
                  if cargasemestral_match is not None:
                        cargasemestral = cargasemestral_match.group(1).strip() if cargasemestral_match else None
                        cargasemestral = re.sub(r'\.\s*$', '', cargasemestral) if cargasemestral else None
                  else:
                        cargasemestral_match=re.search(r'Carga\s+horaria\s+Semestral\s*:\s*(.*)', text)
                  if cargasemestral_match is not None:
                        cargasemestral = cargasemestral_match.group(1).strip() if cargasemestral_match else None
                        cargasemestral = re.sub(r'\.\s*$', '', cargasemestral) if cargasemestral else None
                  else: 
                       cargasemestral_match= re.search(r'Carga\s+horaria\s+semanal\s*:\s*(.*)', text)
                       if cargasemestral_match is not None:
                        cargasemestral = cargasemestral_match.group(1).strip() if cargasemestral_match else None
                        cargasemestral = re.sub(r'\.\s*$', '', cargasemestral) if cargasemestral else None
                       else:
                           cargasemestral= None
       
               
        
             

            ##LOS TEXTOS###

            fundamentacion_match = re.search(r'FUNDAMENTACIÓN\s*(?:\. )?(.*?)(?=III.|$)', text, re.DOTALL)
            if not fundamentacion_match:
                fundamentacion_match = re.search(r'FUNDAMEN[ ]?TACIÓN\s*(?:\. )?(.*?)(?=III.|$)', text, re.DOTALL)

            if fundamentacion_match:
                fundamentacion_text = fundamentacion_match.group(1).strip() if fundamentacion_match else None


            objetivos_match = re.search(r'OBJE[ ]?TIVOS\s*(?:\. )?(.*?)(?=IV.|$)', text, re.DOTALL)
            if not objetivos_match:
                objetivos_match = re.search(r'OBJETI[ ]?VOS\s*(?:\. )?(.*?)(?=IV.|$)', text, re.DOTALL)
            if not objetivos_match:
                objetivos_match = re.search(r'OBJETIVO[ ]?S\s*(?:\. )?(.*?)(?=IV.|$)', text, re.DOTALL)

            if objetivos_match:
                objetivos_text = objetivos_match.group(1).strip() if objetivos_match else None

        
            contenido_match = re.search(r'CONTENIDO\s*(?:\. )?(.*?)(?=V.|$)', text, re.DOTALL)
            if not contenido_match:
             contenido_match = re.search(r'CONTENIDO[ ]?S\s*(?:\. )?(.*?)(?=V.|$)', text, re.DOTALL)
            if not contenido_match:
             contenido_match = re.search(r'CONTENIDO\s+PROGRAMATICO\s*(?:\. )?(.*?)(?=V.|$)', text, re.DOTALL)

            if contenido_match:
               contenido_text = contenido_match.group(1).strip() if contenido_match else None



            metodologia_match = re.search(r'[ ]?METODOLOG[IÍÍ]A\.(.*?)(?=VI\.|$)', text, re.DOTALL)
            if metodologia_match:
                metodologia_text = metodologia_match.group(1).strip()
            else:
                metodologia_match = re.search(r'METODOLOG[ ]?[IÍÍ]A\.(.*?)(?=VI\.|$)', text, re.DOTALL)
                if metodologia_match:
                    metodologia_text = metodologia_match.group(1).strip()
                else:
                    metodologia_match = re.search(r'METODOLOG[IÍÍ][ ]?A\.(.*?)(?=VI\.|$)', text, re.DOTALL)
                    if metodologia_match:
                        metodologia_text = metodologia_match.group(1).strip() if metodologia_match else None
                    else:
                        metodologia_match = re.search(r'METODOLOGIA\.(.*?)(?=VI\.|$)', text, re.DOTALL)
                        if metodologia_match:
                            metodologia_text = metodologia_match.group(1).strip()
                        else:
                            metodologia_match = re.search(r'METODOL[ ]?OGÍA\.(.*?)(?=VI\.|$)', text, re.DOTALL)
                            if metodologia_match:
                                metodologia_text = metodologia_match.group(1).strip()
                            else:
                                metodologia_match = re.search(r'ESTRATEGIA\s*DE\s*ENSEÑANZA\s+APRENDIZAJE\s\.(.*?)(?=VII\.|$)', text, re.DOTALL)
                                if metodologia_match:
                                    metodologia_text = metodologia_match.group(1).strip() if metodologia_match else None


            
            evaluacion_match = re.search(r'EVALUACIÓ[ ]?N\s*(?:\. )?(.*?)(?=VII\.|$)', text, re.DOTALL)
            if evaluacion_match:
                evaluacion_text = evaluacion_match.group(1).strip() if evaluacion_match else None
            else: 
                evaluacion_match = re.search(r'EVALUACI[ ]?ÓN\s*(?:\. )?(.*?)(?=VII\.|$)', text, re.DOTALL)
                if evaluacion_match:
                    evaluacion_text = evaluacion_match.group(1).strip() if evaluacion_match else None
                else:
                    evaluacion_match = re.search(r'EVAL[ ]?UACIÓN\s*(?:\. )?(.*?)(?=VII\.|$)', text, re.DOTALL)
                    if evaluacion_match:
                        evaluacion_text = evaluacion_match.group(1).strip() if evaluacion_match else None
                        
            bibliografia_match = re.search(r'BIBLIOGRAF[ ]?ÍA\s*(?:\. )?(.*?)(?=VIII\.|$)', text, re.DOTALL)
            if bibliografia_match:
                 bibliografia_text = bibliografia_match.group(1).strip() if bibliografia_match else None
            else:
                bibliografia_match = re.search(r'BIBLIOGRAFIA\s*(?:\. )?(.*?)(?=VIII\.|$)', text, re.DOTALL)
                if bibliografia_match:
                    bibliografia_text = bibliografia_match.group(1).strip() if bibliografia_match else None
                

            # Guardar en la base de datos
            pdf = PDF(nombre=nombre_archivo, materia=materia, condicion=condicion,carrera=carrera, curso=curso, semestre=semestre, 
                      requisitos=requisitos,   codigo=codigo, cargasemanal=cargasemanal, cargasemestral=cargasemestral, objetivos=objetivos_text, 
                      fundamentacion=fundamentacion_text, contenido=contenido_text, metodologia=metodologia_text,evaluacion=evaluacion_text, 
                      bibliografia=bibliografia_text)
            pdf.save()

        return redirect('import_success')
    return render(request, 'import_pdf.html')

#retorna/renderiza la vista/plantilla principal 
def seleccionar(request):
    return render(request, 'seleccionar.html')

#Recupera un objeto 
def mostrarpdf(request):
    id = request.GET.get('Materia')
    pdf = PDF.objects.get(id=id)
    return render(request, 'mostrarpdf.html',{'pdf':pdf})


def get_materiasf(request, codcarrera):
    materias= list(PDF.objects.filter(codigo__icontains=codcarrera).values())
    
    #Comprueba si tiene datos
    if (len(materias)>0):
        #Devuelve un diccionario de message y la lista de materias
        data={'message': "Success", 'materias': materias}
    else:
        data={'message': "Not Found"}
    
    
    return JsonResponse(data)     


     #--------CODIGOS NO UTILIZADOS----------------------------------------

            #materia_match = re.search(r'Nombre\s*de\s*la\s*Materia\s*:\s*(.*)', text)
          #  if materia_match=='':
           #     materia_match = re.search(r'Nom[ ]?bre\s*de\s*la\s*Materia\s+*\s*(.*)', text,re.IGNORECASE)
          #  else:
           #      if materia_match=='': 
            #      materia = materia_match.group(1).strip() if materia_match else None
             #     materia = re.sub(r'\.\s*$', '', materia) if materia else None
               
               
               
            #contenido_match = re.search(r'CONTENIDO\s*(?:\. )?(.*?)(?=V.|$)', text, re.DOTALL)
            #if contenido_match:
            #    contenido_text = contenido_match.group(1).strip() if contenido_match else None
           # else:
            
                #if contenido_match:
                 #   contenido_text = contenido_match.group(1).strip() if contenido_match else None    
                #else:
                   # contenido_match = re.search(r'CONTENIDO[ ]?S\s*(?:\. )?(.*?)(?=V.|$)', text, re.DOTALL)
                  ##  if contenido_match:
                 #       contenido_text = contenido_match.group(1).strip() if contenido_match else None
                
            
            #cargasemestral_match = re.search(r'Carga\s+horaria\s+semestral\s*:\s*(.*)', text)
            #if not cargasemestral_match:
             #   cargasemestral_match = re.search(r'Cargar\s+horaria\s+semestral\s*:\s*(.*)', text)
            #if not cargasemestral_match:
             #   cargasemestral_match = re.search(r'Total\s*:\s*(.*)', text)
            #if not cargasemanal_match:
             #   cargasemestral_match = re.search(r'Carga\s+h[ ]?oraria\s*:\s*(.*)', text)
            #if not cargasemestral_match:
             #   cargasemestral_match=re.search(r'Carga\s+horaria\s+Semestral\s*:\s*(.*)', text)
            #if not cargasemestral_match:
             #   cargasemestral_match= re.search(r'Carga\s+horaria\s+semanal\s*:\s*(.*)', text)
                
            #if cargasemestral_match:
             #   cargasemestral = cargasemestral_match.group(1).strip() if cargasemestral_match else None
              #  cargasemestral = re.sub(r'\.\s*$', '', cargasemestral) if cargasemestral else None

        
