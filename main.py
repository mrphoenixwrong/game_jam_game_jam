from game import  game_loop

RUNNING = True

levels = [[80, (5, 10), 5], [80, (4, 8), 10], [100, (4, 7), 15], [120, (3, 6), 18], [150, (2, 5), 23]]

while RUNNING:
    #if RUNNING:
     #   title_loop()
    for i in range(0, 5):
        if RUNNING:
            RUNNING = game_loop(levels[i][0], levels[i][1], levels[i][2])