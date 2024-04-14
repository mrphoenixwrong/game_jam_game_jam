from game import title_loop, game_loop

RUNNING = True

levels = [[2, (5, 10), 5, 5, False], [80, (3, 5), 10, 10, False], [100, (4, 7), 15, 15, True], [120, (3, 6), 18, 20, True], [150, (3, 5), 23, 30, True]]

while RUNNING:
    if RUNNING:
        RUNNING = title_loop()
    for i in range(0, 5):
        if RUNNING:
            IN_LEVEL = True
            while IN_LEVEL:
                RUNNING, IN_LEVEL = game_loop(i+1, levels[i][0], levels[i][1], levels[i][2], levels[i][3], levels[i][4])