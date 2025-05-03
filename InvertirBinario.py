import matplotlib.pyplot as plt
import matplotlib.animation as animation

class TuringMachine:
    def __init__(self, tape, blank=' '):
        self.tape = list(blank + tape + blank * 20) #inicializar la cinta
        self.head = 1  # empieza justo al inicio de la palabra
        self.blank = blank #simbolo en blanco
        self.state = 'q0' # estado de inicio
        self.transitions = {
            #Se desplaza hacia la izquierda hasta encontrar un blanco, 
            #que se reemplaza por A (inicio de palabra).
            ('q0', '0'): ('q0', '0', 'L'),
            ('q0', '1'): ('q0', '1', 'L'),
            ('q0', blank): ('q1', 'A', 'R'),

            #Se mueve hacia la derecha hasta encontrar el primer blanco 
            # a la derecha del último símbolo. Lo reemplaza por Z (fin de palabra).
            ('q1', '0'): ('q1', '0', 'R'),
            ('q1', '1'): ('q1', '1', 'R'),
            ('q1', blank): ('q2', 'Z', 'L'),

            #Se mueve hacia la izquierda hasta encontrar el primer símbolo válido (0 o 1),
            # lo borra (reemplaza con B), y según el símbolo, 
            # transiciona a q3 (para 1) o q6 (para 0).
            ('q2', blank): ('q2', blank, 'L'),
            ('q2', '1'): ('q3', blank, 'R'),
            ('q2', '0'): ('q6', blank, 'R'),
            ('q2', 'A'): ('q8', blank, 'L'),

            # Avanza hacia la derecha buscando Z.
            ('q3', blank): ('q3', blank, 'R'),
            ('q3', 'Z'): ('q4', 'Z', 'R'),

            #Escribe 1 justo después de Z, y transiciona a q5.
            ('q4', '0'): ('q4', '0', 'R'),
            ('q4', '1'): ('q4', '1', 'R'),
            ('q4', blank): ('q5', '1', 'L'),

            #Regresa hacia la izquierda hasta encontrar Z para volver a q2.
            ('q5', '0'): ('q5', '0', 'L'),
            ('q5', '1'): ('q5', '1', 'L'),
            ('q5', 'Z'): ('q2', 'Z', 'L'),

            #Avanza hacia la derecha buscando Z.
            ('q6', blank): ('q6', blank, 'R'),
            ('q6', 'Z'): ('q7', 'Z', 'R'),
            
            #Escribe 0 justo después de Z, y transiciona a q5.
            ('q7', '0'): ('q7', '0', 'R'),
            ('q7', '1'): ('q7', '1', 'R'),
            ('q7', blank): ('q5', '0', 'L'),

            #Cuando no quedan más símbolos, limpia Z y va al estado final.
            ('q8', blank): ('q8', blank, 'R'),
            ('q8', 'Z'): ('q9', blank, 'R'),


        }

    #muestra el contenido actual de la cinta y la posicion del cabezal
    def print_tape(self):
        tape_str = ''.join(self.tape)
        head_str = ' ' * self.head + '^' #marca la posicion del cabezal
        return f"{tape_str}\n       {head_str} (estado: {self.state})\n"

    #ejecuta un solo paso de la máquina
    def step(self):
        #asegura que el cabezal nunca salga de los límites
        if self.head < 0:
            self.tape.insert(0, self.blank)
            self.head = 0
        elif self.head >= len(self.tape):
            self.tape.append(self.blank)

        symbol = self.tape[self.head] #lee el simbolo actual
        key = (self.state, symbol) #crea la clave para buscar transición

        if key in self.transitions:
            new_state, new_symbol, direction = self.transitions[key]
            self.tape[self.head] = new_symbol #escribe nuevo símbolo
            self.state = new_state #cambia al nuevo estado
            self.head += 1 if direction == 'R' else -1 #mueve el cabezal
        else:
            self.state = 'HALT' #si no hay transicion, detiene la maquina

    #ejecuta la maquina hasta llegar a q9 o exceder los pasos maximos
    def run(self, max_steps=10000):
        steps = 0
        tape_history = [] # Guarda las cintas en cada paso
        head_history = [] # Guarda la posicion del cabezal
        state_history = [] # Guarda el estado

        while self.state != 'q9' and steps < max_steps:
            tape_history.append(self.tape[:])
            head_history.append(self.head)
            state_history.append(self.state)
            self.step()
            steps += 1

        # Guardar el ultimo paso cuando llego a q9
        tape_history.append(self.tape[:])
        head_history.append(self.head)
        state_history.append(self.state)

        return tape_history, head_history, state_history

#funcion para la animacion
def animate(i, tape_history, head_history, state_history, ax):
    ax.clear()
    tape = tape_history[i]
    head = head_history[i]
    state = state_history[i]

    #dibuja cada celda de la cinta como un cuadro
    for j, symbol in enumerate(tape):
        rect = plt.Rectangle((j, 0), 1, 1, edgecolor='black', facecolor='lightcyan')
        ax.add_patch(rect)
        ax.text(j + 0.5, 0.5, symbol, ha='center', va='center', fontsize=14)

    # Dibujar el cabezal
    arrow_color = 'red'
    if state == 'q9':
        arrow_color = 'green'  #cuando ya llego a q9
    ax.text(head + 0.5, 1.3, '↓', ha='center', va='center', fontsize=16, color=arrow_color)

    #muestra el estado actual
    ax.text(len(tape) / 2, 2, f"Estado: {state}", ha='center', va='center', fontsize=14, color='blue')

    #ajusta la vista del grafico
    ax.set_xlim(-1, len(tape) + 1)
    ax.set_ylim(-0.5, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')

