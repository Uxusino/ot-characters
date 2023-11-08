class Kassapaate:
    def __init__(self):
        self.kassassa_rahaa = 100000
        self.edulliset = 0
        self.maukkaat = 0

    def syo_edullisesti_kateisella(self, maksu):
        if maksu >= 240:
            self.lataa_rahaa_kassalle(240)
            self.lisaa_edullinen()
            return maksu - 240
        else:
            return maksu

    def syo_maukkaasti_kateisella(self, maksu):
        if maksu >= 400:
            self.lataa_rahaa_kassalle(400)
            self.lisaa_maukas()
            return maksu - 400
        else:
            return maksu

    def syo_edullisesti_kortilla(self, kortti):
        if kortti.saldo >= 240:
            kortti.ota_rahaa(240)
            self.lisaa_edullinen()
            return True
        else:
            return False

    def syo_maukkaasti_kortilla(self, kortti):
        if kortti.saldo >= 400:
            kortti.ota_rahaa(400)
            self.lisaa_maukas()
            return True
        else:
            return False

    def lataa_rahaa_kortille(self, kortti, summa):
        if summa >= 0:
            kortti.lataa_rahaa(summa)
            self.lataa_rahaa_kassalle(summa)
        else:
            return

    def kassassa_rahaa_euroina(self):
        return self.kassassa_rahaa / 100

    def lataa_rahaa_kassalle(self, summa):
        self.kassassa_rahaa += summa

    def lisaa_edullinen(self):
        self.edulliset += 1

    def lisaa_maukas(self):
        self.maukkaat += 1
