import numpy as np
from scamp import *
import pretty_midi

# Se carga el archivo MIDI
midi_file = pretty_midi.PrettyMIDI('fur-elise.mid')

# Con la librería pretty_midi se extraen las notas del archivo MIDI
notes = []
for instrument in midi_file.instruments:
    for note in instrument.notes:
        notes.append(note.pitch)

# Se construye la cadena de Markov
markov_chain = {}
for i in range(len(notes) - 1):
    current_note = notes[i]
    next_note = notes[i + 1]
    if current_note not in markov_chain:
        markov_chain[current_note] = {}
    if next_note not in markov_chain[current_note]:
        markov_chain[current_note][next_note] = 0
    markov_chain[current_note][next_note] += 1

print("Cadena de Markov: ") 
print(markov_chain)

# Se obtienen las notas únicas y se construye la matriz de transición (se normaliza la matriz asegurando que la suma de las probabilidades de transición sea 1)
unique_notes = list(set(notes))
num_notes = len(unique_notes)
transition_matrix = np.zeros((num_notes, num_notes))

for i, current_note in enumerate(unique_notes):
    for j, next_note in enumerate(unique_notes):
        if current_note in markov_chain and next_note in markov_chain[current_note]:
            transition_count = markov_chain[current_note][next_note]
            total_count = sum(markov_chain[current_note].values())
            transition_matrix[i, j] = transition_count / total_count

print("\nMatriz de transición: ")
np.set_printoptions(threshold=np.inf)
np.set_printoptions(formatter={'float': '{: 0.5f}'.format})
print(transition_matrix)


# Se imprimen las probabilidades de transición para cada nota
print("\nProbabilidades de transición:")
for i, current_note in enumerate(unique_notes):
    print(f"Nota actual: {pretty_midi.note_number_to_name(current_note)}")
    for j, next_note in enumerate(unique_notes):
        probability = transition_matrix[i, j]
        if probability > 0:
            print(f"  - Siguiente nota: {pretty_midi.note_number_to_name(next_note)}, Probabilidad: {probability:.5f}")

# Se convierten los números de nota a nombres de nota con su respectiva frecuencia
notes = {}
for note_num in unique_notes:
    note_name = pretty_midi.note_number_to_name(note_num)
    notes[note_name] = pretty_midi.note_number_to_hz(note_num)

print("\nNotas y frecuencias:")
print(notes)

# Configuración de la sesión de SCAMP
session = Session()
piano = session.new_part("Piano")

def freq_to_midi(freq):
    return round(69 + 12 * np.log2(freq / 440))

def generar_tono(frecuencia, duracion):
    pitch = freq_to_midi(frecuencia)
    print("Pitch:", pitch)
    piano.play_note(pitch, 1.0, duracion)

def generador_melodias(num_transiciones):
    notas = list(notes.keys())
    nota_actual = np.random.choice(notas)
    print("Nota:", nota_actual)
    generar_tono(notes[nota_actual], 0.35)

    for _ in range(num_transiciones - 1):
        indice_actual = notas.index(nota_actual)
        nota_actual = np.random.choice(notas, p=transition_matrix[indice_actual])
        print("Nota:", nota_actual)
        generar_tono(notes[nota_actual], 0.35)
        
number_of_transitions = 100
generador_melodias(number_of_transitions)