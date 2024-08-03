import pygame
import os
#整体背景音乐
def bgm():
    # 在初始化部分加载背景音乐
    pygame.mixer.music.load(
    os.path.join("Assets", 'bgm.mp3'))  # 背景音乐文件名为'.mp3'

    # 在游戏开始时播放背景音乐
    pygame.mixer.music.play(-1)  # 播放背景音乐，无限循环

def close_bgm():
    pygame.mixer.music.stop()
