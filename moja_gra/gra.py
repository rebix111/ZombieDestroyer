import pygame
import os
import random
import math
import json
import webbrowser

pygame.init()

wysokosc_okna, szerokosc_okna = 750, 750
mapa = pygame.image.load('moja_gra\\mapa.png')
mapa = pygame.transform.scale(mapa, (wysokosc_okna, szerokosc_okna))
okno = pygame.display.set_mode((wysokosc_okna, szerokosc_okna))

szerokosc_gracza, wysokosc_gracza = 90, 90  
MONETA_CZAS_ZYCIA = 5000
KOLOR_TEKSTU = (50, 50, 50)
KOLOR_TLA = (0, 0, 0)
KATALOG_ZAPISOW = "zapisy"
MAX_ZAPISOW = 5

url = "https://www.tiktok.com/@handball._enjoyer"
url_insta = 'https://www.instagram.com/pagurski_jakis.nn/'

poruszanie_do_prawej = [pygame.image.load(f"moja_gra\\postac_od_prawej\\ludzik_prawa_{i}.png") for i in range(1, 7)]
poruszanie_do_lewej = [pygame.image.load(f"moja_gra\\postac_od_lewej\\ludzik_lewa_{i}.png") for i in range(1, 7)]
poruszanie_do_dolu = [pygame.image.load(f"moja_gra\\postac_od_przodu\\ludzik_przod_{i}.png") for i in range(1, 7)]
poruszanie_do_pszodu = [pygame.image.load(f"moja_gra\\postac_od_tylu\\ludzik_tylem_{i}.png") for i in range(1, 7)]

poruszanie_do_pszodu_zombie = [pygame.image.load(f"moja_gra\\zombie_od_przodu\\zombie_przod_{i}.png") for i in range(1, 7)]

poruszanie_do_prawej = [pygame.transform.scale(img, (wysokosc_gracza, szerokosc_gracza)) for img in poruszanie_do_prawej]
poruszanie_do_lewej = [pygame.transform.scale(img, (wysokosc_gracza, szerokosc_gracza)) for img in poruszanie_do_lewej]
poruszanie_do_dolu = [pygame.transform.scale(img, (20 + wysokosc_gracza, 20 + szerokosc_gracza)) for img in poruszanie_do_dolu]
poruszanie_do_pszodu = [pygame.transform.scale(img, (20 + wysokosc_gracza, 20 + szerokosc_gracza)) for img in poruszanie_do_pszodu]
poruszanie_do_pszodu_zombie = [pygame.transform.scale(img, (wysokosc_gracza, szerokosc_gracza)) for img in poruszanie_do_pszodu_zombie]

noz_tekstura = pygame.transform.rotate(pygame.image.load('moja_gra\\inne_tekstury\\noz.png'),270)
noz_equip_tekstura = pygame.image.load('moja_gra\\inne_tekstury\\noz_equip_wycongnienty.png')
noz_equip_tekstura = pygame.transform.scale(noz_equip_tekstura, (200,200))
noz_equip_tekstura_2 = pygame.image.load('moja_gra\\inne_tekstury\\noz_equip_wycongnienty_+.png')
noz_equip_tekstura_2 = pygame.transform.scale(noz_equip_tekstura_2, (200,200))
obramowka = pygame.image.load('moja_gra\\inne_tekstury\\obramowka.png')
obramowka = pygame.transform.scale(obramowka, (200,100))
monetka = pygame.image.load('moja_gra\\inne_tekstury\\monetka.png')
monetka = pygame.transform.scale(monetka, (50,50))

do_wpisywania = pygame.image.load('moja_gra\\inne_tekstury\\do_wpisywania.png')
do_wpisywania = pygame.transform.scale(do_wpisywania, (300,100))

obramowkaaaa = pygame.image.load('moja_gra\\inne_tekstury\\obramowkaaaa.png')
obramowkaaaa = pygame.transform.scale(obramowkaaaa, (szerokosc_okna,wysokosc_okna))

przycisk_start_img = pygame.image.load('moja_gra\\inne_tekstury\\przycisk_start.png')
przycisk_start_img = pygame.transform.scale(przycisk_start_img, (270, 100))

przycisk_usun_img = pygame.image.load('moja_gra\\inne_tekstury\\usun_przycisk.png')
przycisk_usun_img = pygame.transform.scale(przycisk_usun_img, (100, 100))

do_wpisywania_zaznaczone = pygame.image.load('moja_gra\\inne_tekstury\\do_wpisywania_zaznaczone.png')
do_wpisywania_zaznaczone = pygame.transform.scale(do_wpisywania_zaznaczone, (270,100))

pygame.display.set_caption("Zombie destroyer")

class PoleTekstowe:
    def __init__(self, x, y, szerokosc, wysokosc):
        self.rect = pygame.Rect(x, y, szerokosc, wysokosc)
        self.tekst = ''
        self.aktywne = False
        self.czcionka = pygame.font.Font('moja_gra\\inne\\PressStart2P-Regular.ttf', 23)

    def obsluz_zdarzenie(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.aktywne = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.aktywne:
            if event.key == pygame.K_RETURN:
                self.aktywne = False
            elif event.key == pygame.K_BACKSPACE:
                self.tekst = self.tekst[:-1]
            else:
                if len(self.tekst) < 11 and (event.unicode.isalnum() or event.unicode in ['_', '-']):
                    self.tekst += event.unicode

    def rysuj(self, okno):
        okno.blit(do_wpisywania, (self.rect.x-20, self.rect.y-20))
        pixel_czionka = pygame.font.Font('moja_gra\\inne\\PressStart2P-Regular.ttf', 23)
        tekst_surf = pixel_czionka.render(self.tekst, True, KOLOR_TEKSTU)
        okno.blit(tekst_surf, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(okno, (0,0,0), self.rect, 2)

class Maczeta:
    def __init__(self, x, y, zdj):
        self.x = x
        self.y = y
        self.klikniety = False
        self.wczesiniej_kliknienty = False
        self.original_zdj = zdj
        self.zdj = zdj
        self.rect = self.zdj.get_rect()
        self.kat = 0
        self.offset = 50
        self.mask = pygame.mask.from_surface(zdj)
        self.dlugosc = zdj.get_width()
    
    def aktualizuj(self, gracz_pos, mouse_pos, kierunek_postaci):
        if self.klikniety:
            dx = mouse_pos[0] - gracz_pos[0]
            dy = mouse_pos[1] - gracz_pos[1]
            desired_angle = math.degrees(math.atan2(-dy, dx)) - 90  
            desired_angle %= 360  

            if kierunek_postaci == "lewa":
                main_angle = 90
                min_angle = 0 
                max_angle = 180
            elif kierunek_postaci == "prawa":
                main_angle = 0
                min_angle = 180
                max_angle =  360
            elif kierunek_postaci == "pszud":
                main_angle = 90
                min_angle = 270
                max_angle = 90
            elif kierunek_postaci == "dul":
                main_angle = 180   
                min_angle = 90
                max_angle = 270

            if min_angle < max_angle:
                clamped_angle = max(min(desired_angle, max_angle), min_angle)
            else:
                if desired_angle > max_angle and desired_angle < min_angle:
                    if abs(desired_angle - max_angle) < abs(desired_angle - min_angle):
                        clamped_angle = max_angle
                    else:
                        clamped_angle = min_angle
                else:
                    clamped_angle = desired_angle

            radians = math.radians(clamped_angle + 90)
            dx_clamped = math.cos(radians)
            dy_clamped = -math.sin(radians)
            dystans = math.hypot(dx_clamped, dy_clamped)
            if dystans > 0:
                kierunek = (dx_clamped/dystans, dy_clamped/dystans)
                self.x = gracz_pos[0] + kierunek[0] * self.offset
                self.y = gracz_pos[1] + kierunek[1] * self.offset

            self.kat = clamped_angle
            self.zdj = pygame.transform.rotate(self.original_zdj, self.kat)
            self.rect = self.zdj.get_rect(center=(self.x, self.y))
            self.mask = pygame.mask.from_surface(self.zdj)
    
    def wyjmowanie(self, keys):
        if keys[pygame.K_1] and not self.wczesiniej_kliknienty:  
            self.klikniety = not self.klikniety  
            self.wczesiniej_kliknienty = True
        elif not keys[pygame.K_1]:  
            self.wczesiniej_kliknienty = False
            
    def rysuj_do_maczety(self, okno):
        okno.blit(noz_equip_tekstura, (255,590))
        if self.klikniety:
            okno.blit(noz_equip_tekstura_2, (255,590))

class Monetka:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tekstura = monetka
        self.rect = self.tekstura.get_rect(center=(x, y))
        self.czas_powstania = pygame.time.get_ticks()
    
    def czy_istnieje(self):
        return pygame.time.get_ticks() - self.czas_powstania < MONETA_CZAS_ZYCIA

class Gracz:
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.kierunek_postaci = "dul"
        self.obecna_klatka = 0
        self.predkosc_poruszania = 10
        self.poruszanie = False
        self.czas_animacji = 0
        self.ostatnie_uderzenie = 0  
        self.cooldown_uderzen = 1000 
        self.jest_nietykalny = False
        self.noz = Maczeta(x, y, noz_tekstura)
        self.noz_equip = noz_equip_tekstura
        self.punkty = 0
        self.waluta = 0
        self.level = 1
        self.czas_odnowienia_zombie = 2000 

    def szerokosc_gracza(self):
        if self.kierunek_postaci == "dul":
            return poruszanie_do_dolu[0].get_width()
        elif self.kierunek_postaci == "lewa":
            return poruszanie_do_lewej[0].get_width()
        elif self.kierunek_postaci == "prawa":
            return poruszanie_do_prawej[0].get_width()
        elif self.kierunek_postaci == "pszud":
            return poruszanie_do_pszodu[0].get_width()

    def wysokosc_gracza(self):
        if self.kierunek_postaci == "dul":
            return poruszanie_do_dolu[0].get_height()
        elif self.kierunek_postaci == "lewa":
            return poruszanie_do_lewej[0].get_height()
        elif self.kierunek_postaci == "prawa":
            return poruszanie_do_prawej[0].get_height()
        elif self.kierunek_postaci == "pszud":
            return poruszanie_do_pszodu[0].get_height()

    def tabliczka_zdrowia(self, okno):
        dlugosc_paska = self.szerokosc_gracza() * (self.hp / 100)
        pygame.draw.rect(okno, (255, 0, 0), (self.x, self.y - 20, dlugosc_paska, 10))
        pygame.draw.rect(okno, (255, 255, 255), (self.x, self.y - 20, self.szerokosc_gracza(), 10), 1)

    def rysuj(self, okno):
        if self.kierunek_postaci == "dul":
            okno.blit(poruszanie_do_dolu[self.obecna_klatka], (self.x, self.y))
        elif self.kierunek_postaci == "lewa":
            okno.blit(poruszanie_do_lewej[self.obecna_klatka], (self.x, self.y))
        elif self.kierunek_postaci == "prawa":
            okno.blit(poruszanie_do_prawej[self.obecna_klatka], (self.x, self.y))
        elif self.kierunek_postaci == "pszud":
            okno.blit(poruszanie_do_pszodu[self.obecna_klatka], (self.x, self.y))
        
        if self.noz.klikniety:
            okno.blit(self.noz.zdj, self.noz.rect)
        
        self.tabliczka_zdrowia(okno)
        okno.blit(noz_equip_tekstura_2, (255,590))

    def poruszaj(self, keys):
        self.poruszanie = False
        if self.czas_animacji < 1:
            self.czas_animacji += 1.2
        else:
            self.czas_animacji = 0

            if keys[pygame.K_d] and self.x + self.predkosc_poruszania < szerokosc_okna - self.predkosc_poruszania * 8:
                self.x += self.predkosc_poruszania
                self.kierunek_postaci = "prawa"
                self.poruszanie = True
            elif keys[pygame.K_a] and self.x - self.predkosc_poruszania > 5:
                self.x -= self.predkosc_poruszania
                self.kierunek_postaci = "lewa"
                self.poruszanie = True
            elif keys[pygame.K_s] and self.y + self.wysokosc_gracza() + 10 < wysokosc_okna:
                self.y += self.predkosc_poruszania
                self.kierunek_postaci = "dul"
                self.poruszanie = True
            elif keys[pygame.K_w] and self.y + self.wysokosc_gracza() + 10 > 120:
                self.y -= self.predkosc_poruszania
                self.kierunek_postaci = "pszud"
                self.poruszanie = True

            if self.poruszanie:
                self.obecna_klatka = (self.obecna_klatka + 1) % 6
            else:
                self.obecna_klatka = 1
    
    def upgrade(self):
        if self.level == 1 and self.punkty >= 200:
           self.level += 1
           self.czas_odnowienia_zombie = 1500
        elif self.level == 2 and self.waluta >= 300:
           self.level += 1
           self.czas_odnowienia_zombie = 1000
        elif self.level == 3 and self.waluta >= 600:
           self.level += 1
           self.czas_odnowienia_zombie = 500

class Zombie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.obecna_klatka = 0
        self.predkosc_poruszania = 3
        self.animacje = poruszanie_do_pszodu_zombie
        self.maska = pygame.mask.from_surface(self.animacje[0])
        self.czas_animacji = 0
        
    def rysuj(self, okno):
        okno.blit(self.animacje[self.obecna_klatka], (self.x, self.y))
        if self.czas_animacji < 1:
            self.czas_animacji += 1.2
        else:
            self.czas_animacji = 0
            self.obecna_klatka = (self.obecna_klatka + 1) % len(self.animacje)
            
    def poruszaj(self, gracz):
        if self.x < gracz.x:
            self.x += self.predkosc_poruszania
        elif self.x > gracz.x:
            self.x -= self.predkosc_poruszania
            
        if self.y < gracz.y:
            self.y += self.predkosc_poruszania
        elif self.y > gracz.y:
            self.y -= self.predkosc_poruszania

def zapisz_gre(gracz, nazwa_pliku):
    if not os.path.exists(KATALOG_ZAPISOW):
        os.makedirs(KATALOG_ZAPISOW)
    
    dane = {
        'x': gracz.x,
        'y': gracz.y,
        'hp': gracz.hp,
        'punkty': gracz.punkty,
        'waluta': gracz.waluta,
        'level': gracz.level,
        'predkosc_poruszania': gracz.predkosc_poruszania,
        'czas_odnowienia_zombie': gracz.czas_odnowienia_zombie
    }
    
    sciezka = os.path.join(KATALOG_ZAPISOW, f"{nazwa_pliku}.json")
    with open(sciezka, 'w') as plik:
        json.dump(dane, plik)

def wczytaj_gre(nazwa_pliku):
    sciezka = os.path.join(KATALOG_ZAPISOW, f"{nazwa_pliku}.json")
    if os.path.exists(sciezka):
        with open(sciezka, 'r') as plik:
            return json.load(plik)
    return None

def menu_startowe():
    zajebiste_menu = pygame.image.load('moja_gra\\inne_tekstury\\ALE_ZAJEBISTE_MENU.png').convert()
    zajebiste_menu = pygame.transform.scale(zajebiste_menu, (szerokosc_okna, wysokosc_okna))

    przycisk_nowa_gra = pygame.image.load('moja_gra\\inne_tekstury\\przycisk_nowa_gra.png')
    przycisk_nowa_gra = pygame.transform.scale(przycisk_nowa_gra, (256,128))
    przycisk_rect = przycisk_nowa_gra.get_rect(topleft=(250,400))
    
    przycisk_wczytaj = pygame.image.load('moja_gra\\inne_tekstury\\przycisk_wczytaj.png')
    przycisk_wczytaj = pygame.transform.scale(przycisk_wczytaj, (256,128))
    przycisk_wczytaj_rect = przycisk_wczytaj.get_rect(topleft=(250,550))
    
    ikonka_tiktoka = pygame.image.load('moja_gra\\inne_tekstury\\ikonka_tiktoka.png')
    ikonka_tiktoka = pygame.transform.scale(ikonka_tiktoka, (100,100))
    przycisk_tiktoka = ikonka_tiktoka.get_rect(topleft=(10,650))
    ikonka_insta = pygame.image.load('moja_gra\\inne_tekstury\\insta_logo.png')
    ikonka_insta = pygame.transform.scale(ikonka_insta, (100,100))
    przycisk_insta= ikonka_insta.get_rect(topleft=(120,650))
    

    while True:
        okno.blit(zajebiste_menu, (0,0))
        okno.blit(przycisk_nowa_gra, (250,400))
        okno.blit(przycisk_wczytaj, (250, 550))
        okno.blit(ikonka_tiktoka, (10, 650))
        okno.blit(ikonka_insta, (120, 650))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if przycisk_rect.collidepoint(event.pos):
                    return "nowa_gra"
                elif przycisk_wczytaj_rect.collidepoint(event.pos):
                    return "wczytaj"
                elif przycisk_tiktoka.collidepoint(event.pos):
                    webbrowser.open(url)
                elif przycisk_insta.collidepoint(event.pos):
                    webbrowser.open(url_insta)
        
        pygame.display.flip()

def menu_tworzenia_gry():
    if not os.path.exists(KATALOG_ZAPISOW):
        os.makedirs(KATALOG_ZAPISOW)
    pole_nazwy = PoleTekstowe(250, 400, 250, 50)
    przycisk_start = pygame.Rect(250, 500, 250, 100)
    czcionka_pixel = pygame.font.Font('moja_gra\\inne\\PressStart2P-Regular.ttf', 23)
    istniejące_zapisy = len([f for f in os.listdir(KATALOG_ZAPISOW) if f.endswith('.json')])
    
    if istniejące_zapisy >= MAX_ZAPISOW:
        przycisk_ok = pygame.Rect(300, 450, 150, 50)
        while True:
            okno.blit(obramowkaaaa, (0,0))
            czcionka_pixel = pygame.font.Font('moja_gra\\inne\\PressStart2P-Regular.ttf', 28)
            komunikat = czcionka_pixel.render("Osiagnieto limit", True, (183, 21, 21))
            okno.blit(komunikat, (140, 350))
            komunikat2 = czcionka_pixel.render("zapisow!", True, (183, 21, 21))
            okno.blit(komunikat2, (240, 400))
            pygame.draw.rect(okno, (0, 200, 0), przycisk_ok)
            tekst_ok = czcionka_pixel.render("OK", True, (0,0,0))
            okno.blit(tekst_ok, (przycisk_ok.x + 50, przycisk_ok.y + 10))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if przycisk_ok.collidepoint(event.pos):
                        return None
            pygame.display.flip()

    while True:
        okno.blit(obramowkaaaa, (0,0))
        tekst_tytul = czcionka_pixel.render("Podaj nazwe zapisu", True, (183, 21, 21))
        okno.blit(tekst_tytul, (180, 350))
        pole_nazwy.rysuj(okno)
        okno.blit(przycisk_start_img, (przycisk_start.x, przycisk_start.y))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
            pole_nazwy.obsluz_zdarzenie(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if przycisk_start.collidepoint(event.pos) and pole_nazwy.tekst:
                    if os.path.exists(os.path.join(KATALOG_ZAPISOW, f"{pole_nazwy.tekst}.json")):
                        czcionka_pixel = pygame.font.Font('moja_gra\\inne\\PressStart2P-Regular.ttf', 20)
                        przycisk_tak = pygame.Rect(200, 450, 100, 50)
                        przycisk_nie = pygame.Rect(450, 450, 100, 50)
                        while True:
                            okno.blit(obramowkaaaa, (0,0))
                            pytanie = czcionka_pixel.render("Nadpisac zapis?", True, (183,21,21))
                            okno.blit(pytanie, (230, 350))
                            pygame.draw.rect(okno, (0,200,0), przycisk_tak)
                            pygame.draw.rect(okno, (200,0,0), przycisk_nie)
                            okno.blit(czcionka_pixel.render("TAK", True, (0,0,0)), (przycisk_tak.x + 20, przycisk_tak.y + 10))
                            okno.blit(czcionka_pixel.render("NIE", True, (0,0,0)), (przycisk_nie.x + 20, przycisk_nie.y + 10))
                            
                            for e in pygame.event.get():
                                if e.type == pygame.MOUSEBUTTONDOWN:
                                    if przycisk_tak.collidepoint(e.pos):
                                        return pole_nazwy.tekst
                                    elif przycisk_nie.collidepoint(e.pos):
                                        break
                                if e.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
                            pygame.display.flip()
                            break
                    else:
                        return pole_nazwy.tekst
        
        pygame.display.flip()

def menu_wczytywania_gry():
    if not os.path.exists(KATALOG_ZAPISOW):
        os.makedirs(KATALOG_ZAPISOW)
    
    zapisy = [f[:-5] for f in os.listdir(KATALOG_ZAPISOW) if f.endswith('.json')]
    przyciski = []
    przycisk_usun = pygame.Rect(50, 50, 100, 100)
    czcionka = pygame.font.Font('moja_gra\\inne\\PressStart2P-Regular.ttf', 23)
    
    for i, zapis in enumerate(zapisy):
        przyciski.append(pygame.Rect(230, 50 + i*90, 250, 50))
    
    tryb_usuwania = False
    wybrany_zapis = None
    
    while True:
        okno.blit(obramowkaaaa, (0,0))
        zapisy = [f[:-5] for f in os.listdir(KATALOG_ZAPISOW) if f.endswith('.json')]
        przyciski = []
        for i, zapis in enumerate(zapisy):
            przyciski.append(pygame.Rect(230, 50 + i*90, 250, 50))

        if tryb_usuwania:
            tekst_trybu = czcionka.render("Wybierz zapis do usuniecia", True, (255, 0, 0))
        else:
            tekst_trybu = czcionka.render("Wybierz zapis do wczytania", True, (183, 21, 21))
        okno.blit(tekst_trybu, (60, 600))

        for i, (zapis, przycisk) in enumerate(zip(zapisy, przyciski)):
            if tryb_usuwania and wybrany_zapis == i:
                podswietlony = pygame.transform.scale(do_wpisywania_zaznaczone, (280,100))
                okno.blit(podswietlony, (przycisk.x, przycisk.y))
            else:
                okno.blit(do_wpisywania, (przycisk.x, przycisk.y))
            
            tekst_zapis = czcionka.render(zapis, True, (183, 21, 21))
            okno.blit(tekst_zapis, (przycisk.x + 25, przycisk.y + 25))

        okno.blit(przycisk_usun_img, (przycisk_usun.x, przycisk_usun.y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if przycisk_usun.collidepoint(event.pos):
                    if not tryb_usuwania and zapisy:
                        tryb_usuwania = True
                    elif tryb_usuwania and wybrany_zapis is not None:
                        sciezka = os.path.join(KATALOG_ZAPISOW, f"{zapisy[wybrany_zapis]}.json")
                        if os.path.exists(sciezka):
                            os.remove(sciezka)
                        tryb_usuwania = False
                        wybrany_zapis = None
                    elif tryb_usuwania:
                        tryb_usuwania = False
                        wybrany_zapis = None

                for i, przycisk in enumerate(przyciski):
                    if przycisk.collidepoint(event.pos):
                        if tryb_usuwania:
                            wybrany_zapis = i
                        else:
                            return zapisy[i]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if tryb_usuwania:
                        tryb_usuwania = False
                        wybrany_zapis = None
                    else:
                        return None

        pygame.display.flip()
def main():
    while True:
        wybor = menu_startowe()
        
        if wybor == "nowa_gra":
            nazwa_zapisu = menu_tworzenia_gry()
            if nazwa_zapisu is None:
                continue
            gracz = Gracz(400, 300, 100)
            break
        elif wybor == "wczytaj":
            nazwa_zapisu = menu_wczytywania_gry()
            if nazwa_zapisu is None:
                continue
            dane_gracza = wczytaj_gre(nazwa_zapisu)
            if dane_gracza:
                gracz = Gracz(dane_gracza['x'], dane_gracza['y'], dane_gracza['hp'])
                gracz.punkty = dane_gracza['punkty']
                gracz.waluta = dane_gracza['waluta']
                gracz.level = dane_gracza['level']
                gracz.predkosc_poruszania = dane_gracza.get('predkosc_poruszania', 10)
                gracz.czas_odnowienia_zombie = dane_gracza.get('czas_odnowienia_zombie', 2000)
            else:
                gracz = Gracz(400, 300, 100)
            break
    dziala = True
    lista_zombie = []
    lista_monet = []
    maks_zombie = 10
    czas_odnowienia_zombie = gracz.czas_odnowienia_zombie
    ostatni_czas_spawnu = 0
    zegar = pygame.time.Clock()
    
    def narysuj_mape():
        okno.blit(mapa, (0, 0))
        okno.blit(obramowka, (300,650))
        pixel_font = pygame.font.Font('moja_gra\\inne\\PressStart2P-Regular.ttf', 35)
        tekst_level = pixel_font.render(f"LVL:{gracz.level}", True, (0, 0, 0))
        tekst_punkty = pixel_font.render(f"Punkty:{gracz.punkty}", True, (0, 0, 0))
        tekst_waluta = pixel_font.render(f"${gracz.waluta}", True, (255, 215, 0))
        okno.blit(tekst_level, (10, 700))
        okno.blit(tekst_punkty, (10, 10))
        okno.blit(tekst_waluta, (600, 700))

    while dziala:
        aktualny_czas = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        gracz_pos = (gracz.x + gracz.szerokosc_gracza()//2, gracz.y + gracz.wysokosc_gracza()//2)
        gracz.upgrade()
        
        if len(lista_zombie) < maks_zombie and aktualny_czas - ostatni_czas_spawnu > czas_odnowienia_zombie:
            strona_spawnu = random.randint(0, 3)
            if strona_spawnu == 0:
                x = random.randint(0, szerokosc_okna)
                y = -50
            elif strona_spawnu == 1:
                x = szerokosc_okna + 50
                y = random.randint(0, wysokosc_okna)
            elif strona_spawnu == 2:
                x = random.randint(0, szerokosc_okna)
                y = wysokosc_okna + 50
            else:
                x = -50
                y = random.randint(0, wysokosc_okna)
                
            lista_zombie.append(Zombie(x, y))
            ostatni_czas_spawnu = aktualny_czas
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                zapisz_gre(gracz, nazwa_zapisu)
                dziala = False
        
        keys = pygame.key.get_pressed()
        gracz.poruszaj(keys)
        gracz.noz.wyjmowanie(keys)
        gracz.noz.rysuj_do_maczety(okno)
        gracz.noz.aktualizuj(gracz_pos, mouse_pos, gracz.kierunek_postaci)
        
        for zombie in lista_zombie:
            zombie.poruszaj(gracz)
        
        for zombie in lista_zombie[:]:
            if abs(zombie.x - gracz.x) < 50 and abs(zombie.y - gracz.y) < 50:
                if not gracz.jest_nietykalny:
                    gracz.hp -= 5
                    gracz.ostatnie_uderzenie = aktualny_czas
                    gracz.jest_nietykalny = True
                    if gracz.hp <= 0:
                        dziala = False
            
            if gracz.noz.klikniety:
                if zombie.maska.overlap(gracz.noz.mask, (gracz.noz.rect.x - zombie.x, gracz.noz.rect.y - zombie.y)):
                    zombie.hp -= 100
                    if zombie.hp <= 0:
                        lista_zombie.remove(zombie)
                        lista_monet.append(Monetka(zombie.x, zombie.y))

        for moneta in lista_monet[:]:
            if abs(moneta.x - gracz.x) < 50 and abs(moneta.y - gracz.y) < 50:
                gracz.punkty += 10
                gracz.waluta += 1
                if gracz.waluta % 10 == 0:
                    gracz.level += 1
                    gracz.predkosc_poruszania += 0.5
                lista_monet.remove(moneta)
            elif not moneta.czy_istnieje():
                lista_monet.remove(moneta)

        if gracz.jest_nietykalny and aktualny_czas - gracz.ostatnie_uderzenie > gracz.cooldown_uderzen:
            gracz.jest_nietykalny = False

        narysuj_mape()
        for moneta in lista_monet:
            if moneta.czy_istnieje():
                okno.blit(monetka, (moneta.x, moneta.y))
        gracz.rysuj(okno)
        
        for zombie in lista_zombie:
            zombie.rysuj(okno)
        
        if not gracz.noz.klikniety:
            okno.blit(obramowka, (300,650))
            okno.blit(gracz.noz_equip, (255,590))
        
        pygame.display.update()
        zegar.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
