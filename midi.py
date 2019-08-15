from debug import debug_print
import math


class Midi:
    # note: this will only work for 4-byte values, but that's all midi can store anyway
    def get_var_length_qty(value):
        byte_count = math.ceil(value.bit_length() / 7)
        result = 0
        #print("original value = {}".format(bin(value)))
        for i in range(byte_count):
            current_value = (value & (0x7F << (i * 7))) >> (i * 7)
            result |= (current_value | ((i > 0) << 7)) << (i * 8)
        return result


    # return the number of bytes in a variable length quantity
    def length_of_var_length_qty(value):
        return max(math.ceil(value.bit_length() / 8), 1)


    class HeaderChunk:
        # default to 960 ticks per quarter note
        def __init__(self, ticks_per_quarter = 960):
            self.chunk_type = 'MThd'
            self.length = 6
            self.format = 0 # single multi-channel track for now
            self.ntrks = 1 # always 1 for a format 0 file
            self.division = ticks_per_quarter


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


        def __init__(self, ticks_per_qtr_note):
            self.ticks_per_qtr_note = ticks_per_qtr_note
            self.chunk_type = 'MTrk'
            self.length = 0
            self.events = []


        def add_event(self, note_on_off, channel_num, note_num, key_velocity, dt):
            evt = self.Event()
            evt.delta_time = dt
            # TODO: ensure note_num and key_velocity are 7 bits each
            dt_var_len = Midi.get_var_length_qty(dt)
            len_dt_var_len = Midi.length_of_var_length_qty(dt_var_len)
            self.length += Midi.length_of_var_length_qty(Midi.get_var_length_qty(dt))
            evt.evt_desc = [((0b1000 | note_on_off) << 4) | channel_num, note_num, key_velocity]
            evt_len = len(evt.evt_desc)
            
            # if the status byte of this event is the same as the last one we don't need to write it
            if self.events:
                evt_len -= evt.evt_desc[0] == self.events[len(self.events) - 1].evt_desc[0]
            self.length += evt_len
            self.events.append(evt)

    
        def write_to_file(self, file_name):
            with open(file_name, 'ab') as track_file_writer:
                # TODO: allow other time sigs than 4/4
                #notes_off_dt = self.ticks_per_qtr_note * 3
                notes_off_dt = 0 # end the track when there are no more midi notes
                notes_off_dt = Midi.get_var_length_qty(notes_off_dt)
                # +7 is for the data of the notes off event and the track end event
                self.length += Midi.length_of_var_length_qty(notes_off_dt) + 7
                track_file_writer.write(self.chunk_type.encode())
                track_file_writer.write(self.length.to_bytes(4, 'big'))
                prev_status = 0
                dt_total = 0
                for evt in self.events:
                    dt = Midi.get_var_length_qty(evt.delta_time)
                    dt_total += evt.delta_time
                    track_file_writer.write(dt.to_bytes(Midi.length_of_var_length_qty(dt), 'big'))
                    start_index = 0
                    if evt.evt_desc[0] == prev_status:
                        start_index = 1
                    track_file_writer.write(bytes(evt.evt_desc[start_index:]))
                # write all notes off control change event
                track_file_writer.write(notes_off_dt.to_bytes(Midi.length_of_var_length_qty(notes_off_dt), 'big'))
                track_file_writer.write(bytes([0xB0, 0x7B, 0x00]))
                # need to end with a track end event
                track_file_writer.write(bytes([0x00, 0xFF, 0x2F, 0x00]))
                track_file_writer.flush()


    def __init__(self, ticks_per_quarter = 960):
        self.chunks = [self.HeaderChunk(ticks_per_quarter)]


    def write_to_file(self, file_name):
        for chunk in self.chunks:
            chunk.write_to_file(file_name)
