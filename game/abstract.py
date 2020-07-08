# from abc import ABC, abstractmethod, abstractproperty

# class AbstractGame(ABC):
#     def __init__(self, player1, player2):
#         super().__init__()

#         self.player1 = player1 # agent acting as player1 (1)
#         self.player2 = player2 # agent acting as player2 (-1)

#         self.current_player = 1
    
#     def play(self):
#         finished = False
#         while not finished:
#             finished, winner = self.step()

#         return winner

#     def step(self):
#         valid = self.move()
#         if not valid:
#             return True, -self.current_player

#         finished, winner = self.is_finished()
#         self.current_player = -self.current_player

#         return finished, winner

#     @abstractmethod
#     def move(self):
#         pass

#     @abstractmethod
#     def is_finished(self):
#         pass

#     @abstractproperty
#     def current_player(self):
#         pass

#     @abstractproperty
#     def state(self):
#         pass