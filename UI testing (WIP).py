import pygame
import pygame_gui
import webbrowser
import traceback
import sys

def main():
    
    pygame.init()

    pygame.display.set_caption("Tank War ")
    screen = pygame.display.set_mode((630, 630))

    background = pygame.image.load(r"image\title.png")

    manager = pygame_gui.UIManager((630, 630))

    START = pygame_gui.elements.UIButton(pygame.Rect((250, 350), (130, 50)), text="START", manager=manager)
    EDITOR = pygame_gui.elements.UIButton(pygame.Rect((250, 425), (130, 50)), text="EDITOR", tool_tip_text="WORK IN PROCESS", manager=manager)
    EXIT = pygame_gui.elements.UIButton(pygame.Rect((250, 500), (130, 50)), text="EXIT", manager=manager)
    EASTEREGG = pygame_gui.elements.UIButton(pygame.Rect((620, 620), (10, 10)), text=" ", manager=manager)

    clock = pygame.time.Clock()

    while True:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == EXIT):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == START:
                    
                    screen.fill([0,0,0])
                    
                elif event.ui_element == EDITOR:
                    print("WIP")
                elif event.ui_element == EASTEREGG:
                    webbrowser.open_new_tab("https://www.google.com/search?q=tank+war")

            manager.process_events(event)

        manager.update(time_delta)

        screen.blit(background, (0, 0))
        manager.draw_ui(screen)

        pygame.display.update()

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
