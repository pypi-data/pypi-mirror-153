from Instrument import Instrument
import matplotlib.pyplot as plt

if __name__ == '__main__':
    piano = Instrument()
    # 40 42 44 45 47
    # C  D  E  F  G

    # Ode to Joy
    for _ in range(2):
        for _ in range(2):
            piano.record_key(44, 0.5)
        piano.record_key(45, 0.5)
        for _ in range(2):
            piano.record_key(47, 0.5)
        piano.record_key(44, 0.5)
        piano.record_key(42, 0.5)

        for _ in range(2):
            piano.record_key(40, 0.5)
        piano.record_key(42, 0.5)
        piano.record_key(44, 0.5)
        piano.record_key(44, 0.3)
        piano.record_key(42, 0.2)
        piano.record_key(42, 0.8)

        for _ in range(2):
            piano.record_key(44, 0.5)
        piano.record_key(45, 0.5)
        for _ in range(2):
            piano.record_key(47, 0.5)
        piano.record_key(44, 0.5)
        piano.record_key(42, 0.5)

        for _ in range(2):
            piano.record_key(40, 0.5)
        piano.record_key(42, 0.5)
        piano.record_key(44, 0.5)
        piano.record_key(44, 0.3)
        piano.record_key(40, 0.2)
        piano.record_key(40, 0.8)

        piano.record_key(42, 0.5)
        piano.record_key(42, 0.5)
        piano.record_key(44, 0.5)
        piano.record_key(40, 0.5)

        piano.record_key(42, 0.5)
        piano.record_key(44, 0.2)
        piano.record_key(45, 0.2)
        piano.record_key(44, 0.5)
        piano.record_key(40, 0.5)

        piano.record_key(42, 0.5)
        piano.record_key(44, 0.25)
        piano.record_key(45, 0.25)
        piano.record_key(44, 0.5)
        piano.record_key(42, 0.5)

        piano.record_key(40, 0.5)
        piano.record_key(42, 0.5)
        piano.record_key(35, 0.5)
        piano.record_key(40, 0.5)
        piano.record_key(42, 0.5)

    # # piano.play()
    # piano.clear_sample()

    # # for _ in range(8):
    # #     piano.record_chord([(52, 56, 61)], 0.3)
    # for _ in range(3):
    #     piano.record_chord([(51, 56, 61)], 0.3)
    # # for _ in range(5):
    # #     piano.record_chord([(51, 56, 59)], 0.3)

    piano.play()

    key_colors = {40: ["red", 1], 42: ["blue", 1], 44: ["green", 1], 45: ["gray", 1],
                  47: ["orange", 1], 35: ["purple", 1], ((51, 56, 61),): ['black', 1]}

    for key, time, wave in piano.graphing_sample:
        if key_colors[key][1]:
            plt.plot(time, wave, label=key, color=key_colors[key][0])
            key_colors[key][1] = 0
        else:
            plt.plot(time, wave, color=key_colors[key][0])

    plt.show()

    piano.close()
