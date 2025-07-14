import pygame
import random
import math
import numpy as np
from typing import List, Tuple

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("경기장 대피 시뮬레이션")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)

class Person:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.speed = 2.0
        self.radius = 5
        self.target_exit = None
        self.escaped = False
        self.panic_level = random.uniform(0.1, 0.3)
        
    def update_position(self, exits: List[Tuple[float, float]], obstacles: List[pygame.Rect]):
        if self.escaped:
            return
            
        # 가장 가까운 출구 찾기
        if self.target_exit is None:
            min_distance = float('inf')
            for exit_pos in exits:
                distance = math.sqrt((self.x - exit_pos[0])**2 + (self.y - exit_pos[1])**2)
                if distance < min_distance:
                    min_distance = distance
                    self.target_exit = exit_pos
        
        if self.target_exit:
            # 출구 방향으로 이동
            dx = self.target_exit[0] - self.x
            dy = self.target_exit[1] - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < 10:  # 출구에 도달
                self.escaped = True
                return
                
            # 정규화된 방향 벡터
            if distance > 0:
                dx /= distance
                dy /= distance
                
            # 속도 계산
            self.vx = dx * self.speed
            self.vy = dy * self.speed
            
            # 장애물 회피
            self.avoid_obstacles(obstacles)
            
            # 다른 사람들과의 상호작용
            self.avoid_people()
            
            # 위치 업데이트
            self.x += self.vx
            self.y += self.vy
            
            # 좌석 블록(장애물) 내부로 들어가지 않도록 제한 (통로만 이동)
            for obs in obstacles:
                if obs.collidepoint(self.x, self.y):
                    # 장애물 내부면 이전 위치로 되돌림
                    self.x -= self.vx
                    self.y -= self.vy
                    break
            # 원형 경기장 내로만 이동 제한
            center_x, center_y = WIDTH // 2, HEIGHT // 2
            stadium_radius = 480
            dist_from_center = math.sqrt((self.x - center_x) ** 2 + (self.y - center_y) ** 2)
            if dist_from_center > stadium_radius - self.radius:
                angle = math.atan2(self.y - center_y, self.x - center_x)
                self.x = center_x + (stadium_radius - self.radius) * math.cos(angle)
                self.y = center_y + (stadium_radius - self.radius) * math.sin(angle)
            self.x = max(self.radius, min(WIDTH - self.radius, self.x))
            self.y = max(self.radius, min(HEIGHT - self.radius, self.y))
    
    def avoid_obstacles(self, obstacles: List[pygame.Rect]):
        for obstacle in obstacles:
            # 장애물과의 거리 계산
            closest_x = max(obstacle.left, min(self.x, obstacle.right))
            closest_y = max(obstacle.top, min(self.y, obstacle.bottom))
            
            distance = math.sqrt((self.x - closest_x)**2 + (self.y - closest_y)**2)
            
            if distance < 30:  # 장애물 회피 거리
                # 장애물에서 멀어지는 방향으로 힘 적용
                avoid_x = self.x - closest_x
                avoid_y = self.y - closest_y
                
                if avoid_x != 0 or avoid_y != 0:
                    length = math.sqrt(avoid_x**2 + avoid_y**2)
                    avoid_x /= length
                    avoid_y /= length
                    
                    # 회피 힘 적용
                    self.vx += avoid_x * 1.5
                    self.vy += avoid_y * 1.5
    
    def avoid_people(self):
        # 다른 사람들과의 거리 기반 회피
        pass  # 간단화를 위해 생략
    
    def draw(self, screen):
        if not self.escaped:
            color = (255, int(255 * (1 - self.panic_level)), 0)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

class Stadium:
    def __init__(self):
        self.obstacles = []
        self.exits = []
        self.people = []
        # 배경 이미지 비율 유지하여 불러오기
        self.bg_img = pygame.image.load('stadium_bg.png').convert_alpha()
        self.bg_rect = self.bg_img.get_rect()
        scale_w = WIDTH / self.bg_rect.width
        scale_h = HEIGHT / self.bg_rect.height
        scale = min(scale_w, scale_h)
        new_w = int(self.bg_rect.width * scale)
        new_h = int(self.bg_rect.height * scale)
        self.bg_img = pygame.transform.smoothscale(self.bg_img, (new_w, new_h))
        self.bg_rect = self.bg_img.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.create_stadium()
        self.spawn_people(100)
        
    def create_stadium(self):
        # 경기장 외벽
        wall_thickness = 20
        self.obstacles = []
        self.exits = []
        self.seat_blocks = []  # 좌석 블록(숫자 네모) 저장
        
        # 좌석 블록(숫자 네모) 구역 정의 (예시, 실제 좌표는 사진 참고하여 대략적으로 배치)
        # 1루, 3루, 중앙, 외야 등 주요 구역별로 블록 생성
        # (x, y, w, h) 좌표는 사진을 참고해 대략적으로 배치
        # 1루 내야
        self.seat_blocks.append(pygame.Rect(900, 400, 80, 120))  # 201~205
        self.seat_blocks.append(pygame.Rect(820, 420, 80, 120))  # 206~210
        self.seat_blocks.append(pygame.Rect(740, 440, 80, 120))  # 211~215
        # 3루 내야
        self.seat_blocks.append(pygame.Rect(220, 400, 80, 120))  # 226~222
        self.seat_blocks.append(pygame.Rect(300, 420, 80, 120))  # 221~217
        self.seat_blocks.append(pygame.Rect(380, 440, 80, 120))  # 216~212
        # 중앙 프리미엄
        self.seat_blocks.append(pygame.Rect(520, 420, 160, 60))  # 중앙석
        # 외야(상단)
        self.seat_blocks.append(pygame.Rect(320, 100, 120, 60))  # 401~406
        self.seat_blocks.append(pygame.Rect(760, 100, 120, 60))  # 411~416
        # 300번대 블록 (301~334) 하단 반원형으로 배치 (이미지와 최대한 유사하게)
        circle_cx, circle_cy = WIDTH // 2, HEIGHT // 2 + 260  # 중심을 이미지 하단 쪽으로 이동
        circle_r = 340  # 반지름(가로, 세로 동일)
        angle_start = 200  # 301번 블록 시작 각도 (왼쪽 하단)
        angle_end = -20    # 334번 블록 끝 각도 (오른쪽 하단)
        num_blocks = 34
        self.rotated_blocks = []  # 회전된 블록 정보 저장 (for debugging or future use)
        for i in range(num_blocks):
            angle = math.radians(angle_start + (angle_end - angle_start) * i / (num_blocks - 1))
            block_cx = int(circle_cx + circle_r * math.cos(angle))
            block_cy = int(circle_cy + circle_r * math.sin(angle))
            # 블록 크기
            w, h = 52, 32
            # 블록 중심을 기준으로 각도에 맞춰 회전 (pygame은 rect 회전 지원X, 정보만 저장)
            block_rect = pygame.Rect(block_cx - w//2, block_cy - h//2, w, h)
            self.seat_blocks.append(block_rect)
            self.rotated_blocks.append((block_rect, angle))  # 필요시 시각화에 활용 가능
        # 장애물로 좌석 블록 추가
        self.obstacles.extend(self.seat_blocks)
        # 출구 위치 (사진 기준 실제 좌표에 최대한 맞춤)
        self.exits = [
            (170, 520),      # 2-1 Gate (3루 내야 출입구, 사진상 왼쪽 아래)
            (1030, 520),     # 2-3 Gate (1루 내야 출입구, 사진상 오른쪽 아래)
            (320, 90),       # 1-3 Gate (외야 3루 쪽, 사진상 왼쪽 위)
            (880, 90),       # 1-4 Gate (외야 1루 쪽, 사진상 오른쪽 위)
        ]

    def spawn_people(self, count: int):
        self.people = []
        for _ in range(count):
            # 좌석 블록(숫자 네모)에서만 생성
            block = random.choice(self.seat_blocks)
            x = random.randint(block.left + 10, block.right - 10)
            y = random.randint(block.top + 10, block.bottom - 10)
            self.people.append(Person(x, y))
    
    def update(self):
        for person in self.people:
            person.update_position(self.exits, self.obstacles)
    
    def draw(self, screen):
        # 배경 (비율 유지, 중앙 정렬)
        screen.fill(WHITE)
        # 비율 유지하여 중앙에 배경 이미지 출력
        screen.blit(self.bg_img, self.bg_rect)
        
        
        # 장애물 그리기 (테두리만)
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, GRAY, obstacle, 2)  # 회색 테두리만
        
        # 출구 그리기
        for exit_pos in self.exits:
            pygame.draw.circle(screen, GREEN, (int(exit_pos[0]), int(exit_pos[1])), 15)
        
        # 사람들 그리기
        for person in self.people:
            person.draw(screen)
        
        # 통계 정보
        escaped_count = sum(1 for person in self.people if person.escaped)
        total_count = len(self.people)
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"대피 완료: {escaped_count}/{total_count}", True, BLACK)
        screen.blit(text, (10, 10))

def main():
    clock = pygame.time.Clock()
    stadium = Stadium()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 스페이스바로 새로운 시뮬레이션 시작
                    stadium = Stadium()
        
        stadium.update()
        stadium.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
