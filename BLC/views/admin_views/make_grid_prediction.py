import cv2
from mmdet.apis import inference_detector



def draw_grid_line(frame, grid_x, grid_y):
    dst_frame = frame.copy()
    line_color = (0, 255, 255)
    h, w, _ = dst_frame.shape

    # 그리드 스타일 적용
    line_color = (0, 0, 255)  # 그리드 선의 색상 (파란색 예시)
    line_thickness = 1  # 그리드 선의 두께

    grid_line_x = w//grid_x  # 그리드의 크기 (가로와 세로 방향 간격)
    grid_line_y = h//grid_y
    # 그리드 그리기
    for x in range(0, h, grid_line_x):
        cv2.line(dst_frame, (x, 0), (x, h), line_color, line_thickness)
    for y in range(0, h, grid_line_y):
        cv2.line(dst_frame, (0, y), (w, y), line_color, line_thickness)
    
    return dst_frame

def make_grid_predict(model, frame, score_thr):
    result = inference_detector(model, frame)
    res = [
        {model.CLASSES[idx]: box[:4]}
        for idx, boxes in enumerate(result)
        if boxes.any()
        for box in boxes
        if box[-1] > score_thr
    ]
    return res

def make_grid_frame(frame, grid_x, grid_y):
    results = []
    h, w, _ = frame.shape
    x = w // grid_x
    y = h // grid_y
    point_y = 0
    for j in range(grid_y):
        point_x = 0
        for i in range(grid_x):
            grid_frame = frame[point_y:point_y+y if point_y+y < h else h-1, point_x:point_x+x if point_x+x < w else w-1]
            results.append(grid_frame)
            point_x += x
        point_y += y

    return results

