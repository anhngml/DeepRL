import game.mygym as gym
import pygame
import cv2


if __name__ == '__main__':
    env = gym.make()
    state = env.reset()

    carryOn = True
    while carryOn:
        next_state, reward, done, _ = env.step(2)
    pygame.quit()
