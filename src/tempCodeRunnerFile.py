    # if GameManager.BOARD_SCENE_GLOBAL.__class__.__name__ == 'MultiplayerBoardScene':
    #     running = True
    #     while running:
    #         try:
    #             values = GameManager.BOARD_SCENE_GLOBAL.GameSocket.recv(1024).decode()
    #         except Exception:
    #             continue
    #         if values == '*[ Your Turn ]*' or values == '*[ Player 1 Turn ]*' or values == '*[ Player 2 Turn ]*':
    #             print(values)