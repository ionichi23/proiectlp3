import cv2
import numpy as np
import os

def calculeaza_scor_colorare(imagine):
    #Converteste imaginea din spatiul de culoare BGR la LAB
    img_lab = cv2.cvtColor(imagine, cv2.COLOR_BGR2LAB)
    #Extrage canalul L (luminanta)
    canal_1 = img_lab[:, :, 0]
    #Calculeaza deviatia standard a canalului L
    deviatie_std = np.std(canal_1)
    #Scorul de colorare este inversul deviatiei standard
    scor_colorare = 1.0 / (1.0 + deviatie_std)

    return scor_colorare

def afiseaza_imagine_colorata(imagine):
    cv2.imshow("Imainea cea mai colorata", imagine)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def analizeaza_culori_folder(director, prag_rezolutie):
    imagini_colorate = []
    imagini_neacceptate = []

    #Itereaza prin fisierele din director
    for fisier in os.listdir(director):
        cale_fisier = os.path.join(director, fisier)

        #Verifica daca fisierul este o imagine
        if os.path.isfile(cale_fisier) and any(extensie in fisier for extensie in ['.jpg', '.jpeg', '.png']):
            #Incarca imaginea folosind OpenCV
            img = cv2.imread(cale_fisier)

            if img is None:
                print(f'Eroare: Imaginea {fisier} nu a putut fi incarcata.')
                continue

            #Converteste imaginea din spatiul de culoare BGR la RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #Calculeaza media valorilor de culoare pe fiecare canal
            medie_culori = np.mean(img_rgb, axis=(0, 1))
            #Calculeaza scorul de colorare
            scor_colorare = calculeaza_scor_colorare(img)
            #Verifica rezolutia imaginii
            inaltime, latime, _ = img.shape

            if latime < prag_rezolutie[0] or inaltime < prag_rezolutie[1]:
                imagini_neacceptate.append((fisier, latime, inaltime, medie_culori, scor_colorare))
            else:
                imagini_colorate.append((fisier, latime, inaltime, medie_culori, scor_colorare))

    #Sorteaza imaginile colorate dupa scorul de colorare in ordine descrescatoare
    imagini_colorate.sort(key=lambda x: x[4], reverse=True)

    return imagini_colorate, imagini_neacceptate

#Exemplu de utilizare
folder = 'D:\FAC\sem 2\lp\imaginiprc'
#Pragul de rezolutie minima dorit
prag_rezolutie = (120, 124)

imagini_colorate_folder, imagini_neacceptate_folder = analizeaza_culori_folder(folder, prag_rezolutie)

if len(imagini_neacceptate_folder) > 0:
    print('Imagini care nu au atins pragul de rezolutie:')
    for imagine in imagini_neacceptate_folder:
        nume_imagine = imagine[0]
        latime = imagine[1]
        inaltime = imagine[2]
        culori_medii = imagine[3]
        scor_colorare = imagine[4]

        print(f'Imagine: {nume_imagine}')
        print(f'Rezolutie: {latime}x{inaltime}')
        print(f'Culorile medii ale imaginii {nume_imagine} sunt:', culori_medii)
        print(f'Scorul de colorare al imaginii {nume_imagine} este:', scor_colorare)
        print('______________')

if len(imagini_colorate_folder) > 0:
    print('Restul imaginilor:')
    for imagine in imagini_colorate_folder:
        nume_imagine = imagine[0]
        latime = imagine[1]
        inaltime = imagine[2]
        culori_medii = imagine[3]
        scor_colorare = imagine[4]

        print(f'Imagine: {nume_imagine}')
        print(f'Rezolutie: {latime}x{inaltime}')
        print(f'Culorile medii ale imaginii {nume_imagine} sunt:', culori_medii)
        print(f'Scorul de colorare al imaginii {nume_imagine} este:', scor_colorare)
        print('______________')

if len(imagini_colorate_folder) > 0:
    cea_mai_colorata_imagine = imagini_colorate_folder[0]
    nume_imagine = cea_mai_colorata_imagine[0]
    latime = cea_mai_colorata_imagine[1]
    inaltime = cea_mai_colorata_imagine[2]
    culori_medii = cea_mai_colorata_imagine[3]
    scor_colorare = cea_mai_colorata_imagine[4]

    print('______________')
    print(f'Imaginea cea mai colorata cu rezolutie mai mare de {prag_rezolutie[0]}x{prag_rezolutie[1]} este: {nume_imagine}')
    print(f'Rezolutie: {latime}x{inaltime}')
    print(f'Culorile medii ale imaginii {nume_imagine} sunt:', culori_medii)
    print(f'Scorul de colorare al imaginii {nume_imagine} este:', scor_colorare)
    print('______________')

    imagine_cea_mai_colorata = cv2.imread(os.path.join(folder, nume_imagine))
    afiseaza_imagine_colorata(imagine_cea_mai_colorata)

#Resurse utilizate:
#https://www.tutorialkart.com/opencv/python/opencv-python-get-image-size/
#https://pyimagesearch.com/2017/06/05/computing-image-colorfulness-with-opencv-and-python/
#https://stackoverflow.com/questions/13628491/how-to-convert-an-image-from-bgr-to-lab-with-opencv-2-4-python-2-7-and-numpy
#https://stackoverflow.com/questions/889333/how-to-check-if-a-file-is-a-valid-image-file
#http://imag.pub.ro/common/staff/cflorea/papers/SSPI_OpenCV.pdf
#https://stackoverflow.com/questions/46674833/how-to-get-a-channel-from-lab-lab-color-space-in-python
