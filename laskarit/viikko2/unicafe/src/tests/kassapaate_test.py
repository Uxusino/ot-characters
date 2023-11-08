import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassa = Kassapaate()
        self.kortti = Maksukortti(1000)
        self.broke = Maksukortti (200)

    def test_setup_oikein(self):
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.maukkaat, 0)

    def test_syo_edullisesti_kateisella_jos_riittaa(self):
        vaihtoraha = self.kassa.syo_edullisesti_kateisella(300)

        self.assertEqual(self.kassa.kassassa_rahaa, 100240)
        self.assertEqual(vaihtoraha, 60)
        self.assertEqual(self.kassa.edulliset, 1)
    
    def test_syo_edullisesti_kateisella_jos_ei_riita(self):
        vaihtoraha = self.kassa.syo_edullisesti_kateisella(200)

        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassa.edulliset, 0)

    def test_syo_maukkaasti_kateisella_jos_riittaa(self):
        vaihtoraha = self.kassa.syo_maukkaasti_kateisella(500)

        self.assertEqual(self.kassa.kassassa_rahaa, 100400)
        self.assertEqual(vaihtoraha, 100)
        self.assertEqual(self.kassa.maukkaat, 1)

    def test_syo_maukkaasti_kateisella_jos_ei_riita(self):
        vaihtoraha = self.kassa.syo_maukkaasti_kateisella(200)

        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassa.maukkaat, 0)

    def test_kortilla_tarpeeksi_rahaa_edullinen(self):
        vastaus = self.kassa.syo_edullisesti_kortilla(self.kortti)

        self.assertEqual(self.kortti.saldo, 760)
        self.assertEqual(vastaus, True)
        self.assertEqual(self.kassa.edulliset, 1)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_kortilla_tarpeeksi_rahaa_maukas(self):
        vastaus = self.kassa.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kortti.saldo, 600)
        self.assertEqual(vastaus, True)
        self.assertEqual(self.kassa.maukkaat, 1)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_kortilla_ei_riita_edullinen(self):
        vastaus = self.kassa.syo_edullisesti_kortilla(self.broke)

        self.assertEqual(self.broke.saldo, 200)
        self.assertEqual(vastaus, False)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_kortilla_ei_riita_maukas(self):
        vastaus = self.kassa.syo_maukkaasti_kortilla(self.broke)

        self.assertEqual(self.broke.saldo, 200)
        self.assertEqual(vastaus, False)
        self.assertEqual(self.kassa.maukkaat, 0)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_lataa_rahaa(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, 1000)
        
        self.assertEqual(self.kortti.saldo, 2000)
        self.assertEqual(self.kassa.kassassa_rahaa, 101000)

    def test_ei_ladata_negatiivinen(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, -1000)

        self.assertEqual(self.kortti.saldo, 1000)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_kassassa_rahaa_euroina(self):
        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000.0)