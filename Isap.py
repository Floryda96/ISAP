import requests
import pyperclip
from bs4 import BeautifulSoup
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore

id_szukane = 'view:_id1:_id2:_id59:_id61:callback1:_id84:_id777:_id779:table:rRefs:{}:_id811'
id_alternatywne = 'view:_id1:_id2:_id59:_id61:callback1:_id84:_id791:_id793:table:rRefs:{}:_id825'

class main(QDialog):
    akty = []
    slownik_tytulow = {}
    selected_text = ''

    def ladowanie_tytulow(self):
        self.slownik_tytulow = {}
        with open("ustawy.txt", "r") as plik:
            linki = plik.read().splitlines()
            for link in linki:
                if link != '':
                    soup = BeautifulSoup(requests.get(link).content, 'lxml')
                    tytul = soup.title.string
                    self.slownik_tytulow[link] = tytul
            model = QtCore.QStringListModel()
            model.setStringList([line.strip() for line in self.slownik_tytulow.values()])
            self.Listaustaw.setModel(model)

    def dodawanie_ustaw(self):
        ustawa, ok = QInputDialog.getText(self, 'Okno dodawania ustawy', 'Podaj link do ustawy')
        if ok is not None:
            try:
                with open("ustawy.txt", "a") as plik:
                    if len(self.slownik_tytulow) == 0:
                        plik.write(ustawa)
                    else:
                        plik.write('\n' + ustawa)
            except Exception as e:
                # Handle the exception if the write operation fails
                print("Error occurred while writing to the file:", str(e))
            else:
                # Execute ladowanie_tytulow() only if there was no exception
                self.ladowanie_tytulow()
        else:
            print('Ustawa niedodana')

        dodana = QMessageBox()
        dodana.setText("Ustawa dodana!")
        dodana.exec_()

    def usuwanie_ustaw(self):  # dokonczyc (bug z odswiezaniem)
        try:
            with open("ustawy.txt", "w") as plik:
                rzad_ustawy = self.daj_rzad_zaznaczonej_ustawy()
                linki = self.slownik_tytulow.keys()
                new_linki = []
                i = 0
                for link in linki:
                    if link != '' and i != rzad_ustawy:
                        new_linki.append(link)
                    i = i+1
                plik.write('\n'.join(new_linki))
        except Exception as e:
            # Handle the exception if the write operation fails
            print("Error occurred while writing to the file:", str(e))
        else:
            self.ladowanie_tytulow()
            usunieta = QMessageBox()
            usunieta.setText("Ustawa usunieta!")
            usunieta.exec_()

    def kopiowanie_dziennikow(self):  # zapytać o specyfikacje
        tekst = '\n'.join(self.akty)
        pyperclip.copy(tekst)
        skopiowana = QMessageBox()
        skopiowana.setText("Ustawa skopiowana!")
        skopiowana.exec_()

    def wyjscie(self):
        sys.exit(app.closeAllWindows)

    def daj_rzad_zaznaczonej_ustawy(self):
        selected_indexes = self.Listaustaw.selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            return selected_index.row()
        return -1

    def wyswietlanie_dziennikow(self):
        rzad_ustawy = self.daj_rzad_zaznaczonej_ustawy()
        print(rzad_ustawy)
        if rzad_ustawy != -1:
            link1 = list(self.slownik_tytulow.keys())[rzad_ustawy]
            soup1 = BeautifulSoup(requests.get(link1).content, 'lxml')
            new_akty = []

            i = 0
            found_dane_wyjsciowe = True
            while found_dane_wyjsciowe:
                dane_wejsciowe = soup1.find('a', {'id': id_szukane.format(i)})
                found_dane_wyjsciowe = dane_wejsciowe is not None
                if found_dane_wyjsciowe:
                    new_akty.append(dane_wejsciowe.text)  # Dodawanie dzienników do tablicy
                    i += 1

            i = 0
            found_dane_wyjsciowe = True
            while found_dane_wyjsciowe:
                dane_wejsciowe = soup1.find('a', {'id': id_alternatywne.format(i)})
                found_dane_wyjsciowe = dane_wejsciowe is not None
                if found_dane_wyjsciowe:
                    new_akty.append(dane_wejsciowe.text)  # Dodawanie dzienników do tablicy
                    i += 1

        self.akty = new_akty
        self.model2.setStringList(new_akty)
        return self.akty

    def __init__(self):
        super(main, self).__init__(None)
        uic.loadUi('isapui.ui', self)  # załaduj plik UI

        self.ladowanie_tytulow()

        selection_model = self.Listaustaw.selectionModel()
        selection_model.selectionChanged.connect(self.wyswietlanie_dziennikow)
        self.Dodajustawe.clicked.connect(self.dodawanie_ustaw)
        self.Usunustawe.clicked.connect(self.usuwanie_ustaw)
        self.Kopiujdziennik.clicked.connect(self.kopiowanie_dziennikow)
        self.Wyjscie.clicked.connect(self.wyjscie)

        list_view2 = self.Listadziennikow
        model2 = QtCore.QStringListModel()
        list_view2.setModel(model2)
        self.model2 = model2

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = main()
    main.show()
    sys.exit(app.exec_())
