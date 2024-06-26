import cv2
import mediapipe as mp
import math

mp_face_mesh = mp.solutions.face_mesh


class VideoProcessor:
    def __init__(self):
        """
        Initialize the VideoProcessor with MediaPipe FaceMesh and landmark connections.
        """
        self.face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, refine_landmarks=True)
        self.landmark_connections, self.landmarks = self.get_points()

    def __del__(self):
        """
        Close the FaceMesh instance upon deletion.
        """
        self.face_mesh.close()

    def get_unique(self, c):
        """
        Get a list of unique landmarks from connections.

        Parameters:
        c (list): List of connections (tuples or single values).

        Returns:
        list: List of unique landmarks.
        """
        unique_landmarks = set()
        for connection in c:
            if isinstance(connection, tuple):
                unique_landmarks.update(connection)
            else:
                unique_landmarks.add(connection)
        return list(unique_landmarks)

    def face_center(self, points):
        """
        Calculate the center of the face based on provided landmarks.

        Parameters:
        points (list): List of tuples containing landmark index and coordinates.

        Returns:
        tuple: Center coordinates (x, y).
        """
        sum_x, sum_y = 0, 0
        for landmark in points:
            landmark_index, landmark_x, landmark_y = landmark
            sum_x += landmark_x
            sum_y += landmark_y
        center_x = sum_x / len(points)
        center_y = sum_y / len(points)
        return center_x, center_y

    def get_points(self):
        """
        Retrieve the points of interest (landmarks) and connections.

        Returns:
        tuple: Set of landmark connections and list of unique landmarks.
        """
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
        """
        Calculate the average width of the irises.

        Parameters:
        landmark_points (list): List of tuples containing landmark index and coordinates.

        Returns:
        float: Average iris width.
        """
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
        """
        Calculate the distances of landmarks from the center of the face.

        Parameters:
        landmark_points (list): List of tuples containing landmark index and coordinates.

        Returns:
        dict: Dictionary of landmark distances from the center.
        """
        x_center, y_center = self.face_center(landmark_points)
        width = self.iris_width(landmark_points)
        k = width / 11  # 11 mm - average width of a human iris, k is a scale
        distances = {}
        for landmark in landmark_points:
            landmark_index, x_landmark, y_landmark = landmark
            distance = math.sqrt((x_landmark - x_center) ** 2 + (y_landmark - y_center) ** 2) / k
            distances[landmark_index] = distance
        return distances

    def calculate_distance_mouth(self, landmark_points):
        """
        Calculate the distance between the corners of the mouth.

        Parameters:
        landmark_points (list): List of tuples containing landmark index and coordinates.

        Returns:
        float: Distance between the mouth corners.
        """
        width = self.iris_width(landmark_points)
        k = width / 11  # scale
        x = []
        y = []
        for landmark in landmark_points:
            landmark_index, x_landmark, y_landmark = landmark
            if landmark_index == 61 or landmark_index == 291:
                x.append(x_landmark)
                y.append(y_landmark)
        distance = math.sqrt((x[0] - x[1]) ** 2 + (y[0] - y[1]) ** 2) / k
        return distance

    def process_frame(self, img):
        """
        Process a single frame to detect face landmarks and draw annotations.

        Parameters:
        img (numpy.ndarray): The input image/frame.

        Returns:
        tuple: Processed image and its buffer.
        """
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
                x_center, y_center = self.face_center(landmark_list)
                distances = self.calculate_distance(landmark_list)

                cv2.circle(img, (int(x_center * img.shape[1]), int(y_center * img.shape[0])), 2, (255, 0, 0), -1)
                for index in self.landmarks:
                    cv2.circle(img, (d[index][0], d[index][1]), 2, (0, 255, 0), -1)
                for conn in list(self.landmark_connections):
                    cv2.line(img, (d[conn[0]][0], d[conn[0]][1]),
                             (d[conn[1]][0], d[conn[1]][1]), (0, 0, 255), 1)

        ret, buffer = cv2.imencode('.jpg', img)
        return img, buffer.tobytes()

    def process_video(self, video_file_path):
        """
        Process a video file to detect face landmarks and collect frame data.

        Parameters:
        video_file_path (str): Path to the input video file.

        Returns:
        tuple: Dictionary of frame data, frame with max distance, and landmark list.
        """
        cap = cv2.VideoCapture(video_file_path)

        frame_count = 0
        all_frames_data = {}

        while cap.isOpened():
            ret, img = cap.read()
            if not ret:
                break
            frame_count += 1
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(image_rgb)

            frame_data = {
                'timestamp': timestamp,
                'x_center': None,
                'y_center': None,
                'landmarks': {}
            }

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
                    x_center, y_center = self.face_center(landmark_list)
                    distances = self.calculate_distance(landmark_list)

                    frame_data['x_center'] = x_center
                    frame_data['y_center'] = y_center
                    frame_data['landmarks'] = {index: distances[index] for index, _, _ in landmark_list}

                    for index in self.landmarks:
                        cv2.circle(img, (d[index][0], d[index][1]), 2, (0, 255, 0), -1)
                    for conn in list(self.landmark_connections):
                        cv2.line(img, (d[conn[0]][0], d[conn[0]][1]),
                                 (d[conn[1]][0], d[conn[1]][1]), (0, 0, 255), 1)

            all_frames_data[frame_count] = frame_data

        cap.release()
        return all_frames_data, self.get_max_distance_for_rec(all_frames_data), landmark_list

    def capture_photo(self, img):
        """
        Capture a photo, detect face landmarks, and draw annotations.

        Parameters:
        img (numpy.ndarray): The input image.

        Returns:
        tuple: Processed image, buffer, landmark list, distances, x_center, and y_center.
        """
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

        ret, buffer = cv2.imencode('.jpg', img)
        return img, buffer.tobytes(), landmark_list, distances, x_center, y_center

    def get_max_distance_for_rec(self, frame_data_list):
        """
        Get the frame number with the maximum distance between mouth corners.

        Parameters:
        frame_data_list (dict): Dictionary of frame data.

        Returns:
        int: Frame number with the maximum distance.
        """
        landmark_index = [61, 291]
        max_distance = -1
        frame_number_with_max_distance = None

        for frame_number, frame_data in frame_data_list.items():
            if all(index in frame_data['landmarks'] for index in landmark_index):
                distance = max(frame_data['landmarks'][index] for index in landmark_index)
                if distance > max_distance:
                    max_distance = distance
                    frame_number_with_max_distance = frame_number

        return frame_number_with_max_distance


if __name__ == "__main__":
    processor = VideoProcessor()
    processor.display_video()
