import requests
import pyperclip
from bs4 import BeautifulSoup
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
slownik_tytulow = {}
def ladowanie_tytulow():
    with open("ustawy.txt", "r") as plik:
        linki = plik.read().splitlines()
    for link in linki:
        soup = BeautifulSoup(requests.get(link).content, 'lxml')
        tytul = soup.title.string
        slownik_tytulow[link] = tytul
ladowanie_tytulow()

class main(QDialog):
    akty = []
    def dodawanie_ustaw(self):  # dokonczyc
        ustawa, ok = QInputDialog.getText(self, 'Okno dodawania ustawy', 'Podaj link do ustawy')
        if ok is not None:
            with open("ustawy.txt", "a") as plik:
                plik.write(ustawa + '\n')
                ladowanie_tytulow()
                self.list_view.setModel(self.model)
        else:
            print('Ustawa niedodana')
            # linki = plik.read().splitlines()
            # for link in linki:
            #      soup = BeautifulSoup(requests.get(link).content, 'lxml')
            #      tytul = soup.title.string
            #      slownik_tytulow[link] = tytul

        dodana = QMessageBox()
        dodana.setText("Ustawa dodana!")
        dodana.exec_()

    def usuwanie_ustaw(self):  # dokonczyc
        # with open("ustawy.txt", "w") as plik:
        #     for link in self.linki:
        #         if link.strip("\n") != self.selected_text:
        #             plik.write(link)
        usunieta = QMessageBox()
        usunieta.setText("Ustawa usunieta!")
        usunieta.exec_()

    def kopiowanie_dziennikow(self):  # dokonczyc
        tekst = '\n'.join(self.akty)
        pyperclip.copy(tekst)
        skopiowana = QMessageBox()
        skopiowana.setText("Ustawa skopiowana!")
        skopiowana.exec_()
    def wyjscie(self):
        sys.exit(app.closeAllWindows)
    def wyswietlanie_dziennikow(self):
        selected_indexes = self.Listaustaw.selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            # print (selected_index)
            selected_text = selected_index.data()
            selected_row = selected_index.row()
            link1 = list(slownik_tytulow.keys())[selected_row]
            print('selected row', selected_row)
            soup1 = BeautifulSoup(requests.get(link1).content, 'lxml')
            i = 0
            new_akty = []
            while i < 100:
                id_szukane = f'view:_id1:_id2:_id59:_id61:callback1:_id84:_id777:_id779:table:rRefs:{i}:_id811'
                dane_wejsciowe = soup1.find('a', {'id': id_szukane})
                if dane_wejsciowe is not None:
                    found_dane_wejsciowe = dane_wejsciowe.text
                    new_akty.append(found_dane_wejsciowe)  # Dodawanie dzienników do tablicy
                elif():
                    while i < 100:     # do dokonczenia
                        id_alternatywne = f'view:_id1:_id2:_id59:_id61:callback1:_id84:_id791:_id793:table:rRefs:{i}:_id825'
                        dane_wejsciowe = soup1.find('a', {'id': id_alternatywne})
                        if dane_wejsciowe is not None:
                            found_dane_wejsciowe = dane_wejsciowe.text
                            new_akty.append(found_dane_wejsciowe)  # Dodawanie dzienników do tablicy
                            i +=1
                i += 1
        self.akty = new_akty
        self.model2.setStringList(new_akty)
        return self.akty
        # self.Listadziennikow.clear()
        # self.Listadziennikow.addItems(self.akty)
    def __init__(self):
        super(main, self).__init__(None)
        uic.loadUi('isapui.ui', self)  # załaduj plik UI


        list_view = self.Listaustaw
        model = QtCore.QStringListModel()
        model.setStringList([line.strip() for line in slownik_tytulow.values()])
        list_view.setModel(model)


        selection_model = list_view.selectionModel()
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
