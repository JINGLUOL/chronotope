from util.soundfont import create_midi_output

midi_output = create_midi_output()


class PianoSound:

    def __init__(self, key_midi: int):
        self.key_midi = key_midi
        self.velocity = 0
        self.start_time = 0
        self.stop_time = 0
        pass

    def play(self, start_time: int, velocity: int):
        self.start_time = start_time
        self.stop_time = start_time + 3000
        self.velocity = velocity
        midi_output.note_on(self.key_midi, self.velocity)
        pass

    def set_stop_time(self, stop_time: int):
        self.stop_time = stop_time + max(stop_time - self.start_time, 150)
        pass

    def terminate(self, current_time: int):
        if self.is_terminated(current_time):
            midi_output.note_off(self.key_midi)
            pass
        pass

    def is_terminated(self, current_time: int) -> bool:
        return self.stop_time <= current_time

    pass
