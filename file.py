from typing import Text
import requests
from bs4 import BeautifulSoup
import os
import cv2
from fpdf import FPDF   
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

choose_dir = "C://auta"
default_dir = os.getcwd()

def dir_change():
    dir_change.choose_dir = filedialog.askdirectory(initialdir="/", title="Wybierz folder")
    dir_lbl.config(text=dir_change.choose_dir)
    dir_lbl.pack()
    print(dir_change.choose_dir)

def create_pdf():
    url = ofert_ent.get()
    print(url)
    if not url:
        messagebox.showinfo("Informacja", "Wprowadź url")
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        default_path = os.getcwd()

        #-----SZCZEGOLY-----
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

        print(brand, model, version, generation, year, mileage, engine, fuel, power, transmission, drive)

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
        #-----WYPOSAZENIE-----
        equipment = [s.get_text(separator="\n", strip=True) for s in soup.find_all('ul', class_='offer-features__list')]

        #-----POBRANIE-ZDJECIA---------------
        photos = soup.find_all('img', class_="bigImage")
        i = 1
        j = 1
        print(os.getcwd())

        try:
            os.mkdir(dir_change.choose_dir + "//" + brand + model + year)
        except:
            pass

        try:
            os.mkdir(choose_dir + "//" + brand + model + year)
        except:
            pass

        try:
            os.chdir(dir_change.choose_dir + "//" + brand + model + year)
        except:
            os.chdir(choose_dir + "//" + brand + model + year)
        
        print(os.getcwd())

        for photo in photos:
            photo_link = photo['data-lazy']
            photo_name = f"{brand}{model}{year}-{i}"
            with open(photo_name +'.jpg', 'wb') as f:
                im = requests.get(photo_link)
                f.write(im.content)
                print(f"Writing: {i} photo")
            i += 1

        #-----PRZYCINANIE-ZDJEC--------------------------------------------------
        while j < i:
            photo_name = f"{brand}{model}{year}-{j}.jpg"
            path = os.getcwd() + "\\" + photo_name
            img = cv2.imread(path)
            height, width, channels = img.shape
            img_cropped = img[0:height-35,0:width]
            cv2.imwrite(photo_name, img_cropped)
            print(f"Cropping: {photo_name}")
            j += 1

        #-----PDF------------------------------------------------------------------------------------
        pdf = FPDF("P", "mm", "Letter")
        margins = 10
        WIDTH = pdf.w - 2*margins
        HEIGHT = pdf.h
        bord = True
        k = 1
        l = 1
        pdf.set_auto_page_break(auto=True, margin=0)
        pdf.set_margins(margins, margins, margins)
        pdf.add_page()
        pdf.add_font("Calibri", "", r"C:\Windows\Fonts\calibri.ttf", uni=True)
        pdf.add_font("Calibri", "B", r"C:\Windows\Fonts\calibrib.ttf", uni=True)

        #--tytul-i-logo
        pdf.set_font("times", "B", 30)
        pdf.image(default_dir + "\\logo_magnal.jpg", 5, 5, 50)
        pdf.cell(0, 25, f"{brand} {model}", ln=True, border=bord, align="C")

        #--szczegoly--
        pdf.set_font("calibri", "", 11)
        for a, b in details_dict.items():
            if b != "N/a":
                if l == 4 or l == 8 or l == 12 or l == 16 or l == 20 or l == 24 or l ==28:
                    pdf.cell(WIDTH/4, 6, a + b, border=bord, align="C", ln=True)
                else:
                    pdf.cell(WIDTH/4, 6, a + b, border=bord, align="C")
                l += 1
            else:
                pass
        pdf.cell(10, 10, " ", border=bord, ln=True)
        #--cena--
        pdf.set_font("calibri", "", 15)
        pdf.cell(WIDTH, 6, "Cena: 999 999 PLN", border=bord, align="C", ln=True)

        #--wyposazenie--

        if not equipment:
            print("Brak wyposazenia")
        else:
            pdf.set_font("calibri", "B", 17)
            pdf.set_margins(0, 0, 0)
            pdf.set_fill_color(50, 93, 168)
            pdf.cell(0, 2.5, " ", border=bord, ln=True)
            pdf.cell(0, 10, "         WYPOSAŻENIE" , border=bord, align = "L", fill = True, ln=True)
            pdf.cell(0, 4, " ", border=bord, ln=True)
            pdf.set_margins(margins, margins, margins)

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.set_font("calibri", "", 11)
            pdf.multi_cell(WIDTH/3, 4.5, equipment[0], border=bord, align="C")
            pdf.set_y(y) #wysokosc
            pdf.set_x(x + WIDTH/3)
            pdf.multi_cell(WIDTH/3, 5, equipment[1], border=bord, align="C")
            pdf.set_y(y)
            pdf.set_x(x + 2*(WIDTH/3))
            pdf.multi_cell(WIDTH/3, 5, equipment[2], border=bord, align="C", ln=True)
            pdf.cell(WIDTH, 4, " ", border=bord, ln=True)


        #--zdjecia--
        pdf.set_font("calibri", "B", 17)
        pdf.set_margins(0, 0, 0)
        pdf.set_fill_color(50, 93, 168)
        pdf.cell(0, 2.5, " ", border=bord, ln=True)
        pdf.cell(0, 10, "         ZDJĘCIA" , border=bord, align = "L", fill = True, ln=True)
        pdf.cell(0, 2.5, " ", border=bord, ln=True)
        pdf.set_margins(margins, margins, margins)

        while k < j:
            img_size = 180
            pdf.image(f"{brand}{model}{year}-{k}.jpg", (WIDTH/2)-(img_size/2-10), None, img_size)
            pdf.cell(WIDTH, 4, " ", border=bord, ln=True)
            k += 1

        #--kontakt--
        pdf.set_font("calibri", "B", 17)
        pdf.set_margins(0, 0, 0)
        pdf.set_fill_color(50, 93, 168)
        pdf.cell(0, 2.5, " ", border=bord, ln=True)
        pdf.cell(0, 10, "         KONTAKT" , border=bord, align = "L", fill = True, ln=True)
        pdf.cell(0, 2.5, " ", border=bord, ln=True)
        pdf.set_margins(margins, margins, margins)

        pdf.set_font("calibri", "", 15)
        pdf.cell(WIDTH, 6, "Skontaktuj się z nami:", border=bord, align="C", ln=True)
        pdf.set_font("calibri", "", 14)
        pdf.cell(WIDTH, 6, "+48 784 775 541", border=bord, align="C", ln=True)
        pdf.cell(WIDTH, 6, "daniel.wegrzyn@magnal-logistics.com", border=bord, align="C", ln=True)

        pdf.output(os.getcwd() + "\\" + f"{brand}{model}_{year}.pdf")


root = tk.Tk()

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

lbl2 = tk.Label(frame, text=f"Link oferty:", bg="white")
lbl2.pack()
ofert_ent = tk.Entry(frame, width=100, bg="#c6cacf")
#ofert_ent.insert(0, "Link")
ofert_ent.pack()

root.mainloop()
