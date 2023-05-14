# nacteni karet
import pygame
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

CER_SEDMA = pygame.image.load(dir_path + "/assets/cer_sedma.png")
CER_OSMA = pygame.image.load(dir_path + "/assets/cer_osma.png")
CER_DEVITKA = pygame.image.load(dir_path + "/assets/cer_devitka.png")
CER_DESITKA = pygame.image.load(dir_path + "/assets/cer_desitka.png")
CER_SPODEK = pygame.image.load(dir_path + "/assets/cer_spodek.png")
CER_SVRSEK = pygame.image.load(dir_path + "/assets/cer_svrsek.png")
CER_KRAL = pygame.image.load(dir_path + "/assets/cer_kral.png")
CER_ESO = pygame.image.load(dir_path + "/assets/cer_eso.png")

ZAL_SEDMA = pygame.image.load(dir_path + "/assets/zal_sedma.png")
ZAL_OSMA = pygame.image.load(dir_path + "/assets/zal_osma.png")
ZAL_DEVITKA = pygame.image.load(dir_path + "/assets/zal_devitka.png")
ZAL_DESITKA = pygame.image.load(dir_path + "/assets/zal_desitka.png")
ZAL_SPODEK = pygame.image.load(dir_path + "/assets/zal_spodek.png")
ZAL_SVRSEK = pygame.image.load(dir_path + "/assets/zal_svrsek.png")
ZAL_KRAL = pygame.image.load(dir_path + "/assets/zal_kral.png")
ZAL_ESO = pygame.image.load(dir_path + "/assets/zal_eso.png")

LIS_SEDMA = pygame.image.load(dir_path + "/assets/lis_sedma.png")
LIS_OSMA = pygame.image.load(dir_path + "/assets/lis_osma.png")
LIS_DEVITKA = pygame.image.load(dir_path + "/assets/lis_devitka.png")
LIS_DESITKA = pygame.image.load(dir_path + "/assets/lis_desitka.png")
LIS_SPODEK = pygame.image.load(dir_path + "/assets/lis_spodek.png")
LIS_SVRSEK = pygame.image.load(dir_path + "/assets/lis_svrsek.png")
LIS_KRAL = pygame.image.load(dir_path + "/assets/lis_kral.png")
LIS_ESO = pygame.image.load(dir_path + "/assets/lis_eso.png")

KUL_SEDMA = pygame.image.load(dir_path + "/assets/kul_sedma.png")
KUL_OSMA = pygame.image.load(dir_path + "/assets/kul_osma.png")
KUL_DEVITKA = pygame.image.load(dir_path + "/assets/kul_devitka.png")
KUL_DESITKA = pygame.image.load(dir_path + "/assets/kul_desitka.png")
KUL_SPODEK = pygame.image.load(dir_path + "/assets/kul_spodek.png")
KUL_SVRSEK = pygame.image.load(dir_path + "/assets/kul_svrsek.png")
KUL_KRAL = pygame.image.load(dir_path + "/assets/kul_kral.png")
KUL_ESO = pygame.image.load(dir_path + "/assets/kul_eso.png")


# Game card class
class Card:
    def __init__(self, color: str, value: str):
        self.color = color
        self.value = value
        self.picture = None
        self.points = 0

        if value == 'desitka' or value == 'eso':
            self.points = 10

        # adds picture to a card
        if color == 'cer' and value == 'sedma':
            self.picture = CER_SEDMA
        if color == 'cer' and value == 'osma':
            self.picture = CER_OSMA
        if color == 'cer' and value == 'devitka':
            self.picture = CER_DEVITKA
        if color == 'cer' and value == 'desitka':
            self.picture = CER_DESITKA
        if color == 'cer' and value == 'spodek':
            self.picture = CER_SPODEK
        if color == 'cer' and value == 'svrsek':
            self.picture = CER_SVRSEK
        if color == 'cer' and value == 'kral':
            self.picture = CER_KRAL
        if color == 'cer' and value == 'eso':
            self.picture = CER_ESO

        if color == 'zal' and value == 'sedma':
            self.picture = ZAL_SEDMA
        if color == 'zal' and value == 'osma':
            self.picture = ZAL_OSMA
        if color == 'zal' and value == 'devitka':
            self.picture = ZAL_DEVITKA
        if color == 'zal' and value == 'desitka':
            self.picture = ZAL_DESITKA
        if color == 'zal' and value == 'spodek':
            self.picture = ZAL_SPODEK
        if color == 'zal' and value == 'svrsek':
            self.picture = ZAL_SVRSEK
        if color == 'zal' and value == 'kral':
            self.picture = ZAL_KRAL
        if color == 'zal' and value == 'eso':
            self.picture = ZAL_ESO

        if color == 'lis' and value == 'sedma':
            self.picture = LIS_SEDMA
        if color == 'lis' and value == 'osma':
            self.picture = LIS_OSMA
        if color == 'lis' and value == 'devitka':
            self.picture = LIS_DEVITKA
        if color == 'lis' and value == 'desitka':
            self.picture = LIS_DESITKA
        if color == 'lis' and value == 'spodek':
            self.picture = LIS_SPODEK
        if color == 'lis' and value == 'svrsek':
            self.picture = LIS_SVRSEK
        if color == 'lis' and value == 'kral':
            self.picture = LIS_KRAL
        if color == 'lis' and value == 'eso':
            self.picture = LIS_ESO

        if color == 'kul' and value == 'sedma':
            self.picture = KUL_SEDMA
        if color == 'kul' and value == 'osma':
            self.picture = KUL_OSMA
        if color == 'kul' and value == 'devitka':
            self.picture = KUL_DEVITKA
        if color == 'kul' and value == 'desitka':
            self.picture = KUL_DESITKA
        if color == 'kul' and value == 'spodek':
            self.picture = KUL_SPODEK
        if color == 'kul' and value == 'svrsek':
            self.picture = KUL_SVRSEK
        if color == 'kul' and value == 'kral':
            self.picture = KUL_KRAL
        if color == 'kul' and value == 'eso':
            self.picture = KUL_ESO

    def __repr__(self):
        return "Card:" + self.color + ' ' + self.value

    def __str__(self):
        return self.color + ' ' + self.value
