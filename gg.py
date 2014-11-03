import random
from sys import exit


class Game(object):
    def __init__(self):
        self.pieces = {'5SG': 1, '4SG': 1, '3SG': 1, '2SG': 1, '1SG': 1,
                       'COL': 1, 'LTC': 1, 'MAJ': 1, 'CAP': 1, '1LT': 1, '2LT': 1,
                       'SRG': 1, 'PVT': 6, 'SPY': 2, 'FLG': 1}
        self.slot_code = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                          'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
                          'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                          'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9',
                          'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',
                          'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                          'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
                          'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9']

        self.comp_pieces = ['5SG', '4SG', '3SG', '2SG', '1SG',
                            'COL', 'LTC', 'MAJ', 'CAP', '1LT', '2LT', 'SRG',
                            'PVT', 'PVT', 'PVT', 'PVT', 'PVT', 'PVT',
                            'SPY', 'SPY', 'FLG']
        self.squares = []
        self.record_squares = []
        for i in range(72):
            i = '[---]'
            self.squares.append(i)
            self.record_squares.append(i)

        self.update()
        self.setup()

    def setup(self):
        no_of_pieces = sum(self.pieces.values())
        while no_of_pieces != 0:
            print self.pieces
            piece = raw_input('Pick a piece: ')
            if piece in self.pieces and self.pieces[piece] != 0:
                slot = raw_input('Pick a slot (F1-H9): ')
                if slot in self.slot_code:
                    conv_slot = self.slot_code.index(slot)
                    if conv_slot > self.slot_code.index('E9') and self.squares[conv_slot] == '[---]':
                        self.squares[conv_slot] = '[' + piece + ']'
                        no_of_pieces -= 1
                        self.pieces[piece] -= 1
                        self.update()
                        if self.pieces[piece] == 0:
                            del self.pieces[piece]
                    else:
                        print 'Choice out of range or already occupied'
                        self.update()
                else:
                    print 'Choice not available'
                    self.update()
            else:
                print 'Choice not available'
                self.update()
                
        self.comp_setup()

    def comp_setup(self):
        comp_piece_ind = range(21)
        random.shuffle(comp_piece_ind)
        comp_slot_ind = range(27)
        random.shuffle(comp_slot_ind)

        no_of_comp_piece = 21
        y = 0
        while no_of_comp_piece != 0:
            comp_pick = self.comp_pieces[comp_piece_ind[y]]
            self.squares[comp_slot_ind[y]] = '[XXX]'
            self.record_squares[comp_slot_ind[y]] = '[' + comp_pick + ']'
            no_of_comp_piece -= 1
            y += 1

            self.update()

        self.move()

    def move(self):
        while True:
            choose = raw_input('Pick the slot with the piece you want to move:  ')
            if choose in self.slot_code:
                conv_choose = self.slot_code.index(choose)
                if self.squares[conv_choose] != '[---]' and self.squares[conv_choose] != '[XXX]':
                    avail_moves = []
                    avail_index = []
                    addends = [9, -18, 10, -2]
                    a = conv_choose
                    if conv_choose in [0, 9, 18, 27, 36, 45, 54, 63]:
                        addends = [9, -18, 10]
                    elif conv_choose in [8, 17, 26, 35, 44, 53, 62, 71]:
                        addends = [9, -18, 8]

                    for i in range(len(addends)):
                        a += addends[i]
                        avail_index.append(a)
                        for j in avail_index:
                            if 0 > j or j > 71:
                                avail_index.remove(j)

                    for k in avail_index:
                        avail_moves.append(self.slot_code[k])

                    move_to = raw_input('Pick a slot you want to move the piece: ')
                    if move_to in avail_moves:
                        conv_move_to = self.slot_code.index(move_to)
                        if self.squares[conv_move_to] == '[---]':
                            self.squares[conv_move_to] = self.squares[conv_choose]
                            self.squares[conv_choose] = '[---]'
                            if '[FLG]' in self.squares[0:9]:
                                print 'Winner: You'
                                exit(1)
                            else:
                                self.update()
                                break

                        elif self.squares[conv_move_to] == '[XXX]':
                            print 'SALPAKAN NA!'
                            self.salpakan('You', self.squares[conv_choose], self.record_squares[conv_move_to],
                                          conv_choose, conv_move_to)

                        else:
                            print 'Choice already occupied'
                            self.update()
                    else:
                        print 'Choice not available'
                        self.update()
                else:
                    print 'Choice already occupied'
                    self.update()
            else:
                print 'Choice is empty or occupied by opponent'
                self.update()

        self.comp_move()

    def comp_move(self):
        choose = random.randint(0, 71)
        if self.squares[choose] == '[XXX]':
            avail_moves = []
            addends = [9, -18, 10, -2]
            a = choose
            if choose in [0, 9, 18, 27, 36, 45, 54, 63]:
                addends = [9, -18, 10]
            elif choose in [8, 17, 26, 35, 44, 53, 62, 71]:
                addends = [9, -18, -2]
            for i in range(len(addends)):
                a += addends[i]
                avail_moves.append(a)
                for j in avail_moves:
                    if 0 > j or j > 71:
                        avail_moves.remove(j)

            move_to = avail_moves[random.randint(0, len(avail_moves) - 1)]
            if self.squares[move_to] == '[---]':
                self.squares[move_to] = '[XXX]'
                self.squares[choose] = '[---]'
                self.record_squares[move_to] = self.record_squares[choose]
                self.record_squares[choose] = '[---]'
                if '[FLG]' in self.record_squares[63:72]:
                    print 'Winner: Computer'
                    exit(1)
                else:
                    self.update()

            elif self.squares[move_to] != '[---]' and self.squares[move_to] != '[XXX]':
                print 'SALPAKAN NA!'
                self.salpakan('Computer', self.record_squares[choose], self.squares[move_to], choose, move_to)

            else:
                self.comp_move()
        else:
            self.comp_move()

        self.move()

    def salpakan(self, challenger, my_piece, your_piece, my_pos, your_pos):
        kill_list = {'[5SG]': ['[4SG]', '[3SG]', '[2SG]', '[1SG]', '[COL]', '[LTC]',
                               '[MAJ]', '[CAP]', '[1LT]', '[2LT]', '[SRG]', '[PVT]'],
                     '[4SG]': ['[3SG]', '[2SG]', '[1SG]', '[COL]', '[LTC]', '[MAJ]',
                               '[CAP]', '[1LT]', '[2LT]', '[SRG]', '[PVT]'],
                     '[3SG]': ['[2SG]', '[1SG]', '[COL]', '[LTC]', '[MAJ]',
                               '[CAP]', '[1LT]', '[2LT]', '[SRG]', '[PVT]'],
                     '[2SG]': ['[1SG]', '[COL]', '[LTC]', '[MAJ]', '[CAP]',
                               '[1LT]', '[2LT]', '[SRG]', '[PVT]'],
                     '[1SG]': ['[COL]', '[LTC]', '[MAJ]', '[CAP]',
                               '[1LT]', '[2LT]', '[SRG]', '[PVT]'],
                     '[COL]': ['[LTC]', '[MAJ]', '[CAP]', '[1LT]', '[2LT]', '[SRG]', '[PVT]'],
                     '[LTC]': ['[MAJ]', '[CAP]', '[1LT]', '[2LT]', '[SRG]', '[PVT]'],
                     '[MAJ]': ['[CAP]', '[1LT]', '[2LT]', '[SRG]', '[PVT]'],
                     '[CAP]': ['[1LT]', '[2LT]', '[SRG]', '[PVT]'],
                     '[1LT]': ['[2LT]', '[SRG]', '[PVT]'],
                     '[2LT]': ['[SRG]', '[PVT]'],
                     '[SRG]': ['[PVT]'],
                     '[PVT]': ['[SPY]'],
                     '[SPY]': ['[5SG]', '[4SG]', '[3SG]', '[2SG]', '[1SG]', '[COL]',
                               '[LTC]', '[MAJ]', '[CAP]', '[1LT]', '[2LT]', '[SRG]']}

        if your_piece == '[FLG]':
            print 'Winner: ' + challenger
            exit(1)

        elif my_piece == '[FLG]':
            if challenger == 'You':
                print 'Winner: Computer'
                exit(1)
            else:
                print 'Winner: You'
                exit(1)

        elif my_piece == '[FLG]' and your_piece == '[FLG]':
            print 'Winner: ' + challenger
            exit(1)

        else:
            if your_piece == my_piece:
                self.squares[my_pos] = '[---]'
                self.squares[your_pos] = '[---]'
                self.record_squares[my_pos] = '[---]'
                self.record_squares[your_pos] = '[---]'
            else:
                if your_piece in kill_list[my_piece]:
                    if challenger == 'You':
                        self.squares[your_pos] = self.squares[my_pos]
                        self.squares[my_pos] = '[---]'
                        self.record_squares[your_pos] = '[---]'
                    elif challenger == 'Computer':
                        self.squares[your_pos] = '[XXX]'
                        self.squares[my_pos] = '[---]'
                        self.record_squares[your_pos] = self.record_squares[my_pos]
                        self.record_squares[my_pos] = '[---]'
                elif your_piece not in kill_list[my_piece]:
                    self.squares[my_pos] = '[---]'
                    self.record_squares[my_pos] = '[---]'

        self.update()

    def update(self):
	
        print 'A' + ''.join(self.squares[0:9])
        print 'B' + ''.join(self.squares[9:18])
        print 'C' + ''.join(self.squares[18:27])
        print 'D' + ''.join(self.squares[27:36])
        print 'E' + ''.join(self.squares[36:45])
        print 'F' + ''.join(self.squares[45:54])
        print 'G' + ''.join(self.squares[54:63])
        print 'H' + ''.join(self.squares[63:72])
        print '   1    2    3    4    5    6    7    8    9'


Game()
