import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parametry audio
CHUNK = 1024  # Liczba próbek na ramkę
FORMAT = pyaudio.paInt16  # Format danych audio (16-bitowy int)
CHANNELS = 1  # Liczba kanałów (mono)
RATE = 44100  # Częstotliwość próbkowania (Hz)

# Inicjalizacja PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

# Funkcja inicjalizująca wykres
def init_plot():
    ax.set_xlim(0, RATE // 2)  # Częstotliwości od 0 do Nyquista
    ax.set_ylim(0, 10)  # Zasięg amplitudy
    return line,

# Funkcja aktualizująca wykres
def update(frame):
    # Odczytaj dane z mikrofonu
    data = stream.read(CHUNK, exception_on_overflow=False)
    audio_data = np.frombuffer(data, dtype=np.int16)

    # Oblicz transformatę Fouriera
    fft_data = np.fft.rfft(audio_data)
    fft_magnitude = np.abs(fft_data) / CHUNK  # Normalizacja

    # Oś częstotliwości
    freqs = np.fft.rfftfreq(CHUNK, 1 / RATE)

    # Aktualizuj dane na wykresie
    line.set_data(freqs, fft_magnitude)
    return line,

# Tworzenie figury Matplotlib
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_title("Widmo Fouriera sygnału audio")
ax.set_xlabel("Częstotliwość [Hz]")
ax.set_ylabel("Amplituda")

# Tworzenie animacji
ani = FuncAnimation(fig, update, init_func=init_plot, blit=True, interval=50)

# Wyświetlenie wykresu
print("Rozpoczęto analizę widma (zamknij okno wykresu, aby zakończyć)")
plt.show()

# Sprzątanie po zakończeniu
stream.stop_stream()
stream.close()
audio.terminate()
