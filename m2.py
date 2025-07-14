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

def calculate_manhattan_distance(point1, point2):
    """두 점 사이의 맨해튼 거리를 계산합니다."""
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def debug_manhattan_distances():
    """각 좌석에서 출구까지의 맨해튼 거리를 계산하고 출력합니다."""
    print("=== 맨해튼 거리 디버깅 정보 ===")
    print("좌석별 출구까지의 맨해튼 거리:")
    
    # 좌우로 좌석 분리 (x 좌표 기준으로 중앙값 계산)
    x_coords = [seat[0] for seat in SEAT_POINTS]
    center_x = sum(x_coords) / len(x_coords)
    
    left_seats = []
    right_seats = []
    
    for i, seat in enumerate(SEAT_POINTS):
        if seat[0] <= center_x:
            left_seats.append((i, seat))
        else:
            right_seats.append((i, seat))
    
    print(f"중앙 x 좌표: {center_x}")
    print(f"왼쪽 좌석 수: {len(left_seats)}, 오른쪽 좌석 수: {len(right_seats)}")
    
    # 각 좌석의 맨해튼 거리를 계산하여 저장 (좌우 분리)
    left_distances = []
    right_distances = []
    
    # 왼쪽 좌석들의 거리 계산
    for i, seat in left_seats:
        min_distance = float('inf')
        closest_exit = None
        
        for exit_point in EXIT_POINTS:
            distance = calculate_manhattan_distance(seat, exit_point)
            if distance < min_distance:
                min_distance = distance
                closest_exit = exit_point
        
        left_distances.append((i, seat, min_distance, closest_exit))
        print(f"왼쪽 좌석 {i+1}: ({seat[0]}, {seat[1]}) -> 출구 {closest_exit}: {min_distance}")
    
    # 오른쪽 좌석들의 거리 계산
    for i, seat in right_seats:
        min_distance = float('inf')
        closest_exit = None
        
        for exit_point in EXIT_POINTS:
            distance = calculate_manhattan_distance(seat, exit_point)
            if distance < min_distance:
                min_distance = distance
                closest_exit = exit_point
        
        right_distances.append((i, seat, min_distance, closest_exit))
        print(f"오른쪽 좌석 {i+1}: ({seat[0]}, {seat[1]}) -> 출구 {closest_exit}: {min_distance}")
    
    # 각각 오름차순 정렬
    left_distances.sort(key=lambda x: x[2])
    right_distances.sort(key=lambda x: x[2])
    
    print("\n=== 왼쪽 좌석 맨해튼 거리 오름차순 정렬 ===")
    for rank, (original_index, seat, distance, exit_point) in enumerate(left_distances, 1):
        print(f"왼쪽 순위 {rank}: 좌석 {original_index+1} ({seat[0]}, {seat[1]}) -> 출구 {exit_point}: {distance}")
    
    print("\n=== 오른쪽 좌석 맨해튼 거리 오름차순 정렬 ===")
    for rank, (original_index, seat, distance, exit_point) in enumerate(right_distances, 1):
        print(f"오른쪽 순위 {rank}: 좌석 {original_index+1} ({seat[0]}, {seat[1]}) -> 출구 {exit_point}: {distance}")
    
    # 맨해튼 거리 순서로 인덱스 매핑 생성 (왼쪽과 오른쪽 각각)
    left_distance_to_index = {}
    right_distance_to_index = {}
    
    for rank, (original_index, seat, distance, exit_point) in enumerate(left_distances):
        left_distance_to_index[distance] = rank
    
    for rank, (original_index, seat, distance, exit_point) in enumerate(right_distances):
        right_distance_to_index[distance] = rank
    
    print("\n=== 왼쪽 맨해튼 거리를 인덱스로 치환 ===")
    for distance in sorted(left_distance_to_index.keys()):
        print(f"왼쪽 거리 {distance} -> 순위 {left_distance_to_index[distance]}")
    
    print("\n=== 오른쪽 맨해튼 거리를 인덱스로 치환 ===")
    for distance in sorted(right_distance_to_index.keys()):
        print(f"오른쪽 거리 {distance} -> 순위 {right_distance_to_index[distance]}")
    
    return left_distances, right_distances, left_distance_to_index, right_distance_to_index

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
    def __init__(self, x, y, start_delay=0):
        self.x = x
        self.y = y
        self.radius = 2
        self.color = (255, 100, 0)
        self.original_speed = 0.2  # 픽셀당 속도를 0.2로 설정
        self.speed = self.original_speed  # 현재 속도
        self.escaped = False
        self.exit_target = None
        self.path_index = 0  # 경로 인덱스
        self.joined_path = False  # 경로에 합류했는지 여부
        self.target_exit_index = None  # 목표 출구 인덱스
        self.collision_count = 0  # 충돌 횟수
        self.start_delay = start_delay  # 출발 지연 시간 (초)
        self.start_time = None  # 실제 출발 시간
        self.started = False  # 출발했는지 여부

    def handle_collisions(self, all_people):
        """다른 관중들과의 충돌 감지 및 속도 감소"""
        collision_detected = False
        for other in all_people:
            if other != self and not other.escaped:
                distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
                if distance < 1:  # 충돌 감지 거리를 1로 변경
                    collision_detected = True
                    self.collision_count += 1  # 충돌 횟수 증가
                    break
        if collision_detected:
            self.speed = max(0.06, self.original_speed * 0.3)  # 원래 속도의 30%로 감소 (최소 0.06)
        else:
            self.speed = self.original_speed  # 원래 속도로 복구

    def update(self, path_points, exit_points, all_people, current_time):
        if self.escaped:
            return
        
        # 출발 지연 시간 체크
        if not self.started:
            if self.start_time is None:
                self.start_time = current_time
            elif current_time - self.start_time >= self.start_delay * 1000:  # 밀리초 단위로 변환
                self.started = True
            else:
                return  # 아직 출발하지 않음
        
        self.handle_collisions(all_people)
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
                self.escaped = True
    def draw(self, screen):
        if not self.escaped:
            # 속도에 따른 색상 변경 (빠를수록 초록색, 느릴수록 빨간색)
            if self.speed >= 0.16:
                color = (0, 255, 0)  # 초록색 (빠름)
            elif self.speed >= 0.12:
                color = (255, 165, 0)  # 주황색 (보통)
            else:
                color = (255, 0, 0)  # 빨간색 (느림)
            
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

def spawn_people(num_people_per_seat, left_distances, right_distances, delay_per_rank=2):
    people = []
    
    # 왼쪽 좌석들 처리
    for seat_idx, (original_index, seat, distance, exit_point) in enumerate(left_distances):
        for _ in range(num_people_per_seat):
            px = seat[0] + random.randint(-15, 15)
            py = seat[1] + random.randint(-15, 15)
            # 가장 가까운 PATH_POINTS 인덱스 계산
            min_idx = 0
            min_dist = float('inf')
            for idx, (wx, wy) in enumerate(PATH_POINTS):
                dist = ((px - wx) ** 2 + (py - wy) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    min_idx = idx
            
            # 왼쪽 순위에 따른 지연 시간 계산 (1순위는 0초, 2순위는 2초, 3순위는 4초...)
            start_delay = seat_idx * delay_per_rank
            person = Person(px, py, start_delay)
            person.path_index = min_idx
            people.append(person)
    
    # 오른쪽 좌석들 처리
    for seat_idx, (original_index, seat, distance, exit_point) in enumerate(right_distances):
        for _ in range(num_people_per_seat):
            px = seat[0] + random.randint(-15, 15)
            py = seat[1] + random.randint(-15, 15)
            # 가장 가까운 PATH_POINTS 인덱스 계산
            min_idx = 0
            min_dist = float('inf')
            for idx, (wx, wy) in enumerate(PATH_POINTS):
                dist = ((px - wx) ** 2 + (py - wy) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    min_idx = idx
            
            # 오른쪽 순위에 따른 지연 시간 계산 (1순위는 0초, 2순위는 2초, 3순위는 4초...)
            start_delay = seat_idx * delay_per_rank
            person = Person(px, py, start_delay)
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

    # 맨해튼 거리 디버깅 정보 출력
    left_distances, right_distances, left_distance_to_index, right_distance_to_index = debug_manhattan_distances()

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
    
    # 관중 생성 (각 좌석마다 10명, 좌우 순위별로 5초씩 지연)
    people = spawn_people(10, left_distances, right_distances, 5)
    
    # 탈출 시간 측정 변수
    start_time = pygame.time.get_ticks()
    escape_time = None
    all_escaped = False

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
        current_time = pygame.time.get_ticks()
        for person in people:
            person.update(PATH_POINTS, EXIT_POINTS, people, current_time)
            person.draw(screen)

        # 모든 관중이 탈출했는지 확인
        alive_count = sum(not p.escaped for p in people)
        if alive_count == 0 and not all_escaped:
            all_escaped = True
            escape_time = pygame.time.get_ticks() - start_time

        # 왼쪽 상단에 현재 필드에 존재하는 관중 수 표시
        font = pygame.font.Font(None, 36)
        text = font.render(f'# of people: {alive_count}', True, (0, 0, 0))
        screen.blit(text, (20, 20))
        
        # 경과 시간 표시 (탈출 완료 시에는 멈춤)
        if not all_escaped:
            current_time = pygame.time.get_ticks() - start_time
            time_text = font.render(f'Time: {current_time/1000:.1f}s', True, (0, 0, 255))
        elif escape_time is not None:
            time_text = font.render(f'Total Time: {escape_time/1000:.1f}s', True, (255, 0, 0))
        else:
            time_text = font.render('Time: 0.0s', True, (255, 0, 0))
        screen.blit(time_text, (20, 60))
        
        # 총 충돌 횟수 표시
        total_collisions = sum(p.collision_count for p in people)
        collision_text = font.render(f'Collisions: {total_collisions}', True, (255, 0, 0))
        screen.blit(collision_text, (20, 100))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()
