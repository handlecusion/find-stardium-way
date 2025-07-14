import pygame
import random
import numpy as np

# 설정
GRID_SIZE = 400            # 시뮬레이션용 격자 (성능 고려해 400x400)
CELL_SIZE = 2              # 셀당 픽셀 수 (그래픽 표현용)
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
NUM_AGENTS = 5000          # 관중 수
EXIT_POINTS = [(200, 0), (0, 200), (399, 200), (200, 399), (200, 100)]  # 출구 좌표

# 초기화
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("ABC Crowd Evacuation Heatmap")
clock = pygame.time.Clock()

# 에이전트 초기 위치: 중앙 근처에 무작위 배치
agents = [(random.randint(150, 250), random.randint(150, 250)) for _ in range(NUM_AGENTS)]
heatmap = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

# 히트맵 색상 정의 함수
def get_color(count):
    if count == 0:
        return (255, 255, 255)
    elif count < 3:
        return (144, 238, 144)
    elif count < 6:
        return (255, 255, 0)
    elif count < 10:
        return (255, 165, 0)
    else:
        return (255, 0, 0)

# ABC 알고리즘 유사: 이동할 방향 결정
def evaluate_move(x, y):
    costs = []
    for ex, ey in EXIT_POINTS:
        dist = abs(ex - x) + abs(ey - y)
        congestion_penalty = heatmap[y % GRID_SIZE, x % GRID_SIZE] * 5
        cost = dist + congestion_penalty
        costs.append((cost, (ex, ey)))
    return min(costs, key=lambda c: c[0])[1]

# 메인 루프
running = True
while running:
    screen.fill((0, 0, 0))
    heatmap[:, :] = 0  # 현재 체류 방식: 프레임마다 리셋

    new_agents = []
    for x, y in agents:
        target = evaluate_move(x, y)
        dx = np.sign(target[0] - x)
        dy = np.sign(target[1] - y)
        nx, ny = x + dx, y + dy

        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            new_agents.append((nx, ny))
            heatmap[ny, nx] += 1
        # 출구 도달 시 제외됨

    # 히트맵 시각화
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = get_color(heatmap[y, x])
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    agents = new_agents
    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()