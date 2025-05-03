from flask import Flask, render_template, request
from InvertirBinario import TuringMachine
from InvertirBinario import animate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculator():
    input_expr = ''
    result = ''

    if request.method == 'POST':
        button = request.form['button']
        input_expr = request.form['input']

        if button == 'C': #se borra el numero que el usuario escribio
            input_expr = ''
            result = ''
        elif button == '=': #llama a la maquina de turing
            entrada = input_expr
            input_expr = ''
            mt = TuringMachine(tape=entrada)
            tape_history, head_history, state_history = mt.run()
            # Imprimir la cinta final limpia
            result = limpiar_tape(mt.tape)
            print("Cinta final:", result)

            # Crear la animación
            fig, ax = plt.subplots(figsize=(10, 2))
            ani = animation.FuncAnimation(fig, animate, frames=len(tape_history),
                                          fargs=(tape_history, head_history, state_history, ax),
                                          interval=500, repeat=False)

            # Guardar el gif
            ani.save('static/turing_animation.gif', writer='pillow')  #guarda la imagen
            animation_generated = True
            plt.close(fig)  # cierra la figura para liberar memoria


        else:
            input_expr += button #acumula los valores que se ingresan del boton

    return render_template('index.html', input_expr=input_expr, result=result)

# Función para obtener la cinta limpia (sin A, Z, espacios)
def limpiar_tape(tape):
    return ''.join([c for c in tape if c not in ['A', 'Z', ' ']])


if __name__ == '__main__':
    app.run(debug=True)
