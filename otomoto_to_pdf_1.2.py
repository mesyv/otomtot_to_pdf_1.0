from typing_extensions import IntVar
from googletrans import Translator
#import translators as ts
import requests
from bs4 import BeautifulSoup
import os
import cv2
import re
from fpdf import FPDF   
import tkinter as tk
from tkinter import *
from tkinter import Checkbutton, filedialog, messagebox
from typing import Text

choose_dir = "C:/auta"
default_dir = os.getcwd()
print("Lokalizacja pliku .exe: " + os.getcwd())
ts = Translator()

#tworzenie folderu /auta jesli nie ma
try:
    os.mkdir("C:/auta")
except:
    pass

def get_eur():
    eur_web = "https://www.bankier.pl/waluty/kursy-walut/nbp/eur"

    response = requests.get(eur_web)
    eur_soup = BeautifulSoup(response.text, 'lxml')

    eur_str = eur_soup.find('div', class_='profilLast').text.strip()

    eur_str = eur_str[0:4]
    eur_str = eur_str.replace(",", ".")
    get_eur.eur_rate = float(eur_str)
    print(f"Dzisiejszy kurs euro to: {get_eur.eur_rate} PLN")

def dir_change():
    dir_change.choose_dir = filedialog.askdirectory(initialdir="/", title="Wybierz folder")
    dir_lbl.config(text=dir_change.choose_dir)
    dir_lbl.pack()
    print("Zmieniono folder docelowy na: " + dir_change.choose_dir)

def create_pdf():
    manual_price = chb_price.get()
    print(f"Cena wprowadzona manualnie: {manual_price}")
    skip_photo_numbers = skip_photo.get()
    skip_photo_numbers = re.findall(r'\d+', skip_photo_numbers)
    skip_photo_numbers = list(map(int, skip_photo_numbers))
    print(f"Pomijam zdjecia numer: {skip_photo_numbers}")

    url = ofert_ent.get()
    print(url)
    if not url:
        messagebox.showinfo("Informacja", "Wprowadź url!")
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        default_path = os.getcwd()

        #-----SZCZEGOLY-----
        try:
            price = soup.find('div', class_='offer-price')
            car_price_pln = price['data-price']
            car_price_pln = car_price_pln.replace(" ", "")
            car_price_pln = int(car_price_pln)
        except:
            car_price_pln = "N/a"
        try:
            brand = soup.find(text='Marka pojazdu').findNext(Text).text.strip()
        except:
            brand = "N/a"
            pass
        try:
            model = soup.find(text='Model pojazdu').findNext(Text).text.strip()
        except:
            model = "N/a"
            pass
        try:
            version = soup.find(text='Wersja').findNext(Text).text.strip()
        except:
            version = "N/a"
            pass
        try:
            generation = soup.find(text='Generacja').findNext(Text).text.strip()
        except:
            generation = "N/a"
            pass
        try:
            year = soup.find(text='Rok produkcji').findNext(Text).text.strip()
        except:
            year = "N/a"
            pass
        try:
            mileage = soup.find(text='Przebieg').findNext(Text).text.strip()
        except:
            mileage = "N/a"
            pass
        try:
            engine = soup.find(text='Pojemność skokowa').findNext(Text).text.strip()
        except:
            engine = "N/a"
            pass
        try:
            fuel = soup.find(text='Rodzaj paliwa').findNext(Text).text.strip()
        except:
            fuel = "N/a"
            pass
        try:
            power = soup.find(text='Moc').findNext(Text).text.strip()
        except:
            power = "N/a"
            pass
        try:
            transmission = soup.find(text='Skrzynia biegów').findNext(Text).text.strip()
        except:
            transmission = "N/a"
            pass
        try:
            drive = soup.find(text='Napęd').findNext(Text).text.strip()
        except:
            drive = "N/a"
            pass

        print("Pobieranie danych: ")
        print(car_price_pln, brand, model, version, generation, year, mileage, engine, fuel, power, transmission, drive)

        # try:
        #     doors = soup.find(text='Liczba drzwi').findNext(Text).text.strip()
        #     seats = soup.find(text='Liczba miejsc').findNext(Text).text.strip()
        #     color = soup.find(text='Kolor').findNext(Text).text.strip()
        #     country = soup.find(text='Kraj pochodzenia').findNext(Text).text.strip()
        #     first_registration = soup.find(text='Pierwsza rejestracja').findNext(Text).text.strip()
        #     polish_registration = soup.find(text='Zarejestrowany w Polsce').findNext(Text).text.strip()
        #     condition = soup.find(text='Stan').findNext(Text).text.strip()
        # except:
        #     pass

        details_dict = {
            "Marka: ": brand,
            "Model: ": model,
            "Wersja: ": version,
            "Generacja: ": generation,
            "Rok: ": year,
            "Przebieg: ": mileage,
            "Silnik: ": engine,
            "Rodzaj paliwa: ": fuel,
            "Moc: ": power,
            "Skrzynia: ": transmission,
            "Napęd: ": drive,
        }
        #details_dict = ts.translate(details_dict, dest="en").text

        #-----WYPOSAZENIE-----
        equipment = [s.get_text(separator="\n", strip=True) for s in soup.find_all('ul', class_='offer-features__list')]
        equipment[0] = ts.translate(equipment[0], src="pl", dest="fr")
        equipment[1] = ts.translate(equipment[1], src="pl", dest="fr")
        equipment[2] = ts.translate(equipment[2], src="pl", dest="fr")
        print(equipment[0])

        #-----POBRANIE-ZDJECIA---------------
        photos = soup.find_all('img', class_="bigImage")
        i = 1
        j = 1
        print(os.getcwd())

        last_chars = url[-13:]
        last_chars = last_chars[:-5]
        try:
            os.mkdir(dir_change.choose_dir + "//" + brand +  "_" + model +  "_" + year + "_" + last_chars)
        except:
            pass

        try:
            os.mkdir(choose_dir + "//" + brand +  "_" + model +  "_" + year + "_" + last_chars)
        except:
            pass

        try:
            os.chdir(dir_change.choose_dir + "//" + brand +  "_" + model +  "_" + year + "_" + last_chars)
        except:
            os.chdir(choose_dir + "//" + brand +  "_" + model +  "_" + year + "_" + last_chars)
        
        print(os.getcwd())

        for photo in photos:
            photo_link = photo['data-lazy']
            photo_name = f"{brand}{model}{year}-{i}"
            with open(photo_name +'.jpg', 'wb') as f:
                im = requests.get(photo_link)
                f.write(im.content)
                print(f"Zapisuje zdjecie nr: {i}")
            i += 1

        #-----PRZYCINANIE-ZDJEC--------------------------------------------------
        while j < i:
            photo_name = f"{brand}{model}{year}-{j}.jpg"
            path = os.getcwd() + "\\" + photo_name
            img = cv2.imread(path)
            height, width, channels = img.shape
            img_cropped = img[0:height-35,0:width]
            cv2.imwrite(photo_name, img_cropped)
            print(f"Przycinam zdjecie: {photo_name}")
            j += 1

        #-----PDF------------------------------------------------------------------------------------
        pdf = FPDF("P", "mm", "Letter")
        margins = 10
        WIDTH = pdf.w - 2*margins
        HEIGHT = pdf.h
        bord = False
        k = 1
        l = 1
        pdf.set_auto_page_break(auto=True, margin=0)
        pdf.set_margins(margins, margins, margins)
        pdf.add_page()
        pdf.add_font("Calibri", "", r"C:\Windows\Fonts\calibri.ttf", uni=True)
        pdf.add_font("Calibri", "B", r"C:\Windows\Fonts\calibrib.ttf", uni=True)
        pdf.add_font("Impact", "", r"C:\Windows\Fonts\impact.ttf", uni=True)

        #--tytul-i-logo
        pdf.set_font("calibri", "", 8.5)
        pdf.set_margins(0, 0, 0)
        pdf.cell(0, 4, " " , border=bord, align = "R", ln=True)
        pdf.cell(0, 6, "+48 784775541     " , border=bord, align = "R", ln=True)
        pdf.cell(0, 5, "daniel.wegrzyn@magnal-logistics.com     " , border=bord, align = "R", ln=True)

        pdf.set_font("Impact", "", 30)
        try:
            pdf.image(default_dir + "\\logo_magnal.jpg", 5, 5, 50)
        except:
            print("Nie dodano loga. Brak pliku logo_magnal.jpg w lokacji: " + default_dir)
            pass
        pdf.set_margins(margins, margins, margins)
        pdf.cell(0, 25, f"{brand} {model}", ln=True, border=bord, align="C")

        #--szczegoly--
        pdf.set_font("calibri", "", 11)
        for a, b in details_dict.items():
            if b != "N/a":
                if l == 4 or l == 8 or l == 12 or l == 16 or l == 20 or l == 24 or l ==28:
                    pdf.cell(WIDTH/4, 6, ts.translate(a, dest="fr").text + " " + ts.translate(b, dest="fr").text, border=bord, align="C", ln=True)
                else:
                    pdf.cell(WIDTH/4, 6, ts.translate(a, dest="fr").text + " " + ts.translate(b, dest="fr").text, border=bord, align="C")
                l += 1
            else:
                pass
        pdf.cell(10, 10, " ", border=bord, ln=True)

        #--cena--
        if manual_price == 1:
            car_price_final = manual_price_value.get()
        elif manual_price == 0:
            car_price_eur = int(car_price_pln / get_eur.eur_rate)
            car_price_final = int(car_price_eur * 0.885)
            print(f"Cena auta w PLN: {car_price_pln}")
            print(f"Cena auta w EUR: {car_price_eur}")
            print(f"Cena finalna: {car_price_final} EUR")
        
        pdf.set_font("calibri", "", 15)
        pdf.cell(WIDTH, 6, f"le prix: {car_price_final} EUR", border=bord, align="C", ln=True)

        #--wyposazenie--

        if not equipment:
            print("Brak wyposazenia na aukcji Otomoto")
        else:
            pdf.set_font("calibri", "B", 17)
            pdf.set_margins(0, 0, 0)
            pdf.set_fill_color(50, 93, 168)
            pdf.cell(0, 2.5, " ", border=bord, ln=True)
            pdf.cell(0, 10, "         ÉQUIPEMENT" , border=bord, align = "L", fill = True, ln=True)
            pdf.cell(0, 4, " ", border=bord, ln=True)
            pdf.set_margins(margins, margins, margins)

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.set_font("calibri", "", 11)
            pdf.multi_cell(WIDTH/3, 4.5, equipment[0].text, border=bord, align="C")
            pdf.set_y(y) #wysokosc
            pdf.set_x(x + WIDTH/3)
            pdf.multi_cell(WIDTH/3, 5, equipment[1].text, border=bord, align="C")
            pdf.set_y(y)
            pdf.set_x(x + 2*(WIDTH/3))
            pdf.multi_cell(WIDTH/3, 5, equipment[2].text, border=bord, align="C", ln=True)
            pdf.cell(WIDTH, 4, " ", border=bord, ln=True)


        #--zdjecia--
        pdf.set_font("calibri", "B", 17)
        pdf.set_margins(0, 0, 0)
        pdf.set_fill_color(50, 93, 168)
        pdf.cell(0, 2.5, " ", border=bord, ln=True)
        pdf.cell(0, 10, "         DES PHOTOS" , border=bord, align = "L", fill = True, ln=True)
        pdf.cell(0, 2.5, " ", border=bord, ln=True)
        pdf.set_margins(margins, margins, margins)

        while k < j:
            if k in skip_photo_numbers:
                print(f"Pomijam zdjęcie nr: {k}")
            else:
                img_size = 180
                pdf.image(f"{brand}{model}{year}-{k}.jpg", (WIDTH/2)-(img_size/2-10), None, img_size)
                pdf.cell(WIDTH, 4, " ", border=bord, ln=True)
            k += 1

        #--kontakt--
        pdf.set_font("calibri", "B", 17)
        pdf.set_margins(0, 0, 0)
        pdf.set_fill_color(50, 93, 168)
        pdf.cell(0, 2.5, " ", border=bord, ln=True)
        pdf.cell(0, 10, "         CONTACT" , border=bord, align = "L", fill = True, ln=True)
        pdf.cell(0, 2.5, " ", border=bord, ln=True)
        pdf.set_margins(margins, margins, margins)

        pdf.set_font("calibri", "", 15)
        pdf.cell(WIDTH, 6, "Nous contacter:", border=bord, align="C", ln=True)
        pdf.set_font("calibri", "", 14)
        pdf.cell(WIDTH, 6, "+48 784 775 541", border=bord, align="C", ln=True)
        pdf.cell(WIDTH, 6, "daniel.wegrzyn@magnal-logistics.com", border=bord, align="C", ln=True)

        pdf.output(os.getcwd() + "\\" + f"{brand}{model}_{year}_{last_chars}.pdf")
        print("PDF zapisany pomyślnie: " + os.getcwd() + "\\" + f"{brand}{model}_{year}_{last_chars}.pdf")

get_eur()


root = tk.Tk()
root.title("Otomoto to PDF Converter")

canvas = tk.Canvas(root, height=500, width=800, bg="#263D42")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.1)

#--BUTTONS--
dir_btn = tk.Button(root, text="Zmień folder docelowy", padx=20, pady=5, fg="white", bg="#263D42", command=dir_change)
dir_btn.pack()
create_btn = tk.Button(root, text="Twórz PDFa", padx=20, pady=5, fg="white", bg="#263D42", command=create_pdf)
create_btn.pack()

#--LABELS---
lbl1 = tk.Label(frame, text=f"Folder docelowy PDFa:", bg="white")
lbl1.pack()
dir_lbl = tk.Label(frame, text=choose_dir, bg="#c6cacf")
dir_lbl.pack()
lbl_empty = tk.Label(frame, text=f" ", bg="white")
lbl_empty.pack()

lbl2 = tk.Label(frame, text=f"Link oferty:", bg="white")
lbl2.pack()
ofert_ent = tk.Entry(frame, width=100, bg="#c6cacf")
ofert_ent.pack()
lbl_empty2 = tk.Label(frame, text=f" ", bg="white")
lbl_empty2.pack()

#checkbox
chb_price = IntVar()
first_chb = Checkbutton(frame, text="Wprowadź cenę ręcznie (zaznacz jeśli tak)", variable=chb_price, onvalue=1, offvalue=0)
first_chb.pack()
lbl3 = tk.Label(frame, text=f"Cena auta w EURO:", bg="white")
lbl3.pack()
manual_price_value = tk.Entry(frame, width=100, bg="#c6cacf")
manual_price_value.pack()
lbl_empty3 = tk.Label(frame, text=f" ", bg="white")
lbl_empty3.pack()

lbl3 = tk.Label(frame, text=f"Pomiń zdjęcia: (np. 1, 4, 12)", bg="white")
lbl3.pack()
skip_photo = tk.Entry(frame, width=100, bg="#c6cacf")
skip_photo.pack()

root.mainloop()