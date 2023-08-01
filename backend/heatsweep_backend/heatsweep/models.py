from django.db import models
import math
from random import randrange
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class Player(models.Model):
    username = models.TextField(unique=True, max_length=20)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    elo = models.IntegerField(default=1000)

    def update_elo(self, elo):
        self.elo = elo
        self.save(update_fields=['elo'])

    def incr_wins(self):
        self.wins = self.wins + 1
        self.save(update_fields=['wins'])

    def incr_losses(self):
        self.losses = self.losses + 1
        self.save(update_fields=['losses'])

class Tile(models.Model):
    EMPTY = 'none'
    A = 'a'
    B = 'b'
    H = 'h'
    TILE_CHOICES = (
        (EMPTY, 'None'),
        (A, 'A'),
        (B, 'B'),
        (H, 'Hotspot'),
    )
    status = models.CharField(max_length=6, choices=TILE_CHOICES, default=EMPTY)
    x = models.IntegerField()
    y = models.IntegerField()
    index = models.IntegerField()
    heat_value = models.CharField(max_length=7, default="#CCCCCC")
    a_revealed = models.BooleanField(default=False)
    b_revealed = models.BooleanField(default=False)
    game = models.ForeignKey('heatsweep.Game', related_name="tile_game", on_delete=models.CASCADE)

    '''
    Setter method to update the status of a Tile
    Automatically reveals the tile to player 1/player 2 if they are set as the new owner
    '''
    def set_status(self, status, h_x, h_y, g):
        if self.status == status or self.status == Tile.H:
            return False

        max_dist = g * math.sqrt(2)
        dist = math.sqrt((h_x - self.x)**2 + (h_y - self.y)**2)
        sigma = math.sqrt(g)
        heat = math.exp(-((dist**2)/(2*sigma**2)))

        self.status = status
        self.heat_value = Tile.get_color(heat)
        self.save()

        # # reveal the tile if applicable
        # if status == Tile.A:
        #     self.reveal_a()
        # elif status == Tile.B:
        #     self.reveal_b()
        return True

    @staticmethod
    def get_color(heatValue):
        # Define the colormap and normalization function
        cmap = plt.get_cmap('hot')
        
        # Convert the normalized heat value to an RGB color
        color = cmap(heatValue)
        
        # Convert the RGB color to a hex color code
        hex_color = mcolors.rgb2hex(color)
        
        return hex_color
    
    '''
    Reveals the tile to player a.
    '''
    def reveal_a(self):
        # if not self.a_revealed:
        #     self.a_revealed = True
        #     self.save(update_fields=['a_revealed'])
        pass
    
    '''
    Reveals the tile to player b.
    '''
    def reveal_b(self):
        # if not self.b_revealed:
        #     self.b_revealed = True
        #     self.save(update_fields=['b_revealed'])
        pass

    '''
    Reveals the tile to the given player.
    '''
    def reveal(self, player):
        # if player == self.A:
        #     self.reveal_a()
        # elif player == self.B:
        #     self.reveal_b()
        # else:
        #     raise ValueError("invalid player value passed to Tile.reveal()")
        pass
        
    '''
    Getter method for the revealed state of the tile.
    '''
    def revealed(self, player):
        # if player == self.A:
        #     return self.a_revealed
        # elif player == self.B:
        #     return self.b_revealed
        # else:
        #     raise ValueError("invalid player value passed to Tile.reveal()")
        pass

class Game(models.Model):
    GRID_SIZE = 7
    GRID_X = GRID_SIZE
    GRID_Y = GRID_SIZE
    MARGIN = 2
    ELO_FACTOR = 30
    
    player_a = models.ForeignKey(Player, related_name="game_player_a", null=True, blank=True, on_delete=models.CASCADE)
    player_b = models.ForeignKey(Player, related_name="game_player_b", null=True, blank=True, on_delete=models.CASCADE)
    current_turn = models.ForeignKey(Player, related_name="game_turn", null=True, blank=True, on_delete=models.CASCADE)
    winner = models.ForeignKey(Player, related_name='game_winner', null=True, blank=True, on_delete=models.CASCADE)
    
    a_x = models.IntegerField(default=0)
    a_y = models.IntegerField(default=0)
    b_x = models.IntegerField(default=0)
    b_y = models.IntegerField(default=0)
    hotspot_x = models.IntegerField(default=0)
    hotspot_y = models.IntegerField(default=0)

    @staticmethod
    def create(player):
        game = Game(player_a=player, current_turn=player)
        game.save()
        for x in range(Game.GRID_SIZE):
            for y in range(Game.GRID_SIZE):
                i = (Game.GRID_SIZE*y) + x
                tile = Tile(x=x, y=y, index=i, game=game)
                tile.save()
        game.init_start_points()

        return game     

    def toStatus(self, player):
        if player == self.player_a:
            return Tile.A
        elif player == self.player_b:
            return Tile.B     

    def get_all_tiles(self):
        return Tile.objects.filter(game=self).order_by('index')

    def get_tile_at(self, x, y):
        try:
            return Tile.objects.get(game=self, x=x, y=y)
        except Tile.DoesNotExist:
            return None

    def get_tile(self, index):
        try:
            return Tile.objects.get(game=self, index=index)
        except Tile.DoesNotExist:
            return None

    '''
    Sets ownership (status) of the specified tile to the specified player. If the specified tile is the hotspot, set its 
    status to the hotspot. This happens because at the beginning of the game, the hotspot doesn't appear on the board;
    only its coordinates are saved.

    This is the basic, non-fog-of-war approach.
    '''
    def flip(self, index, player):
        if (self.current_turn != player):
            return False

        tile = self.get_tile(index)
        x = tile.x
        y = tile.y

        if (player == self.player_a and x == self.b_x and y == self.b_y):
            return False
        if (player == self.player_b and x == self.a_x and y == self.a_y):
            return False

        status = Tile.A
        if (x == self.hotspot_x and y == self.hotspot_y):
            status = Tile.H
        elif (player == self.player_a):
            status = Tile.A
        elif (player == self.player_b):
            status = Tile.B

        if not tile.set_status(status, self.hotspot_x, self.hotspot_y, Game.GRID_SIZE):
            return False

        self.next_turn()
        return True

    def init_start_points(self):
        # randomly pick player starting points and set the status of their tiles
        # both points in middle half, a is on top 4th, b bottom 4th
        # a_x = randrange(Game.GRID_X/4,3*Game.GRID_X/4-1)
        # a_y = randrange(0,Game.GRID_Y/4)
        # b_x = randrange(Game.GRID_X/4,3*Game.GRID_X/4-1)
        # b_y = randrange(0,Game.GRID_Y/4)

        # TODO TODO TODO: updpate to better hotspot algorithm below
        self.hotspot_x = randrange(0, Game.GRID_SIZE-(Game.MARGIN*2)-1) + Game.MARGIN
        self.hotspot_y = randrange(0, Game.GRID_SIZE-(Game.MARGIN*2)-1) + Game.MARGIN
        
        corners = (0, Game.GRID_SIZE-1)
        a_x = corners[randrange(0,2)]
        a_y = corners[randrange(0,2)]
        b_x = corners[randrange(0,2)]
        b_y = corners[randrange(0,2)]
        
        while (b_x == a_x and b_y == a_y):
            b_x = corners[randrange(0,2)]
            b_y = corners[randrange(0,2)]

        self.get_tile_at(a_x, a_y).set_status(Tile.A, self.hotspot_x, self.hotspot_y, Game.GRID_SIZE)
        self.get_tile_at(b_x, b_y).set_status(Tile.B, self.hotspot_x, self.hotspot_y, Game.GRID_SIZE)

        self.a_x = a_x
        self.a_y = a_y
        self.b_x = b_x
        self.b_y = b_y
        
        '''
        # hotspot should be equidistant from both players
        # all points on the line perpendicular to (a_x, a_y) -- (b_x, b_y) satisfy this constraint
        # pick an offset from the midpoint of that line at random and do the math
        # TODO: this technically needs integer solutions to be perfectly fair always. Otherwise off by 1
        # first pick the x-coord of the hotspot, then find the y-coord using point-slope form
        midpoint = ((self.b_x - self.a_x)/2, (self.b_y - self.a_y)/2)
        self.hotspot_x = randrange(-self.GRID_X/4, self.GRID_X/4)
        slope = -self.a_x/self.a_y
        self.hotspot_y = slope(self.hotspot_x - midpoint.first) + midpoint.second 
        '''

        # self.hotspot.set_status(Tile.H) TODO: readd this once fog of war comes back
        self.save()

    # '''
    # Returns a list of the coordinates adjacent to (x, y) that are within the grid.
    # '''
    # def valid_adjacent_coords(self, x, y):
    #     coords = []
    #     for (xi, yi) in [(x-1, y), (x, y+1), (x+1, y), (x, y-1)]:
    #         if 0 <= xi < self.GRID_X and 0 <= yi < self.GRID_Y: 
    #             coords.append(xi, yi)
        
    # # '''
    # # Reveals tiles adjacent to (x, y) to the given player.
    # # '''
    # # def reveal_adjacent(self, x, y, player):
    # #     for (xi, yi) in self.valid_adjacent_coords(x, y):
    # #         self.get_tile_at(xi, yi).reveal(player)

    # '''
    # Gives input player ownership of any unowned tiles adjacent to the tile at (x, y).
    # '''
    # def flip_adjacent(self, x, y, player):
    #     for (xi, yi) in self.valid_adjacent_coords(x, y):
    #         tile = self.get_tile_at(xi, yi)
    #         if tile.status == Tile.EMPTY:
    #             tile.set_status(self.toStatus(player))
    #         self.reveal_adjacent(xi, yi, player)

    # '''
    # Gives player ownership of tile at (x, y). If that tile is unowned (and not the hotspot), 
    # flip any unowned adjacent tiles as well.

    # All tiles adjacent to those just flipped will be revealed to the player as well.

    # Note: "adjacent" does not include diagonals here.
    # '''
    # def flipFogOfWar(self, x, y, player):
    #     tile = self.get_tile_at(x, y) # get the tile

    #     # if this grid space is empty, flip adjacent tiles as well (not diagonal)
    #     if tile.status == Tile.EMPTY:
    #         self.flip_adjacent(x, y, player)
        
    #     tile.set_status(self.toStatus(player)) # flip the tile

    # =+++++++++++++++++=
    # WIN CONDITION LOGIC
    # =+++++++++++++++++=

    # grid of 0s
    def empty_grid(self):
        return [[0]*self.GRID_X for _ in range(self.GRID_Y)]

    # return a list of all the coords within a 3x3 square around (x,y) if in the grid
    # I'm sure there's a cleaner way to do this but honestly this is the most readable I can do
    def get_adjacent(self, x, y):
        coords = []
        #for xi in [x-1, x, x+1]:
        #    for yi in [y-1, y, y+1]:
        #        if 0 <= xi < self.GRID_X and 0 <= yi < self.GRID_Y and not (x == y and xi == x): # make sure coords within grid
        #            coords.append((xi, yi))
        for (xi, yi) in [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]:
           if 0 <= xi < self.GRID_X and 0 <= yi < self.GRID_Y:
                coords.append((xi, yi))
        return coords

    def process_adjacent(self, x, y, player, checked):
        checked[y][x] = 1 # mark current coord as checked

        print(checked)
        for (xi, yi) in self.get_adjacent(x, y):
            # base case: hotspot is adjacent to us
            if (xi, yi) == (self.hotspot_x, self.hotspot_y):
                return True
            
            if checked[yi][xi] == 0 and self.get_tile_at(xi, yi).status == self.toStatus(player):
                # recurse on adjacent un-checked squares owned by player
                if self.process_adjacent(xi, yi, player, checked):
                    return True
        
        # base case: no path to hotspot
        return False

    def check_win(self, player):
        # step 0: check if the player can see the hotspot
        # if not self.get_tile_at(self.hotspot_x, self.hotspot_y).revealed(player):
        #     return False
        if self.get_tile_at(self.hotspot_x, self.hotspot_y).status != Tile.H:
            return False
        
        # recursively build out pathway from hotspot
        checkedGrid = self.empty_grid() # initialize matrix of 0s'
        if player == self.player_a:
            print(self.get_adjacent(self.hotspot_x, self.hotspot_y))
            return self.process_adjacent(self.a_x, self.a_y, player, checkedGrid)
        elif player == self.player_b:
            return self.process_adjacent(self.b_x, self.b_y, player, checkedGrid)
        
    def next_turn(self):
        if self.check_win(self.current_turn):
            self.winner = self.current_turn

            a_e = self.player_a.elo
            b_e = self.player_b.elo

            a_r = (1.0 / (1.0 + pow(10.0, ((b_e-a_e) / 400.0)))) 
            b_r = (1.0 / (1.0 + pow(10.0, ((a_e-b_e) / 400.0))))
            if self.winner == self.player_a:
                a_e = math.floor(a_e + Game.ELO_FACTOR*(1.0 - a_r))
                b_e = math.floor(b_e + Game.ELO_FACTOR*(0.0 - b_r))
                self.player_a.incr_wins()
                self.player_b.incr_losses()
            else:
                a_e = math.floor(a_e + Game.ELO_FACTOR*(0.0 - a_r))
                b_e = math.floor(b_e + Game.ELO_FACTOR*(1.0 - b_r))
                self.player_a.incr_losses()
                self.player_b.incr_wins()
            self.player_a.update_elo(a_e)
            self.player_b.update_elo(b_e)
        else:
            self.current_turn = self.player_a if self.current_turn == self.player_b else self.player_b
        self.save()

    
