import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


def plot_signals(file1, file2):
    """
    Wczytuje dwa pliki dźwiękowe i wyświetla wykresy amplitudy oraz widma częstotliwości.

    Parameters:
        file1 (str): Ścieżka do pierwszego pliku (oryginalny dźwięk).
        file2 (str): Ścieżka do drugiego pliku (przefiltrowany dźwięk).
    """
    # Wczytaj dane audio z obu plików
    data1, samplerate1 = sf.read(file1)
    data2, samplerate2 = sf.read(file2)

    # Sprawdź, czy częstotliwości próbkowania są zgodne
    if samplerate1 != samplerate2:
        raise ValueError("Częstotliwości próbkowania obu plików muszą być takie same.")

    # Obsługa plików stereo: konwertuj na mono, jeśli jest potrzebne
    if len(data1.shape) > 1:
        data1 = data1.mean(axis=1)
    if len(data2.shape) > 1:
        data2 = data2.mean(axis=1)

    # Tworzenie osi czasu
    time1 = np.linspace(0, len(data1) / samplerate1, len(data1))
    time2 = np.linspace(0, len(data2) / samplerate2, len(data2))

    # Obliczanie FFT (widma częstotliwości)
    fft1 = np.fft.rfft(data1)
    fft2 = np.fft.rfft(data2)
    freq1 = np.fft.rfftfreq(len(data1), 1 / samplerate1)
    freq2 = np.fft.rfftfreq(len(data2), 1 / samplerate2)

    # Normalizacja amplitudy FFT
    fft1_magnitude = np.abs(fft1) / len(data1)
    fft2_magnitude = np.abs(fft2) / len(data2)

    # Rysowanie wykresów
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # Wykresy amplitudy w dziedzinie czasu
    axs[0, 0].plot(time1, data1, label="Oryginalny")
    axs[0, 0].set_title("Amplituda (oryginalny)")
    axs[0, 0].set_xlabel("Czas [s]")
    axs[0, 0].set_ylabel("Amplituda")

    axs[0, 1].plot(time2, data2, label="Przefiltrowany", color="orange")
    axs[0, 1].set_title("Amplituda (przefiltrowany)")
    axs[0, 1].set_xlabel("Czas [s]")
    axs[0, 1].set_ylabel("Amplituda")

    # Wykresy widma częstotliwości
    axs[1, 0].plot(freq1, fft1_magnitude, label="Oryginalny")
    axs[1, 0].set_title("Widmo częstotliwości (oryginalny)")
    axs[1, 0].set_xlabel("Częstotliwość [Hz]")
    axs[1, 0].set_ylabel("Amplituda")

    axs[1, 1].plot(freq2, fft2_magnitude, label="Przefiltrowany", color="orange")
    axs[1, 1].set_title("Widmo częstotliwości (przefiltrowany)")
    axs[1, 1].set_xlabel("Częstotliwość [Hz]")
    axs[1, 1].set_ylabel("Amplituda")

    # Dostosowanie układu i wyświetlenie
    plt.tight_layout()
    plt.show()


def main():
    # Wprowadzenie plików audio
    file1 = input("Podaj ścieżkę do oryginalnego pliku audio (np. 'plik.wav'): ").strip()
    file2 = input("Podaj ścieżkę do przefiltrowanego pliku audio (np. 'filtered_plik.wav'): ").strip()

    plot_signals(file1, file2)


if __name__ == "__main__":
    main()
