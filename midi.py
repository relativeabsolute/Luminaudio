import math

class Midi:
    # note: this will only work for 4-byte values, but that's all midi can store anyway
    def get_var_length_qty(value):
        byte_count = math.ceil(value.bit_length() / 7)
        result = 0
        #print("original value = {}".format(bin(value)))
        for i in range(byte_count):
            current_value = (value & (0x7F << (i * 7))) >> (i * 7)
            #print("byte {} = {:02x}".format(i, current_value))
            result |= (current_value | ((i > 0) << 7)) << (i * 8)
            #print("current result value = {:x}".format(result))
        return result

    # return the number of bytes in a variable length quantity
    def length_of_var_length_qty(value):
        return math.ceil(value.bit_length() / 8)

    class HeaderChunk:
        def __init__(self):
            self.chunk_type = 'MThd'
            self.length = 6
            self.format = 0 # single multi-channel track for now
            self.ntrks = 1 # always 1 for a format 0 file
            self.division = 3 << 8 # not sure about this one
        def write_to_file(self, file_name):
            with open(file_name, 'wb') as header_file_writer:
                header_file_writer.write(self.chunk_type.encode())
                header_file_writer.write(self.length.to_bytes(4, 'big'))
                header_file_writer.write(self.format.to_bytes(2, 'big'))
                header_file_writer.write(self.ntrks.to_bytes(2, 'big'))
                header_file_writer.write(self.division.to_bytes(2, 'big'))
                header_file_writer.flush()
    class TrackChunk:
        class Event:
            # blank values to initialize
            def __init__(self):
                self.delta_time = 0
                self.evt_desc = [0, 0, 0]

        def __init__(self):
            self.chunk_type = 'MTrk'
            # TODO: update length of chunk with events
            self.length = 0
            self.events = []

        def add_event(self, note_on_off, channel_num, note_num, key_velocity, dt):
            evt = self.Event()
            evt.delta_time = dt
            # TODO: ensure note_num and key_velocity are 7 bits each
            evt.evt_desc = [((0b1000 | note_on_off) << 4) | channel_num, note_num, key_velocity]
            self.events.append(evt)
    
        def write_to_file(self, file_name):
            with open(file_name, 'ab') as track_file_writer:
                track_file_writer.write(self.chunk_type.encode())
                track_file_writer.write(self.length.to_bytes(4, 'big'))
                prev_status = 0
                for evt in self.events:
                    dt = Midi.get_var_length_qty(evt.delta_time)
                    track_file_writer.write(dt.to_bytes(Midi.length_of_var_length_qty(dt), 'big'))
                    start_index = 0
                    if evt.evt_desc[0] == prev_status:
                        start_index = 1
                    track_file_writer.write(bytes(evt.evt_desc[start_index:]))
                track_file_writer.flush()

    def __init__(self):
        self.chunks = [self.HeaderChunk()]

    def write_to_file(self, file_name):
        for chunk in self.chunks:
            chunk.write_to_file(file_name)
