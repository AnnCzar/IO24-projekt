import cv2
import mediapipe as mp
import math

mp_face_mesh = mp.solutions.face_mesh

class VideoProcessor:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True)
        self.landmark_connections, self.landmarks = self.get_points()

    def __del__(self):
        self.cap.release()
        self.face_mesh.close()

    def get_unique(self, c):
        unique_landmarks = set()
        for connection in c:
            if isinstance(connection, tuple):
                unique_landmarks.update(connection)
            else:
                unique_landmarks.add(connection)
        return list(unique_landmarks)

    def face_center(self, points):
        sum_x, sum_y = 0, 0
        for landmark_list in points:
            for landmark in landmark_list:
                landmark_index, landmark_x, landmark_y = landmark
                sum_x += landmark_x
                sum_y += landmark_y
        center_x = sum_x / len(points[0])
        center_y = sum_y / len(points[0])
        return center_x, center_y

    def get_points(self):
        connections = [
            mp_face_mesh.FACEMESH_LIPS,
            mp_face_mesh.FACEMESH_LEFT_EYEBROW,
            mp_face_mesh.FACEMESH_RIGHT_EYEBROW,
            mp_face_mesh.FACEMESH_LEFT_EYE,
            mp_face_mesh.FACEMESH_RIGHT_EYE
        ]
        landmark_connections = set().union(*connections)
        additional_landmarks = [206, 203, 216, 212, 423, 426, 436, 432]
        landmark_connections.update((landmark, landmark) for landmark in additional_landmarks)
        additional_connections = [
            (203, 206),
            (206, 216),
            (216, 212),
            (423, 426),
            (426, 436),
            (436, 432)
        ]
        landmark_connections.update(additional_connections)
        landmarks = self.get_unique(landmark_connections)
        return landmark_connections, landmarks

    def calculate_distance(self, landmark_points):
        x_center, y_center = self.face_center(landmark_points)
        distances = {}
        for landmark_list in landmark_points:
            for landmark in landmark_list:
                landmark_index, x_landmark, y_landmark = landmark
                distance = math.sqrt((x_landmark - x_center) ** 2 + (y_landmark - y_center) ** 2)
                distances[landmark_index] = distance
        return distances

    def process_frame(self):
        ret, img = self.cap.read()
        if not ret:
            return None

        results = self.face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks:
            for face_landmark in results.multi_face_landmarks:
                lms = face_landmark.landmark
                d = {}
                land_list = []
                line = []
                for index in self.landmarks:
                    x = int(lms[index].x * img.shape[1])
                    y = int(lms[index].y * img.shape[0])
                    d[index] = (x, y)
                    norm_x = lms[index].x
                    norm_y = lms[index].y
                    line.append((index, norm_x, norm_y))

                # printing landmarks just for now
                land_list.append(line)
                print(land_list)
                x_center, y_center = self.face_center(land_list)
                print(x_center, y_center)
                distances = self.calculate_distance(land_list)
                print(distances)

                cv2.circle(img, (int(x_center * img.shape[1]), int(y_center * img.shape[0])), 2, (255, 0, 0), -1)
                for index in self.landmarks:
                    cv2.circle(img, (d[index][0], d[index][1]), 2, (0, 255, 0), -1)
                for conn in list(self.landmark_connections):
                    cv2.line(img, (d[conn[0]][0], d[conn[0]][1]),
                             (d[conn[1]][0], d[conn[1]][1]), (0, 0, 255), 1)

        # it writes a JPEG-compressed image into a memory buffer (RAM) instead of to disk
        ret, buffer = cv2.imencode('.jpg', img)
        return buffer.tobytes()  # changes the frame into bytes

    def display_video(self):
        while True:
            img = self.process_frame()
            if img is None:
                break
            cv2.imshow('frame', cv2.flip(img, 1))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
