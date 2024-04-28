import cv2
import mediapipe as mp


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
        mp_face_mesh.FACEMESH_RIGHT_EYE]


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

        cv2.imshow('frame', cv2.flip(img, 1))

        # press q if you want to close it
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
