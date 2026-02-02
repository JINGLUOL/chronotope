from util.soundfont import create_midi_output

midi_output = create_midi_output()


class PianoSound:

    def __init__(self, key_midi: int):
        self.key_midi = key_midi
        self.velocity = 0
        self.sustain = 0
        self.start_time = 0
        self.stop_time = 0
        pass

    def play(self, start_time: int, velocity: int, sustain: int):
        self.start_time = start_time
        self.stop_time = start_time + 10000
        self.velocity = velocity
        self.sustain = sustain
        midi_output.note_on(self.key_midi, self.velocity)
        pass

    def set_stop_time(self, stop_time: int):
        self.stop_time = stop_time + max(stop_time - self.start_time, 150) + self.sustain
        pass

    def terminate(self, current_time: int) -> bool:
        if self.stop_time <= current_time:
            midi_output.note_off(self.key_midi)
            return True
        return False

    pass
