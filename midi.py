class Midi:
    class HeaderChunk:
        def __init__(self):
            self.chunk_type = 'MThd'
            self.length = 6
            self.format = 0 # single multi-channel track for now
            self.ntrks = 1 # always 1 for a format 0 file
            self.division = 3 << 8 # not sure about this one
        def write_to_file(self, file_name):
            with open(file_name, 'wb') as file_object:
                file_object.write(self.chunk_type.encode())
                file_object.write(self.length.to_bytes(4, 'big'))
                file_object.write(self.format.to_bytes(2, 'big'))
                file_object.write(self.ntrks.to_bytes(2, 'big'))
                file_object.write(self.division.to_bytes(2, 'big'))
                file_object.flush()
    class TrackChunk:
        class Event:
            # blank values to initialize
            def __init__(self):
                self.delta_time = 0
                self.event = [0, 0, 0]

        def __init__(self):
            self.chunk_type = 'MTrk'
            self.length = 0
            self.events = []

        def add_event(self, note_on_off, channel_num, note_num, key_velocity, dt):
            evt = self.Event()
            evt.delta_time = dt
            # TODO: ensure note_num and key_velocity are 7 bits each
            evt.event = [((8 | note_on_off) << 4) | channel_num, note_num, key_velocity]
            self.events.append(evt)
    
        def write_to_file(self, file_name):
            with open(file_name, 'ab') as file_object:
                file_object.write(self.chunk_type.encode())
                file_object.write(self.length.to_bytes(4, 'big'))
                for evt in self.events:
                    # TODO: figure out writing variable length quantities (which a delta time is)

    def __init__(self):
        self.chunks = [self.HeaderChunk()]

    def write_to_file(self, file_name):
        for chunk in self.chunks:
            chunk.write_to_file(file_name)
