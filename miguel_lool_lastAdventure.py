### The Last Adventure - Juego de rol de consola con narrativa generada por IA ###
### Desarrollado por Miguel Lool ###
### Ingeniería en Sistemas ###



import sys
import os
import time
import random
import msvcrt
from colorama import Fore, Back, Style, init
from openai import OpenAI
client = OpenAI()

###inicia el colorama###
init(autoreset=True)
os.system('mode con: cols=110 lines=30')
os.system('title The Last Adventure')

### class player y clase ###
class Player:
    def __init__(self):
        self.name = ''
        self.hp = 0
        self.mp = 0
        self.clase = ''
        self.inventory = []
        self.gold = 0
        self.lvl = 1
        self.historia = []
    
player1 = Player()

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def generar_narrativa(tipo_evento, contexto={}):
    system_prompt = f"""Eres el narrador de un RPG de aventuras llamado 'The Last Adventure'. 
Tu trabajo es crear narrativa inmersiva y emocionante, oscura y sin censura, que cada accion sea cruel, que represente la crueldad de este mundo oscuro y aterrador.
El jugador se llama {player1.name}, es un {player1.clase} de nivel {player1.lvl}.
HP actual: {player1.hp}, MP actual: {player1.mp}, Oro: {player1.gold}

IMPORTANTE: Mantén las respuestas cortas (2-4 oraciones) y descriptivas.
NO uses markdown ni formato especial, solo texto plano.
NO des opciones, solo narra la escena."""

    prompts = {
    'inicio': f"Narra el comienzo de la aventura de {player1.name}, un {player1.clase} que se embarca en una cruda y oscura aventura sobre un detino ya marcado.",
    'explorar': f"El jugador está explorando {contexto.get('lugar', 'un lugar desconocido')}. Narra lo que ve y siente en este entorno oscuro y peligroso.",
    'pre_combate': f"El jugador se encuentra con un enemigo peligroso: {contexto.get('enemigo', 'un enemigo desconocido')}. Narra la tensión y el miedo antes del combate.",
    'durante_combate': f"El jugador está en medio de un combate brutal contra {contexto.get('enemigo', 'un enemigo')}. Narra la acción y el peligro del enfrentamiento.",
    'victoria': f"El jugador ha derrotado a {contexto.get('enemigo', 'un enemigo')}. Narra la sensación de triunfo y las consecuencias de la victoria en este mundo cruel.",
    'derrota': f"El jugador ha sido derrotado por {contexto.get('enemigo', 'un enemigo')}. Narra la desesperación y las consecuencias de la derrota en este mundo oscuro.",
    'tienda': f"El jugador entra en una tienda oscura y misteriosa. Narra la atmósfera y los objetos extraños que encuentra para comprar.",
    'descanso': f"El jugador encuentra un lugar para descansar. Narra la sensación de alivio y la preparación para los peligros que le esperan.",
    'encuentro_especial': f"El jugador tiene un encuentro especial con {contexto.get('hallazgo', 'algo inesperado')}. Narra la interacción y las posibles consecuencias en esta aventura oscura.",
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompts.get(tipo_evento, prompts['explorar'])}
            ],
            max_tokens=150,
            temperature=0.8
        )
        
        narrativa = response.choices[0].message.content.strip()
        
        # Guardar en historial
        player1.historia.append({
            'tipo': tipo_evento,
            'narrativa': narrativa,
            'contexto': contexto
        })
        
        return narrativa
    
    except Exception as e:
        print(f"Error al generar narrativa: {e}")
    return f"Continúas tu aventura como {player1.clase}..."

def mostrar_narrativa(texto, color = Fore.LIGHTYELLOW_EX, velocidad=0.03):

    screen_width = os.get_terminal_size().columns
    palabras = texto.split(' ')
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        if len(linea_actual + palabra) < screen_width - 10:
            linea_actual += palabra + " "
        else:
            lineas.append(linea_actual.strip())
            linea_actual = palabra + " "
    
    if linea_actual:
        lineas.append(linea_actual.strip())
    
    print()
    for linea in lineas:
        for char in linea:
            print(color + char, end='', flush=True)
            time.sleep(velocidad)
        print()
    print()
    time.sleep(1)


### aqui e la logica de los combates ###
def combate():
    opciones_combate = ["Atacar", "Usar Pocion", "Huir"]
    enemigos = [
        {"nombre": "Goblin Putrefacto", "hp": 30, "atk": 5},
        {"nombre": "Esqueleto Sediento", "hp": 40, "atk": 7},
        {"nombre": "Orco Maldito", "hp": 50, "atk": 10},
        {"nombre": "Troll Hambriento", "hp": 60, "atk": 12},
        {"nombre": "Dragón Anciano", "hp": 100, "atk": 20},
        {"nombre": "Lobo Aullador", "hp": 35, "atk": 6},
        {"nombre": "Muerto Viviente", "hp": 45, "atk": 8},
        {"nombre": "Vampiro Acechador", "hp": 55, "atk": 11},
        {"nombre": "Hombre Lobo", "hp": 65, "atk": 13},
        {"nombre": "Demonio Anciano", "hp": 80, "atk": 15},
    ]
    enemigo = random.choice(enemigos)
    enemigo_hp = enemigo["hp"]
    seleccion = 0
    screen_width = os.get_terminal_size().columns
    limpiar_pantalla()
    narrativa_encuentro = generar_narrativa('pre_combate', {'enemigo': enemigo['nombre']})
    mostrar_narrativa(narrativa_encuentro, Fore.RED)
    input(Fore.CYAN + "Presiona Enter para iniciar el combate...".center(screen_width))

    while enemigo_hp > 0 and player1.hp > 0:
        limpiar_pantalla()
        print(Fore.GREEN + f"{player1.name} - HP: {player1.hp} | MP: {player1.mp}".center(screen_width))
        print(Fore.RED + f"{enemigo['nombre']} - HP: {enemigo_hp}".center(screen_width))
        print("\n")
        
        for i, opcion in enumerate(opciones_combate):
            if i == seleccion:
                print(Fore.CYAN + Style.BRIGHT + f"> {opcion} <".center(screen_width))
            else:
                print(Fore.WHITE + f"  {opcion}  ".center(screen_width))
        
        tecla = msvcrt.getch()
        if tecla == b'w' and seleccion > 0:
            seleccion -= 1
        elif tecla == b's' and seleccion < len(opciones_combate) - 1:
            seleccion += 1
        elif tecla == b'\r':
            # Empieza las acciones del combate
            if opciones_combate[seleccion] == "Atacar":
                dano = random.randint(10, 20)
                enemigo_hp -= dano
                print(Fore.YELLOW + f"\nHas atacado al {enemigo['nombre']} causando {dano} de daño.".center(screen_width))
            elif opciones_combate[seleccion] == "Usar Pocion":
                if "Poción de Vida" in player1.inventory:
                    curacion = random.randint(15, 25)
                    player1.hp += curacion
                    player1.inventory.remove("Poción de Vida")
                    print(Fore.MAGENTA + f"\nUsaste una poción y recuperaste {curacion} de HP.".center(screen_width))
                else:
                    print(Fore.MAGENTA + "\nNo tienes pociones!".center(screen_width))
            elif opciones_combate[seleccion] == "Huir":
                exito = random.choice([True, False])
                if exito:
                    print(Fore.LIGHTBLUE_EX + f"\nHas logrado huir del {enemigo['nombre']}!".center(screen_width))
                    time.sleep(2)
                    return
                else:
                    print(Fore.LIGHTBLUE_EX + f"\nNo pudiste escapar!".center(screen_width))
            
            # Turno del enemigo
            if enemigo_hp > 0:
                dano_enemigo = random.randint(1, enemigo["atk"])
                player1.hp -= dano_enemigo
                print(Fore.RED + f"El {enemigo['nombre']} te ataca y causa {dano_enemigo} de daño!".center(screen_width))
            
            time.sleep(2)
    
    limpiar_pantalla()
    if player1.hp > 0:
        # Narrativa de victoria con la api
        narrativa_victoria = generar_narrativa('victoria', {'enemigo': enemigo['nombre']})
        mostrar_narrativa(narrativa_victoria, Fore.GREEN)
        
        # Loot
        if random.random() < 0.5:
            item = "Poción de Vida"
            player1.inventory.append(item)
            print(Fore.YELLOW + f"Has conseguido un {item}!".center(screen_width))
        
        oro_ganado = random.randint(10, 50)
        player1.gold += oro_ganado
        print(Fore.YELLOW + f"Obtuviste {oro_ganado} de oro!".center(screen_width))
    else:
        # Narrativa de derrota con la api
        narrativa_derrota = generar_narrativa('derrota', {'enemigo': enemigo['nombre']})
        mostrar_narrativa(narrativa_derrota, Fore.RED)
        print(Fore.RED + "GAME OVER".center(screen_width))
        time.sleep(3)
        sys.exit()
    
    input("\nPresiona Enter para continuar...")

### SISTEMA DE EXPLORACIÓN ###
def explorar():
    lugares = ["un bosque oscuro", "unas ruinas antiguas", "una cueva misteriosa", 
               "un pueblo abandonado", "una montaña nevada"]
    
    lugar = random.choice(lugares)
    limpiar_pantalla()
    
    # Generar narrativa de exploración
    narrativa_explorar = generar_narrativa('explorar', {'lugar': lugar})
    mostrar_narrativa(narrativa_explorar, Fore.CYAN)
    
    # genera el Evento aleatorio
    evento = random.choice(['combate', 'tesoro', 'nada', 'encuentro_especial'])
    screen_width = os.get_terminal_size().columns
    
    if evento == 'combate':
        print(Fore.RED + "¡Un enemigo aparece!".center(screen_width))
        time.sleep(1)
        combate()
    elif evento == 'tesoro':
        oro = random.randint(20, 100)
        player1.gold += oro
        print(Fore.YELLOW + f"¡Encontraste un cofre con {oro} de oro!".center(screen_width))
        time.sleep(2)
    elif evento == 'encuentro_especial':
        narrativa_especial = generar_narrativa('encuentro_especial', 
                                               {'hallazgo': 'un artefacto mágico brillando en la oscuridad'})
        mostrar_narrativa(narrativa_especial, Fore.MAGENTA)
        time.sleep(2)
    else:
        print(Fore.WHITE + "No encuentras nada interesante...".center(screen_width))
        time.sleep(2)

### TIENDA ###
def tienda():
    limpiar_pantalla()
    screen_width = os.get_terminal_size().columns
    
    # genera la Narrativa de tienda
    narrativa_tienda = generar_narrativa('tienda')
    mostrar_narrativa(narrativa_tienda, Fore.YELLOW)
    
    items_tienda = [
        {"nombre": "Poción de Vida", "precio": 30},
        {"nombre": "Poción de Maná", "precio": 40},
        {"nombre": "Espada Mejorada", "precio": 100},
    ]
    
    seleccion = 0
    opciones = [f"{item['nombre']} - {item['precio']} oro" for item in items_tienda]
    opciones.append("Salir")
    
    while True:
        limpiar_pantalla()
        print(Fore.YELLOW + f"=== TIENDA === (Oro: {player1.gold})".center(screen_width))
        print()
        
        for i, opcion in enumerate(opciones):
            if i == seleccion:
                print(Fore.GREEN + Style.BRIGHT + f"> {opcion} <".center(screen_width))
            else:
                print(Fore.WHITE + f"  {opcion}  ".center(screen_width))
        
        tecla = msvcrt.getch()
        if tecla == b'w' and seleccion > 0:
            seleccion -= 1
        elif tecla == b's' and seleccion < len(opciones) - 1:
            seleccion += 1
        elif tecla == b'\r':
            if seleccion == len(opciones) - 1:  # Salir
                break
            else:
                item = items_tienda[seleccion]
                if player1.gold >= item['precio']:
                    player1.gold -= item['precio']
                    player1.inventory.append(item['nombre'])
                    print(Fore.GREEN + f"\n¡Compraste {item['nombre']}!".center(screen_width))
                else:
                    print(Fore.RED + "\n¡No tienes suficiente oro!".center(screen_width))
                time.sleep(2)
    
def menu_juego():
    opciones = ["Explorar", "Tienda", "Inventario", "Descansar", "Salir"]
    seleccion = 0
    screen_width = os.get_terminal_size().columns
    
    while True:
        limpiar_pantalla()
        print(Fore.CYAN + Style.BRIGHT + f"=== {player1.name} el {player1.clase} ===".center(screen_width))
        print(Fore.GREEN + f"HP: {player1.hp} | MP: {player1.mp} | Nivel: {player1.lvl} | Oro: {player1.gold}".center(screen_width))
        print()
        
        for i, opcion in enumerate(opciones):
            if i == seleccion:
                print(Fore.YELLOW + Style.BRIGHT + f"> {opcion} <".center(screen_width))
            else:
                print(Fore.WHITE + f"  {opcion}  ".center(screen_width))
        
        print()
        print(Fore.CYAN + "Usa W/S para navegar y Enter para seleccionar.".center(screen_width))
        
        tecla = msvcrt.getch()
        if tecla == b'w' and seleccion > 0:
            seleccion -= 1
        elif tecla == b's' and seleccion < len(opciones) - 1:
            seleccion += 1
        elif tecla == b'\r':
            if opciones[seleccion] == "Explorar":
                explorar()
            elif opciones[seleccion] == "Tienda":
                tienda()
            elif opciones[seleccion] == "Inventario":
                mostrar_inventario()
            elif opciones[seleccion] == "Descansar":
                descansar()
            elif opciones[seleccion] == "Salir":
                print("Este mundo no es para todos...")
                time.sleep(1)
                sys.exit()

def mostrar_inventario():
    limpiar_pantalla()
    screen_width = os.get_terminal_size().columns
    print(Fore.MAGENTA + "=== INVENTARIO ===".center(screen_width))
    print()
    if player1.inventory:
        for item in player1.inventory:
            print(Fore.WHITE + f"- {item}".center(screen_width))
    else:
        print(Fore.WHITE + "Tu inventario está vacío".center(screen_width))
    print()
    input(Fore.CYAN + "Presiona Enter para continuar...")

def descansar():
    limpiar_pantalla()
    screen_width = os.get_terminal_size().columns
    
    # Narrativa de descanso
    narrativa_descanso = generar_narrativa('descanso')
    mostrar_narrativa(narrativa_descanso, Fore.GREEN)
    
    curacion = 50
    player1.hp = min(player1.hp + curacion, 120)  # Max HP según clase
    print(Fore.GREEN + f"Recuperaste {curacion} HP".center(screen_width))
    time.sleep(2)

### Menu Principal ###
def mostrar_menu_principal(seleccion):
    opciones = ["Jugar", "Ayuda", "Salir"]
    screen_width = os.get_terminal_size().columns
    limpiar_pantalla()
    arte = r"""                                                                                                    
    ███        ▄█    █▄       ▄████████       ▄█          ▄████████    ▄████████     ███                   
▀█████████▄   ███    ███     ███    ███      ███         ███    ███   ███    ███ ▀█████████▄               
   ▀███▀▀██   ███    ███     ███    █▀       ███         ███    ███   ███    █▀     ▀███▀▀██               
    ███   ▀  ▄███▄▄▄▄███▄▄  ▄███▄▄▄          ███         ███    ███   ███            ███   ▀               
    ███     ▀▀███▀▀▀▀███▀  ▀▀███▀▀▀          ███       ▀███████████ ▀███████████     ███                   
    ███       ███    ███     ███    █▄       ███         ███    ███          ███     ███                   
    ███       ███    ███     ███    ███      ███▌    ▄   ███    ███    ▄█    ███     ███                   
   ▄████▀     ███    █▀      ██████████      █████▄▄██   ███    █▀   ▄████████▀     ▄████▀                 
                                             ▀                                                             
   ▄████████ ████████▄   ▄█    █▄     ▄████████ ███▄▄▄▄       ███     ███    █▄     ▄████████    ▄████████ 
  ███    ███ ███   ▀███ ███    ███   ███    ███ ███▀▀▀██▄ ▀█████████▄ ███    ███   ███    ███   ███    ███ 
  ███    ███ ███    ███ ███    ███   ███    █▀  ███   ███    ▀███▀▀██ ███    ███   ███    ███   ███    █▀  
  ███    ███ ███    ███ ███    ███  ▄███▄▄▄     ███   ███     ███   ▀ ███    ███  ▄███▄▄▄▄██▀  ▄███▄▄▄     
▀███████████ ███    ███ ███    ███ ▀▀███▀▀▀     ███   ███     ███     ███    ███ ▀▀███▀▀▀▀▀   ▀▀███▀▀▀     
  ███    ███ ███    ███ ███    ███   ███    █▄  ███   ███     ███     ███    ███ ▀███████████   ███    █▄  
  ███    ███ ███   ▄███ ███    ███   ███    ███ ███   ███     ███     ███    ███   ███    ███   ███    ███ 
  ███    █▀  ████████▀   ▀██████▀    ██████████  ▀█   █▀     ▄████▀   ████████▀    ███    ███   ██████████ 
                                                                                   ███    ███              
"""

    for line in arte.splitlines():
        print(Fore.RED + line.center(screen_width))
    for i, opcion in enumerate(opciones):
        if i == seleccion:
            print(Fore.RED + Style.BRIGHT + f"> {opcion} <".center(screen_width))
        else: print(Fore.WHITE + f"  {opcion}  ".center(screen_width))
    print()
    print(Fore.WHITE + "Usa W/S para navegar y Enter para seleccionar.".center(screen_width))

def menu_principal():
    seleccion = 0
    opciones = ["Jugar", "Ayuda", "Salir"]
    while True:
        mostrar_menu_principal(seleccion)
        tecla = msvcrt.getch()
        if tecla == b'w' and seleccion > 0:
            seleccion -= 1
        elif tecla == b's' and seleccion < len(opciones) - 1:
            seleccion += 1
        elif tecla == b'\r':
            if seleccion == 0:
                limpiar_pantalla()
                iniciar_juego()
                break
            elif seleccion == 1:
                mostrar_ayuda()
            elif seleccion == 2:
                print("Saliendo...")
                sys.exit()

def mostrar_ayuda():
    limpiar_pantalla()
    screen_width = os.get_terminal_size().columns
    print(Fore.CYAN + "=== AYUDA ===".center(screen_width))
    print()
    print(Fore.WHITE + "Controles:".center(screen_width))
    print(Fore.WHITE + "W/S - Navegar menús".center(screen_width))
    print(Fore.WHITE + "Enter - Seleccionar".center(screen_width))
    print()
    print(Fore.WHITE + "Explora, combate enemigos, compra items y sobrevive!".center(screen_width))
    print()
    input(Fore.CYAN + "Presiona Enter para continuar...")


def iniciar_juego():
    screen_width = os.get_terminal_size().columns
    arte_i = r"""                                                                                                 

      *                                                            *
                              aaaaaaaaaaaaaaaa               *
                          aaaaaaaaaaaaaaaaaaaaaaaa
                       aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
                     aaaaaaaaaaaaaaaaa           aaaaaa
                   aaaaaaaaaaaaaaaa                  aaaa
                  aaaaaaaaaaaaa aa                      aa
 *               aaaaaaaa      aa                         a
                 aaaaaaa aa aaaa
           *    aaaaaaaaa     aaa
                aaaaaaaaaaa aaaaaaa                               *
                aaaaaaa    aaaaaaaaaa
                aaaaaa a aaaaaa aaaaaa
                 aaaaaaa  aaaaaaa
                 aaaaaaaa                                 a
                  aaaaaaaaaa                            aa
                   aaaaaaaaaaaaaaaa                  aaaa
                     aaaaaaaaaaaaaaaaa           aaaaaa        *
       *               aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
                          aaaaaaaaaaaaaaaaaaaaaaaa
                       *      aaaaaaaaaaaaaaaa
           
"""

    for line in arte_i.splitlines():
        print(Fore.LIGHTRED_EX + line)
    input_name = input(Fore.LIGHTWHITE_EX + "Bienvenido Aventurero, antes de todo... empecemos por lo basico. ¿Cuál es tu nombre?" + "\n> ")
    player1.name = input_name
    limpiar_pantalla()
    seleccion_clase()

def asignar_stats(player):
    if player.clase == "Guerrero":
        player.hp = 120
        player.mp = 30
    elif player.clase == "Mago":
        player.hp = 70
        player.mp = 120
    elif player.clase == "Arquero":
        player.hp = 90
        player.mp = 60

def seleccion_clase():
    clase_seleccion = [
        ("Guerrero", "Fuerte y resistente, experto en combate cuerpo a cuerpo."),
        ("Mago", "Sabio y poderoso, domina la energía mágica."),
        ("Arquero", "Ágil y preciso, letal a distancia."),
    ]
    seleccion = 0
    clase_arte = [
        ("Guerrero", r"""                         
              /
       ,~~   /
   _  <=)  _/_
  /I\.="==.{>
  \I/-\T/-'
      /_\
     // \\_
    _I    /
         
 
"""),
        ("Mago", r""" 

            ,    _
           /|   | |
         _/_\_  >_<
        .-\-/.   |
       /  | | \_ |
       \ \| |\__(/
       /(`---')  |
      / /     \  |
   _.'  \'-'  /  |
   `----'`=-='   '
"""),
        ("Arquero", r"""
       /\
      /__\_{)
     |--<<)__\
      \  /  (
       \/   )
           /|
           \ \
           ~ ~         
""")
    ]
    while True:
        limpiar_pantalla()
        screen_width = os.get_terminal_size().columns
        print(Fore.YELLOW + Style.BRIGHT + "Elige tu clase, " + player1.name +"\n".center(screen_width))
        max_len = max(len(line) for line in clase_arte)
        screen_width = os.get_terminal_size().columns 
        margen = (screen_width - max_len) // 2
        for line in clase_arte[seleccion][1].splitlines():
                 print(" " * margen+ Fore.LIGHTMAGENTA_EX + line)
        for i, (nombre, desc) in enumerate(clase_seleccion):
            if i == seleccion:
                print(Fore.GREEN + Style.BRIGHT + f"> {nombre} <".center(screen_width))
                print(Fore.LIGHTBLACK_EX + desc.center(screen_width))
            else:
                print(Fore.WHITE + f"  {nombre}  ".center(screen_width))
        print()
        print(Fore.CYAN + "Usa W/S para moverte y Enter para seleccionar.".center(screen_width))
        tecla = msvcrt.getch()
        if tecla == b'w' and seleccion > 0:
            seleccion -= 1
        elif tecla == b's' and seleccion < len(clase_seleccion) - 1:
            seleccion += 1
        elif tecla == b'\r':
            player1.clase = clase_seleccion[seleccion][0]
            asignar_stats(player1)
            limpiar_pantalla()
            print(Fore.GREEN + f"¡Has elegido la clase {player1.clase}, {player1.name}!".center(screen_width))
            print(Fore.GREEN + f"HP: {player1.hp} | MP: {player1.mp}".center(screen_width))
            time.sleep(2)
            menu_juego()
            break


menu_principal()
