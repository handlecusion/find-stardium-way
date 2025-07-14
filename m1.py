import pygame
# 관객 생성 좌표를 점으로 시각화하기 위한 코드 예시:
SEAT_POINTS = [
    (937, 343), (937, 369), (937, 402), (931, 431), (920, 457), (915, 485),
    (898, 511), (885, 534), (863, 558), (848, 575), (820, 597), (795, 609),
    (768, 625), (737, 639), (713, 651), (682, 661), (644, 668), (609, 667),
    (573, 661), (536, 650), (505, 639), (479, 628), (453, 615), (428, 598),
    (402, 584), (380, 564), (365, 539), (346, 514), (330, 488), (322, 460),
    (317, 430), (312, 399), (312, 376), (311, 344)
]

def draw_seat_points(screen):
    # 점이 보이지 않는 문제는 draw_seat_points 함수가 실제로 호출되지 않거나,
    # SEAT_POINTS가 함수 정의 전에 선언되지 않아서 발생할 수 있습니다.
    # SEAT_POINTS를 함수 위로 올리고, 점이 화면에 그려지는지 확인하세요.
    # 또한, 점이 다른 그래픽 요소에 가려지지 않도록 draw_seat_points를 화면 그리기 루프에서
    # 배경, 장애물, 사람 그리기 전에 호출하는 것이 좋습니다.
    for x, y in SEAT_POINTS:
        pygame.draw.circle(screen, (128, 128, 128), (int(x), int(y)), 3)

import random

class Person:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 3
        self.color = (255, 100, 0)
        self.speed = 1.0  # 이동 속도 느리게
        self.escaped = False
        self.exit_target = None
        self.path_index = 0  # 경로 인덱스
        self.joined_path = False  # 경로에 합류했는지 여부
        self.target_exit_index = None  # 목표 출구 인덱스

    def update(self, path_points, exit_points):
        if self.escaped:
            return
            
        # 아직 경로에 합류하지 않았다면 가장 가까운 경로 지점으로 이동
        if not self.joined_path:
            if self.path_index < len(path_points):
                target = path_points[self.path_index]
                dx = target[0] - self.x
                dy = target[1] - self.y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                if dist < self.speed:
                    self.x, self.y = target
                    self.joined_path = True
                    self.path_index += 1
                else:
                    self.x += self.speed * dx / dist
                    self.y += self.speed * dy / dist
            return
            
        # 목표 출구 인덱스가 설정되지 않았다면 가장 가까운 EXIT_POINT의 인덱스 찾기
        if self.target_exit_index is None:
            min_dist = float('inf')
            for i, (ex, ey) in enumerate(exit_points):
                dist = ((self.x - ex) ** 2 + (self.y - ey) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    self.target_exit_index = i
        
        # 목표 출구 인덱스에 해당하는 PATH_POINTS 인덱스 찾기
        target_exit = exit_points[self.target_exit_index]
        target_path_index = None
        for i, (px, py) in enumerate(path_points):
            if (px, py) == target_exit:
                target_path_index = i
                break
        
        # 목표 출구 방향으로 경로 따라 이동
        if target_path_index is not None:
            if self.path_index < target_path_index:
                # 목표 출구 방향으로 이동 (인덱스 증가)
                if self.path_index < len(path_points):
                    target = path_points[self.path_index]
                    dx = target[0] - self.x
                    dy = target[1] - self.y
                    dist = (dx ** 2 + dy ** 2) ** 0.5
                    if dist < self.speed:
                        self.x, self.y = target
                        self.path_index += 1
                    else:
                        self.x += self.speed * dx / dist
                        self.y += self.speed * dy / dist
            elif self.path_index > target_path_index:
                # 목표 출구 방향으로 이동 (인덱스 감소)
                if self.path_index > 0:
                    target = path_points[self.path_index - 1]
                    dx = target[0] - self.x
                    dy = target[1] - self.y
                    dist = (dx ** 2 + dy ** 2) ** 0.5
                    if dist < self.speed:
                        self.x, self.y = target
                        self.path_index -= 1
                    else:
                        self.x += self.speed * dx / dist
                        self.y += self.speed * dy / dist
            else:
                # 목표 출구에 도달
                self.escaped = True

    def draw(self, screen):
        if not self.escaped:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def spawn_people(num_people_per_seat):
    people = []
    for x, y in SEAT_POINTS:
        for _ in range(num_people_per_seat):
            px = x + random.randint(-15, 15)
            py = y + random.randint(-15, 15)
            # 가장 가까운 PATH_POINTS 인덱스 계산
            min_idx = 0
            min_dist = float('inf')
            for idx, (wx, wy) in enumerate(PATH_POINTS):
                dist = ((px - wx) ** 2 + (py - wy) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    min_idx = idx
            person = Person(px, py)
            person.path_index = min_idx
            people.append(person)
    return people


# 탈출 지점 좌표 (예시: 클릭한 좌표에서 추출)
EXIT_POINTS = [(832, 526), (404, 508)]
# 301~334 블록 안쪽 흰색길 경로 좌표
PATH_POINTS = [
    (336, 346), (339, 365), (345, 398), (353, 423), (363, 448), (373, 470),
    (386, 490), (404, 508), (421, 527), (438, 542), (457, 556), (479, 570),
    (500, 581), (526, 590), (550, 598), (578, 604), (608, 607), (640, 608),
    (670, 605), (698, 598), (721, 592), (747, 582), (770, 571), (792, 558),
    (810, 543), (832, 526), (846, 511), (864, 487), (876, 469), (889, 445),
    (897, 420), (906, 397), (912, 370), (913, 346)
]
import sys
def print_click_pos(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        print(f"클릭한 좌표: ({x}, {y})")

# 화면 크기 설정 (예시: 1200x800)
WIDTH, HEIGHT = 1200, 800

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("경기장 이미지 시뮬레이션")

    # stadium_bg.png 이미지를 불러오고 화면 크기에 맞게 비율 유지하여 스케일링
    bg_img = pygame.image.load('stadium_bg.png').convert_alpha()
    bg_rect = bg_img.get_rect()
    scale_w = WIDTH / bg_rect.width
    scale_h = HEIGHT / bg_rect.height
    scale = min(scale_w, scale_h)
    new_w = int(bg_rect.width * scale)
    new_h = int(bg_rect.height * scale)
    bg_img = pygame.transform.smoothscale(bg_img, (new_w, new_h))
    bg_rect = bg_img.get_rect(center=(WIDTH//2, HEIGHT//2))

    clock = pygame.time.Clock()
    running = True
    
    # 관중 생성 (각 좌석마다 100명)
    people = spawn_people(100)

    # 문제 원인: 클릭 좌표를 출력하는 print_click_pos 함수가 main 루프에서 호출되지 않음
    # 해결: 이벤트 루프에서 MOUSEBUTTONDOWN 이벤트 발생 시 print_click_pos 호출

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 클릭 이벤트 처리 추가
            if event.type == pygame.MOUSEBUTTONDOWN:
                print_click_pos(event)

        screen.fill((255, 255, 255))  # 배경 흰색
        screen.blit(bg_img, bg_rect)  # 중앙 정렬로 이미지 출력
        
        # 좌석 점들을 그리기
        draw_seat_points(screen)
        
        # 관중들 업데이트 및 그리기
        for person in people:
            person.update(PATH_POINTS, EXIT_POINTS)
            person.draw(screen)

        # 왼쪽 상단에 현재 필드에 존재하는 관중 수 표시
        font = pygame.font.SysFont(None, 36)
        alive_count = sum(not p.escaped for p in people)
        text = font.render(f'# of people: {alive_count}', True, (0, 0, 0))
        screen.blit(text, (20, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()
