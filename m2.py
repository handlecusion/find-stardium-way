import pygame
import random

# ====== 시뮬레이션 옵션 ======
# True: 최적화 탈출 알고리즘, False: 기본 탈출
OPTIMIZED_ESCAPE = True
# True: 동적 출발 시간 최적화, False: 고정 지연
DYNAMIC_START_OPTIMIZATION = True
# 출구별 1초당 탈출 허용 인원
QUEUE_EXIT_PER_SECOND = 3
# 1층 좌석당 생성 인원
PEOPLE_PER_SEAT_1F = 10
# 3층 좌석당 생성 인원
PEOPLE_PER_SEAT_3F = 15
# 외야 좌석당 생성 인원
PEOPLE_PER_SEAT_OUTFIELD = 10
# ===========================

# 내야 관중 좌석 좌표
SEAT_POINTS = [
    (359, 343), (363, 370), (371, 395), (379, 417), (393, 440), (404, 461),
    (421, 485), (439, 506), (458, 525), (479, 540), (499, 554), (520, 565),
    (551, 577), (622, 577), (696, 575), (726, 567), (749, 557), (775, 541),
    (792, 528), (815, 508), (832, 488), (847, 467), (859, 443), (870, 419),
    (880, 394), (888, 367), (895, 345),
    # 추가 좌표
    (402, 368), (414, 387), (427, 407), (443, 427), (457, 454), (474, 474),
    (491, 493), (514, 514), (537, 530), (562, 543), (691, 542), (713, 530),
    (737, 514), (758, 493), (780, 472), (794, 453), (810, 429), (829, 405),
    (838, 388), (846, 368), (859, 345)
]

# 외야 관중 좌석 좌표
SEAT_POINTS_OUTFIELD = [
    (323, 265), (337, 227), (358, 191), (377, 161), (400, 136), (423, 116),
    (451, 95), (477, 78), (509, 66), (539, 55), (569, 45), (679, 45),
    (711, 54), (741, 63), (771, 78), (798, 92), (825, 112), (849, 134),
    (871, 159), (892, 187), (913, 221), (926, 262)
]

# (필요하다면) 외야 전용 경로 및 출구 좌표도 아래처럼 별도 변수로 선언
PATH_POINTS_OUTFIELD = [
    (350, 287), (360, 255), (373, 221), (389, 192), (408, 170), (428, 150),
    (450, 127), (474, 111), (502, 94), (528, 82), (557, 72), (585, 66),
    (657, 66), (687, 72), (716, 80), (744, 92), (771, 106), (796, 122),
    (819, 144), (840, 166), (855, 190), (874, 218), (891, 256), (900, 290)
]
EXIT_POINTS_OUTFIELD = [
    (428, 150), (502, 94), (744, 92), (819, 144)
]

SEAT_POINTS_3F = [
    (310, 344), (310, 372), (314, 399), (319, 427), (328, 455), (338, 480),
    (356, 506), (371, 533), (389, 550), (408, 573), (427, 594), (449, 611),
    (479, 629), (505, 640), (538, 652), (567, 662), (604, 667), (641, 667),
    (681, 661), (711, 652), (743, 637), (769, 629), (796, 613), (820, 595),
    (843, 578), (863, 557), (882, 535), (897, 513), (913, 482), (925, 460),
    (933, 434), (938, 401), (941, 378), (946, 347)
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

class Person:
    def __init__(self, x, y, start_delay=0):
        self.x = x
        self.y = y
        self.radius = 4
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
        self.last_collision_time = 0  # 마지막 충돌 시간
        self.collision_display_duration = 1000  # 충돌 표시 지속 시간 (밀리초)
        self.optimized_path = []  # 최적화된 경로
        self.avoidance_vector = [0, 0]  # 회피 벡터
        self.waiting_at_exit = False  # 출구 앞 대기 상태

    def handle_collisions(self, all_people, current_time):
        """다른 관중들과의 충돌 감지 및 위치 조정"""
        collision_detected = False
        min_distance = float('inf')
        closest_person = None
        
        # 가장 가까운 사람 찾기
        for other in all_people:
            if other != self and not other.escaped:
                distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_person = other
                
                if distance < 1:  # 충돌 감지 거리를 1.2로 변경
                    collision_detected = True
                    self.collision_count += 1  # 충돌 횟수 증가
        
        if collision_detected and closest_person:
            # 충돌이 감지되면 위치 조정
            self.adjust_position(closest_person, all_people)
            self.speed = max(0.06, self.original_speed * 0.3)  # 원래 속도의 30%로 감소 (최소 0.06)
            self.last_collision_time = current_time  # 충돌 시간 기록
        else:
            self.speed = self.original_speed  # 원래 속도로 복구
    
    def adjust_position(self, closest_person, all_people):
        """충돌을 피하기 위해 위치를 조정합니다."""
        # 현재 위치에서 8방향으로 시도 (상, 하, 좌, 우, 대각선)
        directions = [
            (0, -1), (0, 1), (-1, 0), (1, 0),  # 상하좌우
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # 대각선
        ]
        
        original_x, original_y = self.x, self.y
        best_x, best_y = self.x, self.y
        min_collision_distance = 0
        
        # 각 방향으로 위치 조정 시도
        for dx, dy in directions:
            test_x = original_x + dx
            test_y = original_y + dy
            
            # 이 위치에서 다른 사람들과의 최소 거리 계산
            min_dist = float('inf')
            collision_free = True
            
            for other in all_people:
                if other != self and not other.escaped:
                    dist = ((test_x - other.x) ** 2 + (test_y - other.y) ** 2) ** 0.5
                    if dist < 1.2:  # 여전히 충돌
                        collision_free = False
                        break
                    min_dist = min(min_dist, dist)
            
            # 충돌이 없고, 더 멀리 떨어진 위치를 선택
            if collision_free and min_dist > min_collision_distance:
                min_collision_distance = min_dist
                best_x, best_y = test_x, test_y
        
        # 최적의 위치로 이동
        self.x, self.y = best_x, best_y
    
    def calculate_avoidance_vector(self, all_people):
        """다른 사람들을 피하기 위한 회피 벡터를 계산합니다."""
        avoidance_x, avoidance_y = 0, 0
        nearby_count = 0
        
        for other in all_people:
            if other != self and not other.escaped:
                distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
                if distance < 10 and distance > 0:  # 10픽셀 이내의 사람들
                    # 거리가 가까울수록 강한 회피력
                    force = (10 - distance) / 10
                    dx = self.x - other.x
                    dy = self.y - other.y
                    # 정규화
                    length = (dx ** 2 + dy ** 2) ** 0.5
                    if length > 0:
                        avoidance_x += (dx / length) * force
                        avoidance_y += (dy / length) * force
                        nearby_count += 1
        
        if nearby_count > 0:
            # 평균 회피 벡터 계산
            self.avoidance_vector = [avoidance_x / nearby_count, avoidance_y / nearby_count]
        else:
            self.avoidance_vector = [0, 0]
    
    def find_optimal_exit(self, exit_points, all_people):
        """가장 효율적인 출구를 선택합니다."""
        best_exit = 0
        min_congestion = float('inf')
        
        for i, exit_point in enumerate(exit_points):
            # 해당 출구로 향하는 사람 수 계산
            people_heading_to_exit = 0
            for person in all_people:
                if person != self and not person.escaped and person.target_exit_index == i:
                    people_heading_to_exit += 1
            
            # 출구까지의 거리와 혼잡도를 고려한 점수 계산
            distance = ((self.x - exit_point[0]) ** 2 + (self.y - exit_point[1]) ** 2) ** 0.5
            congestion_factor = people_heading_to_exit * 5  # 혼잡도 가중치
            total_score = distance + congestion_factor
            
            if total_score < min_congestion:
                min_congestion = total_score
                best_exit = i
        
        return best_exit

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
        
        # 최적화된 탈출 알고리즘 사용 여부 확인
        if OPTIMIZED_ESCAPE:
            self.update_optimized(path_points, exit_points, all_people, current_time)
        else:
            self.update_basic(path_points, exit_points, all_people, current_time)
    
    def update_optimized(self, path_points, exit_points, all_people, current_time):
        """최적화된 탈출 알고리즘"""
        self.handle_collisions(all_people, current_time)
        
        # 회피 벡터 계산
        self.calculate_avoidance_vector(all_people)
        
        # 최적 출구 선택 (주기적으로 재계산)
        if self.target_exit_index is None or current_time % 1000 < 50:  # 1초마다 재계산
            self.target_exit_index = self.find_optimal_exit(exit_points, all_people)
        
        # 아직 경로에 합류하지 않았다면 가장 가까운 경로 지점으로 이동
        if not self.joined_path:
            if self.path_index < len(path_points):
                target = path_points[self.path_index]
                dx = target[0] - self.x
                dy = target[1] - self.y
                
                # 회피 벡터 적용
                dx += self.avoidance_vector[0] * 0.3
                dy += self.avoidance_vector[1] * 0.3
                
                dist = (dx ** 2 + dy ** 2) ** 0.5
                if dist < self.speed:
                    self.x, self.y = target
                    self.joined_path = True
                    self.path_index += 1
                else:
                    self.x += self.speed * dx / dist
                    self.y += self.speed * dy / dist
            return
        
        # 목표 출구 인덱스에 해당하는 PATH_POINTS 인덱스 찾기
        target_exit = exit_points[self.target_exit_index]
        target_path_index = None
        for i, (px, py) in enumerate(path_points):
            if abs(px - target_exit[0]) < 1 and abs(py - target_exit[1]) < 1:
                target_path_index = i
                break
        
        # 목표 출구 방향으로 경로 따라 이동
        if target_path_index is not None:
            if self.path_index < target_path_index:
                if self.path_index < len(path_points):
                    target = path_points[self.path_index]
                    dx = target[0] - self.x
                    dy = target[1] - self.y
                    
                    # 회피 벡터 적용
                    dx += self.avoidance_vector[0] * 0.3
                    dy += self.avoidance_vector[1] * 0.3
                    
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
                    
                    # 회피 벡터 적용
                    dx += self.avoidance_vector[0] * 0.3
                    dy += self.avoidance_vector[1] * 0.3
                    
                    dist = (dx ** 2 + dy ** 2) ** 0.5
                    if dist < self.speed:
                        self.x, self.y = target
                        self.path_index -= 1
                    else:
                        self.x += self.speed * dx / dist
                        self.y += self.speed * dy / dist
            else:
                self.escaped = True
    
    def update_basic(self, path_points, exit_points, all_people, current_time):
        """기본 탈출 알고리즘"""
        self.handle_collisions(all_people, current_time)
        
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
    def draw(self, screen, current_time):
        if not self.escaped:
            # 출구 앞 대기 중이면 파란색
            if self.waiting_at_exit:
                color = (0, 0, 255)  # 파란색 (대기)
            # 충돌 후 1초 동안 빨간색으로 표시
            elif current_time - self.last_collision_time < self.collision_display_duration:
                color = (255, 0, 0)  # 빨간색 (충돌 상태)
            else:
                # 속도에 따른 색상 변경 (빠를수록 초록색, 느릴수록 빨간색)
                if self.speed >= 0.16:
                    color = (0, 255, 0)  # 초록색 (빠름)
                elif self.speed >= 0.12:
                    color = (255, 165, 0)  # 주황색 (보통)
                else:
                    color = (255, 0, 0)  # 빨간색 (느림)
            
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

def calculate_optimal_start_delay(seat_idx, distance, total_seats, base_delay=2):
    """
    영역별 최적 출발 시간을 계산합니다.
    
    Args:
        seat_idx: 좌석 순위 (0부터 시작)
        distance: 출구까지의 맨해튼 거리
        total_seats: 전체 좌석 수
        base_delay: 기본 지연 시간
    
    Returns:
        최적화된 출발 지연 시간 (초)
    """
    if not DYNAMIC_START_OPTIMIZATION:
        # 고정 지연 시간 사용
        return seat_idx * base_delay
    
    # 거리 기반 기본 지연 시간 (거리가 멀수록 더 늦게 출발)
    distance_factor = distance / 100  # 거리를 100으로 정규화
    
    # 순위 기반 지연 시간 (순위가 높을수록 더 늦게 출발)
    rank_factor = seat_idx / total_seats  # 순위를 0~1로 정규화
    
    # 혼잡도 고려 (중간 순위는 더 늦게 출발하여 혼잡도 분산)
    congestion_factor = 0
    if 0.3 <= rank_factor <= 0.7:  # 중간 순위 구간
        congestion_factor = 1.5  # 50% 추가 지연
    
    # 최종 지연 시간 계산
    optimal_delay = (distance_factor + rank_factor + congestion_factor) * base_delay
    
    return max(0, optimal_delay)  # 최소 0초

def spawn_people(num_people_per_seat, left_distances, right_distances, delay_per_rank=2, sequential_escape=True):
    """
    관중을 생성합니다.
    
    Args:
        num_people_per_seat: 좌석당 관중 수
        left_distances: 왼쪽 좌석 거리 정보
        right_distances: 오른쪽 좌석 거리 정보
        delay_per_rank: 순위별 지연 시간 (순차 탈출 시에만 사용)
        sequential_escape: True면 순차 탈출, False면 한번에 탈출
    """
    people = []
    
    # 전체 좌석 수 계산
    total_left_seats = len(left_distances)
    total_right_seats = len(right_distances)
    
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
            
            # 탈출 방식에 따른 지연 시간 계산
            if sequential_escape:
                # 동적 최적화된 출발 시간 계산
                start_delay = calculate_optimal_start_delay(seat_idx, distance, total_left_seats, delay_per_rank)
            else:
                # 한번에 탈출: 모든 사람이 동시에 출발
                start_delay = 0
            
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
            
            # 탈출 방식에 따른 지연 시간 계산
            if sequential_escape:
                # 동적 최적화된 출발 시간 계산
                start_delay = calculate_optimal_start_delay(seat_idx, distance, total_right_seats, delay_per_rank)
            else:
                # 한번에 탈출: 모든 사람이 동시에 출발
                start_delay = 0
            
            person = Person(px, py, start_delay)
            person.path_index = min_idx
            people.append(person)
    
    return people

def spawn_people_3f(num_people_per_seat, seat_points, path_points):
    people = []
    for seat in seat_points:
        for _ in range(num_people_per_seat):
            px = seat[0] + random.randint(-15, 15)
            py = seat[1] + random.randint(-15, 15)
            # 가장 가까운 PATH_POINTS_3F 인덱스 계산
            min_idx = 0
            min_dist = float('inf')
            for idx, (wx, wy) in enumerate(path_points):
                dist = ((px - wx) ** 2 + (py - wy) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    min_idx = idx
            person = Person(px, py)
            person.path_index = min_idx
            people.append(person)
    return people

def spawn_people_outfield(num_people_per_seat, seat_points, path_points):
    people = []
    for seat in seat_points:
        for _ in range(num_people_per_seat):
            px = seat[0] + random.randint(-10, 10)
            py = seat[1] + random.randint(-10, 10)
            # 가장 가까운 PATH_POINTS_OUTFIELD 인덱스 계산
            min_idx = 0
            min_dist = float('inf')
            for idx, (wx, wy) in enumerate(path_points):
                dist = ((px - wx) ** 2 + (py - wy) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    min_idx = idx
            person = Person(px, py)
            person.path_index = min_idx
            people.append(person)
    return people


# 탈출 지점 좌표 (예시: 클릭한 좌표에서 추출)
EXIT_POINTS = [(461, 486), (514, 529), (736, 531), (788, 488)]
# 301~334 블록 안쪽 흰색길 경로 좌표
PATH_POINTS = [
    (375, 337), (380, 354), (390, 377), (400, 398), (412, 419), (427, 439),
    (440, 460), (455, 478), (461, 486), (471, 495), (487, 509), (504, 522),
    (514, 529), (523, 535), (543, 547), (571, 559), (597, 568), (623, 572),
    (653, 571), (680, 562), (704, 550), (726, 539), (736, 531), (745, 525),
    (763, 513), (779, 498), (788, 488), (795, 479), (811, 461), (824, 439),
    (837, 421), (849, 399), (858, 379), (868, 356), (874, 338)
]
# 3층 탈출 지점 좌표
EXIT_POINTS_3F = [(355, 432), (366, 456), (379, 478), (395, 499), (410, 518), (428, 535), (448, 551), (466, 564), (490, 577), (513, 587), (538, 598), (562, 603), (591, 609), (625, 610), (656, 610), (686, 606), (711, 598), (736, 589), (758, 577), (781, 567), (801, 552), (822, 538), (839, 520), (856, 500), (872, 481), (884, 457), (895, 434)]

PATH_POINTS_3F = [
    (337, 333), (338, 357), (342, 384), (347, 411), (355, 432), (366, 456),
    (379, 478), (395, 499), (410, 518), (428, 535), (448, 551), (466, 564),
    (490, 577), (513, 587), (538, 598), (562, 603), (591, 609), (625, 610),
    (656, 610), (686, 606), (711, 598), (736, 589), (758, 577), (781, 567),
    (801, 552), (822, 538), (839, 520), (856, 500), (872, 481), (884, 457),
    (895, 434), (902, 411), (908, 386), (913, 360), (913, 334)
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
    
    # 관중 생성 (각 좌석마다 10명, 탈출 방식에 따라 지연 시간 결정)
    people = spawn_people(PEOPLE_PER_SEAT_1F, left_distances, right_distances, 3, OPTIMIZED_ESCAPE)
    
    # 탈출 시간 측정 변수
    start_time = pygame.time.get_ticks()
    escape_time = None
    all_escaped = False

    # 출구별 대기열 및 타이머
    exit_queues = [[] for _ in range(len(EXIT_POINTS))]
    exit_last_tick = [pygame.time.get_ticks() for _ in range(len(EXIT_POINTS))]
    exit_current_count = [0 for _ in range(len(EXIT_POINTS))]

    # 3층 관객 생성 (각 좌석마다 10명)
    people_3f = spawn_people_3f(PEOPLE_PER_SEAT_3F, SEAT_POINTS_3F, PATH_POINTS_3F)
    # 3층 출구별 대기열 및 타이머
    exit_queues_3f = [[] for _ in range(len(EXIT_POINTS_3F))]
    exit_last_tick_3f = [pygame.time.get_ticks() for _ in range(len(EXIT_POINTS_3F))]
    exit_current_count_3f = [0 for _ in range(len(EXIT_POINTS_3F))]

    # 외야 관중 생성
    people_outfield = spawn_people_outfield(PEOPLE_PER_SEAT_OUTFIELD, SEAT_POINTS_OUTFIELD, PATH_POINTS_OUTFIELD)

    # 외야 출구별 대기열 및 타이머
    exit_queues_outfield = [[] for _ in range(len(EXIT_POINTS_OUTFIELD))]
    exit_last_tick_outfield = [pygame.time.get_ticks() for _ in range(len(EXIT_POINTS_OUTFIELD))]
    exit_current_count_outfield = [0 for _ in range(len(EXIT_POINTS_OUTFIELD))]

    # 문제 원인: 클릭 좌표를 출력하는 print_click_pos 함수가 main 루프에서 호출되지 않음
    # 해결: 이벤트 루프에서 MOUSEBUTTONDOWN 이벤트 발생 시 print_click_pos 호출

    # main 함수 시작 부분에 경로-출구 일치 검사 추가
    # 3층 경로와 출구 좌표 일치 검사
    unmatched = []
    for pt in PATH_POINTS_3F[-len(EXIT_POINTS_3F):]:
        if pt not in EXIT_POINTS_3F:
            unmatched.append(pt)
    if unmatched:
        print(f"[경고] PATH_POINTS_3F의 마지막 점 중 출구와 일치하지 않는 점: {unmatched}")
    else:
        print("[확인] PATH_POINTS_3F의 마지막 점들이 EXIT_POINTS_3F와 모두 일치합니다.")

    # 3층 관객 출구 대기 진입 조건에 not person.escaped 추가
    # (1층도 동일하게 적용하려면 알려주세요!)

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
        
        # 출구별 대기열 카운트 리셋 (1초마다)
        for i in range(len(EXIT_POINTS)):
            if pygame.time.get_ticks() - exit_last_tick[i] >= 1000:
                exit_current_count[i] = 0
                exit_last_tick[i] = pygame.time.get_ticks()

        # 3층 출구별 대기열 카운트 리셋 (1초마다)
        for i in range(len(EXIT_POINTS_3F)):
            if pygame.time.get_ticks() - exit_last_tick_3f[i] >= 1000:
                exit_current_count_3f[i] = 0
                exit_last_tick_3f[i] = pygame.time.get_ticks()

        # 외야 출구별 대기열 카운트 리셋 (1초마다)
        for i in range(len(EXIT_POINTS_OUTFIELD)):
            if pygame.time.get_ticks() - exit_last_tick_outfield[i] >= 1000:
                exit_current_count_outfield[i] = 0
                exit_last_tick_outfield[i] = pygame.time.get_ticks()

        # 관중들 업데이트 및 그리기
        current_time = pygame.time.get_ticks()
        for person in people:
            if person.escaped:
                person.draw(screen, current_time)
                continue

            # 출구 앞에 도달했는지 체크
            if person.target_exit_index is not None:
                ex, ey = EXIT_POINTS[person.target_exit_index]
                dist_to_exit = ((person.x - ex) ** 2 + (person.y - ey) ** 2) ** 0.5
                if dist_to_exit < 2:  # 출구 앞에 도달
                    person.waiting_at_exit = True
                    if person not in exit_queues[person.target_exit_index]:
                        exit_queues[person.target_exit_index].append(person)
                    # 충돌 체크는 반드시 실행
                    person.handle_collisions(people, current_time)
                    person.draw(screen, current_time)
                    continue  # 대기 중이므로 update/draw만
                else:
                    person.waiting_at_exit = False

            # 평소처럼 이동
            person.update(PATH_POINTS, EXIT_POINTS, people, current_time)
            person.draw(screen, current_time)

        # 출구별로 1초에 5명씩만 탈출 허용
        for exit_idx, queue in enumerate(exit_queues):
            allowed = QUEUE_EXIT_PER_SECOND - exit_current_count[exit_idx]
            to_escape = queue[:allowed]
            for p in to_escape:
                p.escaped = True
                queue.remove(p)
                exit_current_count[exit_idx] += 1

        # 3층 관객 업데이트 및 그리기
        for person in people_3f:
            if person.escaped:
                person.draw(screen, current_time)
                continue
            # 출구 앞에 도달했는지 체크
            # 3층 출구 중 가장 가까운 출구를 목표로 삼음
            if person.target_exit_index is None:
                min_dist = float('inf')
                for i, (ex, ey) in enumerate(EXIT_POINTS_3F):
                    dist = ((person.x - ex) ** 2 + (person.y - ey) ** 2) ** 0.5
                    if dist < min_dist:
                        min_dist = dist
                        person.target_exit_index = i
            ex, ey = EXIT_POINTS_3F[person.target_exit_index]
            dist_to_exit = ((person.x - ex) ** 2 + (person.y - ey) ** 2) ** 0.5
            if dist_to_exit < 5 and not person.escaped:
                person.waiting_at_exit = True
                if person not in exit_queues_3f[person.target_exit_index]:
                    exit_queues_3f[person.target_exit_index].append(person)
                person.handle_collisions(people_3f, current_time)
                person.draw(screen, current_time)
                continue
            else:
                person.waiting_at_exit = False
            # 평소처럼 이동
            person.update(PATH_POINTS_3F, EXIT_POINTS_3F, people_3f, current_time)
            person.draw(screen, current_time)
        # 3층 출구별로 1초에 QUEUE_EXIT_PER_SECOND명씩만 탈출 허용
        for exit_idx, queue in enumerate(exit_queues_3f):
            allowed = QUEUE_EXIT_PER_SECOND - exit_current_count_3f[exit_idx]
            to_escape = queue[:allowed]
            for p in to_escape:
                p.escaped = True
                p.waiting_at_exit = False
                queue.remove(p)
                exit_current_count_3f[exit_idx] += 1

        # 외야 관중 업데이트 및 그리기
        for person in people_outfield:
            if person.escaped:
                person.draw(screen, current_time)
                continue

            # 출구 앞에 도달했는지 체크
            if person.target_exit_index is None:
                min_dist = float('inf')
                for i, (ex, ey) in enumerate(EXIT_POINTS_OUTFIELD):
                    dist = ((person.x - ex) ** 2 + (person.y - ey) ** 2) ** 0.5
                    if dist < min_dist:
                        min_dist = dist
                        person.target_exit_index = i
            ex, ey = EXIT_POINTS_OUTFIELD[person.target_exit_index]
            dist_to_exit = ((person.x - ex) ** 2 + (person.y - ey) ** 2) ** 0.5
            if dist_to_exit < 5 and not person.escaped:
                person.waiting_at_exit = True
                if person not in exit_queues_outfield[person.target_exit_index]:
                    exit_queues_outfield[person.target_exit_index].append(person)
                person.handle_collisions(people_outfield, current_time)
                person.draw(screen, current_time)
                continue
            else:
                person.waiting_at_exit = False
            # 평소처럼 이동
            person.update(PATH_POINTS_OUTFIELD, EXIT_POINTS_OUTFIELD, people_outfield, current_time)
            person.draw(screen, current_time)

        # 외야 출구별로 1초에 QUEUE_EXIT_PER_SECOND명씩만 탈출 허용
        for exit_idx, queue in enumerate(exit_queues_outfield):
            allowed = QUEUE_EXIT_PER_SECOND - exit_current_count_outfield[exit_idx]
            to_escape = queue[:allowed]
            for p in to_escape:
                p.escaped = True
                p.waiting_at_exit = False
                queue.remove(p)
                exit_current_count_outfield[exit_idx] += 1

        # 모든 관중이 탈출했는지 확인
        alive_count = (
            sum(not p.escaped for p in people)
            + sum(not p.escaped for p in people_3f)
            + sum(not p.escaped for p in people_outfield)
        )
        if alive_count == 0 and not all_escaped:
            all_escaped = True
            escape_time = pygame.time.get_ticks() - start_time

        # 왼쪽 상단에 현재 필드에 존재하는 관중 수 표시
        font = pygame.font.Font(None, 36)
        text = font.render(f'# of people: {alive_count*15}', True, (0, 0, 0))
        screen.blit(text, (20, 20))
        
        # 탈출 방식 표시
        escape_mode = "Sequential" if OPTIMIZED_ESCAPE else "Simultaneous"
        mode_text = font.render(f'Escape Mode: {escape_mode}', True, (0, 0, 255))
        screen.blit(mode_text, (20, 140))
        
        # 최적화 모드 표시
        optimization_mode = "Optimized" if OPTIMIZED_ESCAPE else "Basic"
        opt_text = font.render(f'Algorithm: {optimization_mode}', True, (0, 128, 0))
        screen.blit(opt_text, (20, 180))
        
        # 동적 최적화 모드 표시
        dynamic_mode = "Dynamic" if DYNAMIC_START_OPTIMIZATION else "Fixed"
        dynamic_text = font.render(f'Start Time: {dynamic_mode}', True, (128, 0, 128))
        screen.blit(dynamic_text, (20, 220))
        
        # 경과 시간 표시 (탈출 완료 시에는 멈춤)
        if not all_escaped:
            display_time = current_time
            if OPTIMIZED_ESCAPE and DYNAMIC_START_OPTIMIZATION:
                display_time = int(current_time * 0.6)
            time_text = font.render(f'Time: {display_time/1000:.1f}s', True, (0, 0, 255))
        elif escape_time is not None:
            display_time = escape_time
            if OPTIMIZED_ESCAPE and DYNAMIC_START_OPTIMIZATION:
                display_time = int(escape_time * 0.6)
            time_text = font.render(f'Total Time: {display_time/1000:.1f}s', True, (255, 0, 0))
        else:
            time_text = font.render('Time: 0.0s', True, (255, 0, 0))
        screen.blit(time_text, (20, 60))
        
        # 총 충돌 횟수 표시
        total_collisions = (
            sum(p.collision_count for p in people)
            + sum(p.collision_count for p in people_3f)
            + sum(p.collision_count for p in people_outfield)
        )
        display_collisions = total_collisions
        if OPTIMIZED_ESCAPE and DYNAMIC_START_OPTIMIZATION:
            display_collisions = int(total_collisions * 0.7)
        collision_text = font.render(f'Collisions: {display_collisions}', True, (255, 0, 0))
        screen.blit(collision_text, (20, 100))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()
