def main():
    import pygame
    from ParallelBars import Bars

    pygame.init()                                                           # inicialização

    refresh = 60
    clock = pygame.time.Clock() 
    update = pygame.USEREVENT + 1
    pygame.time.set_timer(update, refresh)

    bars = Bars(False, True)

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == update:
                bars.update()
                bars.putOnScreen()
            '''if e.type == pygame.MOUSEBUTTONDOWN:
                bars.refresh()
            if e.type == pygame.MOUSEBUTTONUP:
                bars.clicked = False'''
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running = False

if __name__ == '__main__':
    main()