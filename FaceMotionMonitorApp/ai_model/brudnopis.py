import cv2
import mediapipe as mp
import math

def get_unique(c):
    unique_landmarks = set()
    for connection in c:
        if isinstance(connection, tuple):
            unique_landmarks.update(connection)
        else:
            unique_landmarks.add(connection)
    return list(unique_landmarks)

mp_face_mesh = mp.solutions.face_mesh

def get_points():
    connections = [
        mp_face_mesh.FACEMESH_LIPS,
        mp_face_mesh.FACEMESH_LEFT_EYEBROW,
        mp_face_mesh.FACEMESH_RIGHT_EYEBROW,
        mp_face_mesh.FACEMESH_LEFT_EYE,
        mp_face_mesh.FACEMESH_RIGHT_EYE,
        mp_face_mesh.FACEMESH_IRISES]


    landmark_connections = set().union(*connections)

    additional_landmarks = [206, 203, 216, 212, 423, 426, 436, 432]
    landmark_connections.update((landmark, landmark) for landmark in additional_landmarks)

    additional_connections = [
        (203, 206),
        (206, 216),
        (216, 212),
        (423, 426),
        (426, 436),
        (436, 432)]

    landmark_connections.update(additional_connections)
    landmarks = get_unique(landmark_connections)

    return landmark_connections, landmarks

def face_center(points):
    sum_x, sum_y = 0, 0

    for landmark_list in points:
        for landmark in landmark_list:
            landmark_index, landmark_x, landmark_y = landmark
            sum_x += landmark_x
            sum_y += landmark_y

    center_x = sum_x / len(points[0])
    center_y = sum_y / len(points[0])

    return center_x, center_y


mp_face_mesh = mp.solutions.face_mesh


def iris_width(landmark_points):
    left = [469, 471]
    right = [474, 476]
    x_landmarks = {}
    y_landmarks = {}
    for landmark_list in landmark_points:
        for landmark in landmark_list:
            landmark_index, x_landmark, y_landmark = landmark
            if landmark_index in left or landmark_index in right:
                x_landmarks.update({landmark_index : x_landmark})
                y_landmarks.update({landmark_index : y_landmark})
    left_width = math.sqrt((x_landmarks.get(469) - x_landmarks.get(471))**2 + (y_landmarks.get(469) - y_landmarks.get(471))**2)
    right_width = math.sqrt((x_landmarks.get(474) - x_landmarks.get(476)) ** 2 + (y_landmarks.get(474) - y_landmarks.get(476)) ** 2)
    width = (left_width + right_width)/2
    return width

def calculate_distance(landmark_points):
    x_center, y_center = face_center(landmark_points)
    width = iris_width(landmark_points)
    k = width/11 # 11 mm - average width of a human iris, k is a scale

    # dictionary - the key is the index of a point, value is its distance from the center
    distances = {}
    for landmark_list in landmark_points:
        for landmark in landmark_list:
            landmark_index, x_landmark, y_landmark = landmark
            distance = math.sqrt((x_landmark - x_center) ** 2 + (y_landmark - y_center) ** 2)
            distances[landmark_index] = distance*k
    return distances   #distances in mm


landmark_connections, landmarks = get_points()
cap = cv2.VideoCapture(0)
with mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True) as face_mesh:
    while True:
        ret, img = cap.read()
        if not ret:
            break

        results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if results.multi_face_landmarks:
            for face_landmark in results.multi_face_landmarks:
                lms = face_landmark.landmark
                d = {}
                for index in landmarks:
                    x = int(lms[index].x * img.shape[1])
                    y = int(lms[index].y * img.shape[0])
                    d[index] = (x, y)
                    norm_x = lms[index].x
                    norm_y = lms[index].y

                    # this info will be passed to the DB, for now i just print it

                    print(f"Landmark {index}: ({norm_x}, {norm_y})")

                # in the final project, landmarks will not be drawn on the recording, but for now, I'm leaving this part

                for index in landmarks:
                    cv2.circle(img, (d[index][0], d[index][1]), 2, (0, 255, 0), -1)
                for conn in list(landmark_connections):
                    cv2.line(img, (d[conn[0]][0], d[conn[0]][1]),
                             (d[conn[1]][0], d[conn[1]][1]), (0, 0, 255), 1)

                left_iris = [468, 469, 470, 471]  # indexes of irises: 468 - top, 469 - right, 470 - bottom, 471 - left
                right_iris = [473, 474, 475, 476] # 473 - top, 474 - right - 475 - bottom, 476 - left

                for index in left_iris + right_iris:
                    x = int(lms[index].x * img.shape[1])
                    y = int(lms[index].y * img.shape[0])
                    cv2.circle(img, (x, y), 2, (255, 0, 0), -1)

        cv2.imshow('frame', cv2.flip(img, 1))

        # press q if you want to close it
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
