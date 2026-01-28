from pygame import midi
from pygame.midi import Output

midi.init()


def create_midi_output() -> Output:
    return midi.Output(midi.get_default_output_id())
