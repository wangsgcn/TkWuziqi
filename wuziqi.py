class Wuziqi:
    def __init__(self, game_size=19):
        self.size = game_size
        self.end_game_flag = False
        self.opp_color = {1:2, 2:1} # dictionary for opponent color id

        # board: 0-> empty, 1-> human, 2-> computer
        self.board = [[0 for i in range(self.size)] for j in range(self.size)]

        # scores for different situations
        self.connected_5_pts = 20000
        self.open_4_pts = 20000
        self.double_3_pts = 10000
        self.closed_4_pts = 2000
        self.open_3_pts =  2000
        self.closed_3_pts = 20
        self.open_2_pts = 2
        self.closed_2_pts = 1
        self.player_penalty = 10.0

        # catch for the minimax search algorithm
        # key: board code
        # value: board score 
        self.minimax_records = {}
        self.computer_color = 2  # white color
        self.player_color = 1  # black color

    def print_board(self):
        line="    "
        for col in range(self.size):
            line += "%3d" %(col)
        print(line)
        line="     "
        for col in range(self.size):
            line += "---"
        print(line)
        for row in range(self.size):
            line = "%02d | " %row
            for col in range(self.size):
                line +=  " " + str(self.board[row][col]) + " "
            print(line)
        # print("")

    def count_five(self, color_id):
        a = color_id
        count = 0
        #  a a a a a
        #  -          (-) represent the current point to check
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != a:
                    continue
                # horizontal direction
                if self.inside([(r,c+4)]) and self.check([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4)],[a,a,a,a,a]):
                    count += 1
                # vertical direction
                if self.inside([(r+4,c)]) and self.check([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c)], [a,a,a,a,a]):
                    count += 1
                # upper right diagonal direction
                if self.inside([(r-4,c+4)]) and self.check([(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3),(r-4,c+4)], [a,a,a,a,a]):
                    count += 1
                # lower right diagonal direction
                if self.inside([(r+4,c+4)]) and self.check([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4)], [a,a,a,a,a]):
                    count +=1
        return count

    def count_open_four(self, color_id):
        a = color_id
        count = 0
        # 0 a a a a 0
        for r in range(self.size):
            for c in range(self.size):
                # if the current point is already taken by either computer or player, no need to check
                if self.board[r][c] != 0:
                    continue
                # horizontal direction
                if self.inside([(r,c+4)]) and self.check([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4)],[0,a,a,a,a,0]):
                    count += 1
                # vertical direction
                if self.inside([(r+4,c)]) and self.check([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c)], [0,a,a,a,a,0]):
                    count += 1
                # upper right diagonal direction
                if self.inside([(r-4,c+4)]) and self.check([(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3),(r-4,c+4)], [0,a,a,a,a,0]):
                    count += 1
                # lower right diagonal direction
                if self.inside([(r+4,c+4)]) and self.check([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4)], [0,a,a,a,a,0]):
                    count += 1
        return count

    def count_closed_four(self, color_id):
        a = color_id             # current color to check
        b = self.opp_color[a]    # opponent color
        count = 0
        #0 a a a a b
        #b a a a a 0
        for r in range(self.size):
            for c in range(self.size):
                # if the current point is taken by color a, then continue. The algorithm only checks 0 or b for possible closed four.
                if self.board[r][c]==a:
                    continue
                # horizontal direction
                if self.inside([(r,c+5)]) and (self.check([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4),(r,c+5)], [0,a,a,a,a,b])\
                                            or self.check([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4),(r,c+5)], [b,a,a,a,a,0])):
                    count += 1
                # vertical direction
                if self.inside([(r+5,c)]) and (self.check([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c),(r+5,c)], [0,a,a,a,a,b]) \
                                            or self.check([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c),(r+5,c)], [b,a,a,a,a,0])):
                    count += 1
                # upper right diagonal direction
                if self.inside([(r-5,c+5)]) and (self.check([(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3),(r-4,c+4),(r-5,c+5)], [0,a,a,a,a,b]) \
                                              or self.check([(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3),(r-4,c+4),(r-5,c+5)], [b,a,a,a,a,0])):
                    count += 1
                # lower right diagonal direction
                if self.inside([(r+5,c+5)]) and (self.check([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4),(r+5,c+5)],[0,a,a,a,a,b]) \
                                              or self.check([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4),(r+5,c+5)],[b,a,a,a,a,0])):
                    count += 1
        return count

    def count_open_three(self, color_id):
        count = 0
        a = color_id # current cor to check
        for r in range(self.size):
            for c in range(self.size):
                # 0 * * * 0 (r, c), (r, c+4)
                if self.inside([(r,c+4)]) and self.check([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4)], [0,a,a,a,0]):
                    count += 1
                # column, (r, c) -> (r+4, c)
                if self.inside([(r+4,c)]) and self.check([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c)], [0,a,a,a,0]):
                    count += 1
                # upper right diagonal (r, c) -> (r-4,c+4)
                if self.inside([(r-4,c+4)]) and self.check([(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3),(r-4,c+4)], [0,a,a,a,0]):
                    count += 1
                # lower right diagonal (r, c) => (r+4, c+4)
                if self.inside([(r+4,c+4)]) and self.check([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4)], [0,a,a,a,0]):
                    count += 1
        return count

    def count_closed_three(self, color_id):
        a = color_id
        b = self.opp_color[a]
        count = 0
        # b a a a 0 0
        # 0 0 a a a b
        # -           (-) current point
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == a:
                    continue
                # horizontal direction
                if self.inside([(r,c+4)]) and (self.check([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4),(r,c+5)], [b,a,a,a,0,0])\
                                            or self.check([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4),(r,c+5)], [0,0,a,a,a,b])):
                    count += 1
                # vertical direction
                if self.inside([(r+4,c)]) and (self.check([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c),(r+5,c)], [b,a,a,a,0,0])\
                                            or self.check([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c),(r+5,c)], [0,0,a,a,a,b])):
                    count += 1
                # upper right diagonal direction
                if self.inside([(r-4,c+4)]) and (self.check([(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3),(r-4,c+4),(r-5,c+5)], [b,a,a,a,0,0])\
                                              or self.check([(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3),(r-4,c+4),(r-5,c+5)], [0,0,a,a,a,b])):
                    count += 1
                # lower right diagonal direction
                if self.inside([(r+4,c+4)]) and (self.check([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4),(r+5,c+5)], [b,a,a,a,0,0])\
                                              or self.check([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4),(r+5,c+5)], [0,0,a,a,a,b])):
                    count += 1
        return count

    def count_closed_two(self, color_id):
        a = color_id
        b = self.opp_color[a]
        count = 0
        # closed cases
        # b a a 0 0 0
        # 0 0 0 a a b
        # -             current point to check
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == a:
                    continue
                # horizontal direction
                if self.inside([(r,c+5)]) and (self.check([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4),(r,c+5)], [b,a,a,0,0,0])\
                                            or self.check([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4),(r,c+5)], [0,0,0,a,a,b])):
                    count += 1
                # vertical direction
                if self.inside([(r+5,c)]) and (self.check([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c),(r+5,c)], [b,a,a,0,0,0])\
                                            or self.check([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c),(r+5,c)], [0,0,0,a,a,b])):
                    count += 1
                # upper right diagonal direction
                if self.inside([(r-5,c+5)]) and (self.check([(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3),(r-4,c+4),(r-5,c+5)], [b,a,a,0,0,0])\
                                              or self.check([(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3),(r-4,c+4),(r-5,c+5)], [0,0,0,a,a,b])):
                    count += 1
                # lower right diagonal direction
                if self.inside([(r+5,c+5)]) and (self.check([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4),(r+5,c+5)], [b,a,a,0,0,0])\
                                              or self.check([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4),(r+5,c+5)], [0,0,0,a,a,b])):
                    count += 1
        return count

    def count_open_two(self, color_id):
        # only two situations of open two are considered for computational efficiency
        a = color_id
        count = 0
        for r in range(self.size):
            for c in range(self.size):
                # 0 0 a a 0
                # 0 a a 0 0
                if self.board[r][c] != 0:
                    continue
                # horizontal direction
                if self.inside([(r,c+4)]) and (self.check([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4)], [0,0,a,a,0]) \
                                           or  self.check([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4)], [0,a,a,0,0])):
                    count += 1
                # vertical direction
                if self.inside([(r+4,c)]) and (self.check([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c)], [0,0,a,a,0]) \
                                           or  self.check([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c)], [0,a,a,0,0])):
                    count += 1
                # upper right diagonal direction
                if self.inside([(r-4,c+4)]) and (self.check([(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3),(r-4,c+4)], [0,0,a,a,0]) \
                                             or self.check([(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3),(r-4,c+4)], [0,a,a,0,0])):
                    count += 1
                # lower right diagonal direction
                if self.inside([(r+4,c+4)]) and (self.check([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4)], [0,0,a,a,0]) \
                                              or self.check([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4)], [0,a,a,0,0])):
                    count += 1
        return count

    def winning_position(self, color_id):
        a = color_id
        for r in range(self.size):
            for c in range(self.size):
                for offset in range(0, 5):
                    others = list(filter(lambda x: x != offset, [0, 1, 2, 3, 4]))
                    o0, o1, o2, o3 = others[0], others[1], others[2], others[3]
                    # horizontal direction
                    if self.inside([(r,c+4)]) and self.check([(r,c+offset),(r,c+o0),(r,c+o1),(r,r+o2),(r,c+o3)], [0,a,a,a,a]):
                        return r, c+offset
                    # vertical direction
                    if self.inside([(r+4,c)]) and self.check([(r+offset,c),(r+o0,c),(r+o1,c),(r+o2,c),(r+o3,c)], [0,a,a,a,a]):
                        return r+offset, c
                    # upper right diagonal direction
                    if self.inside([(r-4,c+4)]) and self.check([(r-offset,c+offset),(r-o0,c+o0),(r-o1,c+o1),(r-o2,c+o2),(r-o3,c+o3)], [0,a,a,a,a]):
                        return r-offset, c+offset
                    # lower right diagonal direction
                    if self.inside([(r+4,c+4)]) and self.check([(r+offset,c+offset),(r+o0,c+o0),(r+o1,c+o1),(r+o2,c+o2),(r+o3,c+o3)], [0,a,a,a,a]):
                        return r+offset, c+offset
        return  -1, -1 # no winining position

    def game_over(self):
        for r in range(self.size):
            for c in range(self.size):
                for x in [self.computer_color, self.player_color]:
                    # horizontal direction
                    if self.inside([(r,c+4)]) and self.check([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4)],[x,x,x,x,x]):
                        return x
                    # vertical direction
                    if self.inside([(r+4,r)]) and self.check([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c)], [x,x,x,x,x]):
                        return x
                    # upper right direction
                    if self.inside([(r-4,c+4)]) and self.check([(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3),(r-4,c+4)], [x,x,x,x,x]):
                        return x
                    # lower right direction
                    if self.inside([(r+4,c+4)]) and self.check([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4)], [x,x,x,x,x]):
                        return x
        return -1 # game is not over yet.


    def nearby_moves(self, buffer_size=1):
        nearby_row_col = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] > 0:
                    row_max = min(row + buffer_size+1, self.size)
                    col_max = min(col + buffer_size+1, self.size)
                    row_min = max(row - buffer_size, 0)
                    col_min = max(col - buffer_size, 0)

                    for r in range(row_min, row_max):
                        for c in range(col_min, col_max):
                            if self.board[r][c] == 0 and (r, c) not in nearby_row_col:
                                nearby_row_col.append((r, c))
        return nearby_row_col

    def nearby_moves2(self):
        nearby_row_col = [[False for i in range(self.size)] for j in range(self.size)]
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] > 0:
                    row_max = min(row + 1, self.size)
                    col_max = min(col + 1, self.size)
                    row_min = max(row - 1, 0)
                    col_min = max(col - 1, 0)

                    for r in range(row_min, row_max + 1):
                        for c in range(col_min, col_max + 1):
                            nearby_row_col[r][c] = True

        return nearby_row_col

    def board_string_code(self):
        string_code = ""
        for row in range(self.size):
            for col in range(self.size):
                string_code += str(self.board[row][col])
        return string_code

    def evaluate_board_score2(self):
        computer_connected_five = self.count_five(self.computer_color)
        player_connected_five = self.count_five(self.player_color)

        computer_open_four = self.count_open_four(self.computer_color)
        player_open_four = self.count_open_four(self.player_color)

        computer_open_three = self.count_open_three(self.computer_color)
        player_open_three = self.count_open_three(self.player_color)

        computer_open_two = self.count_open_two(self.computer_color)
        player_open_two = self.count_open_two(self.player_color)

        computer_closed_four = self.count_closed_four(self.computer_color) - computer_open_four
        player_closed_four = self.count_closed_four(self.player_color) - player_open_four

        computer_closed_three = self.count_closed_three(self.computer_color) - computer_open_three
        player_closed_three = self.count_closed_three(self.player_color) - player_open_three

        computer_closed_two = self.count_closed_two(self.computer_color) - computer_open_two
        player_closed_two = self.count_closed_two(self.player_color) - player_open_two

        score = 6000 * (computer_connected_five - player_connected_five)
        + 4800 * (computer_open_four - player_open_four)
        + 500 * (computer_closed_four - player_closed_four)
        + 500 * (computer_open_three - player_open_three)
        + 200 * (computer_closed_three - player_closed_three)
        + 50 * (computer_open_two - player_open_two)
        + 10 * (computer_closed_two - player_closed_two)

        return score

    def get_move_greedy(self):
        # check the wining positions
        computer_win_row, computer_win_col = self.winning_position(self.computer_color)
        player_win_row, player_win_col = self.winning_position(self.player_color)
        if (computer_win_row, computer_win_col) != (-1, -1):
            return computer_win_row, computer_win_col
        if (player_win_row, player_win_col) != (-1, -1):
            return player_win_row, player_win_col
        open_four_row, open_four_col = self.find_open_four(self.computer_color)
        if (open_four_row, open_four_col) != (-1, -1):
            return open_four_row, open_four_col

        # greedy algorithm
        best_score = float("-inf")
        best_row, best_col = -1, -1
        possible_moves = self.nearby_moves(buffer_size=2)
        for (row, col) in possible_moves:
            score = self.evaluate_board_greedy(row,col)
            if best_score < score:
                best_score = score
                best_row, best_col = row, col
        return best_row, best_col

    def evaluate_board_greedy(self, row, col):
        # evaluate computer offense
        self.board[row][col] = self.computer_color
        computer_connected_five = self.count_five(self.computer_color)
        computer_open_four      = self.count_open_four(self.computer_color)
        computer_closed_four    = self.count_closed_four(self.computer_color)
        computer_open_three     = self.count_open_three(self.computer_color)
        computer_closed_three   = self.count_closed_three(self.computer_color)
        computer_open_two       = self.count_open_two(self.computer_color)
        computer_closed_two     = self.count_closed_two(self.computer_color)
        computer_double_three   = computer_open_three//2
        if computer_double_three > 0:
            print("computer double three: row=%d, col=%d"%(row,col))
        self.board[row][col] = 0

        offend_score   = self.open_2_pts * computer_open_two + self.closed_2_pts * computer_closed_two \
                         + self.open_3_pts * computer_open_three + self.closed_3_pts * computer_closed_three \
                         + self.open_4_pts * computer_open_four + self.closed_4_pts * computer_closed_four \
                         + self.connected_5_pts * computer_connected_five + self.double_3_pts * computer_double_three

        # evaluate computer defense
        self.board[row][col] = self.player_color
        player_connected_five  = self.count_five(self.player_color)
        player_open_four       = self.count_open_four(self.player_color)
        player_closed_four     = self.count_closed_four(self.player_color)
        player_open_three      = self.count_open_three(self.player_color)
        player_closed_three    = self.count_closed_three(self.player_color)
        player_open_two        = self.count_open_two(self.player_color)
        player_closed_two      = self.count_closed_two(self.player_color)
        player_double_three    = player_open_three//2

        self.board[row][col] = 0
        defend_score = self.open_2_pts * player_open_two + self.closed_2_pts * player_closed_two \
                       + (self.open_3_pts * player_open_three + self.closed_3_pts * player_closed_three \
                       + self.open_4_pts * player_open_four + self.closed_4_pts * player_closed_four \
                       + self.connected_5_pts * player_connected_five + self.double_3_pts * player_double_three)*2

        return offend_score + defend_score

    def get_move_wiki(self):
        computer_win_row, computer_win_col = self.winning_position(self.computer_color)
        player_win_row, player_win_col = self.winning_position(self.player_color)
        if (computer_win_row, computer_win_col) != (-1, -1):
            return computer_win_row, computer_win_col
        if (player_win_row, player_win_col) != (-1, -1):
            return player_win_row, player_win_col
        open_four_row, open_four_col = self.find_open_four(self.computer_color)
        if (open_four_row, open_four_col) != (-1, -1):
            return open_four_row, open_four_col

        depth = 0
        score = float("-inf")
        possible_moves = self.nearby_moves()
        best_row, best_col = possible_moves[0]
        debug_info = []
        for move_row, move_col in possible_moves:
            print("try (%d, %d)" %(move_row, move_col))
            self.board[move_row][move_col] = self.computer_color
            move_score = self.minimax_wiki(depth, True)
            debug_info.append({"position":(move_row, move_col), "score": move_score})
            if move_score > score:
                score = move_score
                best_row, best_col = move_row, move_col
            self.board[move_row][move_col] = 0 # restore current position
            self.minimax_records = {}  # clear catch
        print("get_move_wiki:")
        print(debug_info)
        return best_row, best_col

    def minimax_wiki(self, depth, maximize_computer_flag):
        if depth==0 or self.game_over() != -1:
            board_code = self.board_string_code()
            if board_code in self.minimax_records.keys():
                return self.minimax_records[board_code]
            else:
                score = self.evaluate_board_score(maximize_computer_flag)
                self.minimax_records[board_code] = score
                print("score: ", score)
                return score

        possible_moves = self.nearby_moves()
        if maximize_computer_flag:     # True, maximize computer
            score = float("-inf")
            debug_info = []
            for (move_row, move_col) in possible_moves:
                self.board[move_row][move_col] = self.player_color
                board_code = self.board_string_code()
                if board_code in self.minimax_records.keys():
                    move_score = self.minimax_records[board_code]
                else:
                    move_score = self.minimax_wiki(depth-1, False)
                self.board[move_row][move_col] = 0
                debug_info.append([(move_row, move_col), move_score])
                score = max(score, move_score)
            print("maximize computer: ")
            print(debug_info)
            print("max score: ", score)
            return score
        else:                         # False, maximize player by minimizing the score
            score = float("inf")
            debug_info = []
            for (move_row, move_col) in possible_moves:
                self.board[move_row][move_col] = self.computer_color
                board_code = self.board_string_code()
                if board_code in self.minimax_records.keys():
                    move_score = self.minimax_records[board_code]
                else:
                    move_score = self.minimax_wiki(depth-1, True)
                self.board[move_row][move_col] = 0
                debug_info.append([(move_row, move_col), move_score])
                score = min(score, move_score)
            print("minimize computer: ")
            print(debug_info)
            print("min score: ", score)
            return score


    def count_stone(self):
        count = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != 0:
                    count += 1
        return count

    def find_open_four(self, color_id):
        a = color_id
        # 0 A a a a 0
        # -           - current point, A, return point
        # 0 a a a A 0
        # -           - current point, A, return point
        for r in range(self.size):
            for c in range(self.size):
                # horizontal direction
                if self.inside([(r,c+5)]) and self.check([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4),(r,c+5)], [0,0,a,a,a,0]):
                    return r, c+1
                if self.inside([(r,c+5)]) and self.check([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4),(r,c+5)], [0,a,a,a,0,0]):
                    return r, c+4
                # vertical direction
                if self.inside([(r+5,c)]) and self.check([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c),(r+5,c)], [0,0,a,a,a,0]):
                    return r+1, c
                if self.inside([(r+5,c)]) and self.check([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c),(r+5,c)], [0,a,a,a,0,0]):
                    return r+4, c
                # upper right direction
                if self.inside([(r-5,c+5)]) and self.check([(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3),(r-4,c+4),(r-5,c+5)], [0,0,a,a,a,0]):
                    return r-1, c+1
                if self.inside([(r-5,c+5)]) and self.check([(r,c),(r-1,c+1),(r-2,c+2),(r-3,c+3),(r-4,c+4),(r-5,c+5)], [0,a,a,a,0,0]):
                    return r-4, c+4
                # lower right direction
                if self.inside([(r+5,c+5)]) and self.check([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4),(r+5,c+5)], [0,0,a,a,a,0]):
                    return r+1, c+1
                if self.inside([(r+5,c+5)]) and self.check([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4),(r+5,c+5)], [0,a,a,a,0,0]):
                    return r+4, c+4
        return -1, -1  # no open four

    def check(self, stone_row_col_list, pattern):
        result = True
        for k in range(len(stone_row_col_list)):
            row, col = stone_row_col_list[k]
            result = result and (self.board[row][col] == pattern[k])
        return result

    def inside(self, stones):
        for row, col in stones:
            if not ((0 <= row < self.size) and (0 <= col < self.size)):
                return False
        return True


    def print_possible_moves(self, possible_moves):
        print("possible moves: ")
        for row in range(self.size):
            for col in range(self.size):
                if possible_moves[row][col]==True:
                    print("(%d, %d)" %(row, col), end=" ")
        print("")

