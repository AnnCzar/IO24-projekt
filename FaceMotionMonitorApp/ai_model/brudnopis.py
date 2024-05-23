import cv2
import mediapipe as mp
import math
import numpy as np

mp_face_mesh = mp.solutions.face_mesh


class VideoProcessor:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, refine_landmarks=True)
        self.landmark_connections, self.landmarks = self.get_points()
        self.freeze_frame = None  # for freezing the video
        self.is_frozen = False

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
        for landmark in points:
            landmark_index, landmark_x, landmark_y = landmark
            sum_x += landmark_x
            sum_y += landmark_y
        center_x = sum_x / len(points)
        center_y = sum_y / len(points)
        return center_x, center_y

    def get_points(self):
        connections = [
            mp_face_mesh.FACEMESH_LIPS,
            mp_face_mesh.FACEMESH_LEFT_EYEBROW,
            mp_face_mesh.FACEMESH_RIGHT_EYEBROW,
            mp_face_mesh.FACEMESH_LEFT_EYE,
            mp_face_mesh.FACEMESH_RIGHT_EYE,
            mp_face_mesh.FACEMESH_IRISES
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

    def iris_width(self, landmark_points):
        left = [469, 471]
        right = [474, 476]
        x_landmarks = {}
        y_landmarks = {}
        for landmark in landmark_points:
            landmark_index, x_landmark, y_landmark = landmark
            if landmark_index in left or landmark_index in right:
                x_landmarks.update({landmark_index: x_landmark})
                y_landmarks.update({landmark_index: y_landmark})
        left_width = math.sqrt(
            (x_landmarks.get(469) - x_landmarks.get(471)) ** 2 + (y_landmarks.get(469) - y_landmarks.get(471)) ** 2)
        right_width = math.sqrt(
            (x_landmarks.get(474) - x_landmarks.get(476)) ** 2 + (y_landmarks.get(474) - y_landmarks.get(476)) ** 2)
        width = (left_width + right_width) / 2
        return width

    def calculate_distance(self, landmark_points):
        x_center, y_center = self.face_center(landmark_points)
        width = self.iris_width(landmark_points)
        k = width / 11  # 11 mm - average width of a human iris, k is a scale
        distances = {}
        for landmark in landmark_points:
            landmark_index, x_landmark, y_landmark = landmark
            distance = math.sqrt((x_landmark - x_center) ** 2 + (y_landmark - y_center) ** 2)
            distances[landmark_index] = distance
        return distances

    def process_frame(self):
        ret, img = self.cap.read()
        if not ret:
            return None, None

        results = self.face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks:
            for face_landmark in results.multi_face_landmarks:
                lms = face_landmark.landmark
                d = {}
                landmark_list = []
                land_list = []
                for index in self.landmarks:
                    x = int(lms[index].x * img.shape[1])
                    y = int(lms[index].y * img.shape[0])
                    d[index] = (x, y)
                    norm_x = lms[index].x
                    norm_y = lms[index].y
                    landmark_list.append((index, norm_x, norm_y))

                land_list.append(landmark_list)
                print(land_list)
                x_center, y_center = self.face_center(landmark_list)
                distances = self.calculate_distance(landmark_list)

                cv2.circle(img, (int(x_center * img.shape[1]), int(y_center * img.shape[0])), 2, (255, 0, 0), -1)
                for index in self.landmarks:
                    cv2.circle(img, (d[index][0], d[index][1]), 2, (0, 255, 0), -1)
                for conn in list(self.landmark_connections):
                    cv2.line(img, (d[conn[0]][0], d[conn[0]][1]),
                             (d[conn[1]][0], d[conn[1]][1]), (0, 0, 255), 1)

                print(f"Frame center: ({x_center}, {y_center}), Distances: {distances}")

        ret, buffer = cv2.imencode('.jpg', img)
        return img, buffer.tobytes()

    # for capturing the photo
    def capture_photo(self):  # almost everything is the same as in the process frame,
        if self.freeze_frame is not None:
            img = self.freeze_frame

            results = self.face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            if results.multi_face_landmarks:
                for face_landmark in results.multi_face_landmarks:
                    lms = face_landmark.landmark
                    d = {}
                    landmark_list = []
                    for index in self.landmarks:
                        x = int(lms[index].x * img.shape[1])
                        y = int(lms[index].y * img.shape[0])
                        d[index] = (x, y)
                        norm_x = lms[index].x
                        norm_y = lms[index].y
                        landmark_list.append((index, norm_x, norm_y))

                    x_center, y_center = self.face_center(landmark_list)
                    distances = self.calculate_distance(landmark_list)

                    cv2.circle(img, (int(x_center * img.shape[1]), int(y_center * img.shape[0])), 2, (255, 0, 0), -1)
                    for index in self.landmarks:
                        cv2.circle(img, (d[index][0], d[index][1]), 2, (0, 255, 0), -1)
                    for conn in list(self.landmark_connections):
                        cv2.line(img, (d[conn[0]][0], d[conn[0]][1]),
                                 (d[conn[1]][0], d[conn[1]][1]), (0, 0, 255), 1)

                    print(f"Photo center: ({x_center}, {y_center}), Distances: {distances}")

            ret, buffer = cv2.imencode('.jpg', img)
            return img, buffer.tobytes()

    def display_video(self):
        while True:
            if not self.is_frozen:
                img, img_bytes = self.process_frame()
                if img is None:
                    break
                self.freeze_frame = img

            decoded_img = cv2.imdecode(np.frombuffer(cv2.imencode('.jpg', self.freeze_frame)[1], np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('frame', cv2.flip(decoded_img, 1))

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('p'):
                self.is_frozen = not self.is_frozen
                if self.is_frozen:
                    self.capture_photo()
                else:
                    self.freeze_frame = None

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    processor = VideoProcessor()
    processor.display_video()
