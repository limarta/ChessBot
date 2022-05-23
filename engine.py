import pexpect
import chess

class UCIBoard(chess.Board):
    '''
    Generates the moves played in long notation for UCI
    '''
    def __init__(self):
        super().__init__()
        self.color = 1
        child = pexpect.spawn("./main")
        child.sendline("uci")
        child.expect("\r\n")
        child.expect("\r\n")
        child.expect("\r\n")
        child.expect("\r\n")
        self.child = child
    def readAndReply(self, opponent_move=None):
        if opponent_move is None: # We are white
            self.color = 0
        else:
            self.push_san(opponent_move)
        
        # Make next move
        moves = [str(move) for move in self.move_stack]
        setup = "position startpos" + ("" if len(moves) == 0 else (" moves " + (" ".join(moves))))
        self.child.sendline(setup)
        self.child.expect("\r\n")
        self.child.sendline("go")
        self.child.expect("\r\n")
        while True:
            self.child.expect(["info.*", "\r\n"])
            if "info" not in self.child.after.decode('utf-8'):
                # print(child.before)
                # print(child.after)
                break
            # else:
                # print("Info maybe")
                # print(child.before)
                # print(child.after)
        my_move = self.child.before.decode('utf-8')[9:]
        print("My move: ", my_move)
        self.push_uci(my_move)
        print(f"Moves for ply {self.ply}: {self.move_stack}")
        return my_move

if __name__=="__main__":
    board = UCIBoard()
    moves = []
