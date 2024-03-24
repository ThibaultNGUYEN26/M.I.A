# import cv2
# import numpy as np
# import face_recognition
# import os


# path = 'recognition_images'
# images = []
# class_names = []
# my_list = os.listdir(path)

# for cl in my_list:
#     cur_img = cv2.imread(f'{path}/{cl}')
#     images.append(cur_img)
#     class_names.append(os.path.splitext(cl)[0])


# def find_encoding(images):
#     encode_list = []
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encode_list.append(encode)
#     return encode_list


# encode_list_known = find_encoding(images)
# print('Encoding Complete')

# cap = cv2.VideoCapture(0)

# test = True
# while test:
#     success, img = cap.read()
#     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#     faces_curframe = face_recognition.face_locations(imgS)
#     encodes_cur_frame = face_recognition.face_encodings(imgS, faces_curframe)

#     for encodeFace, faceLoc in zip(encodes_cur_frame, faces_curframe):
#         matches = face_recognition.compare_faces(encode_list_known, encodeFace)
#         faceDis = face_recognition.face_distance(encode_list_known, encodeFace)
#         # print(faceDis)
#         match_index = np.argmin(faceDis)

#         if matches[match_index]:
#             name = class_names[match_index].upper()
#             print(name)
#             y1, x2, y2, x1 = faceLoc
#             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#             cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
#             cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

#             if name == "THIBAULT":
#                 test = False

#         else:
#             name = "INCONNU"
#             print(name)
#             y1, x2, y2, x1 = faceLoc
#             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#             cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
#             cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)


#     cv2.imshow('Webcam', img)
#     cv2.waitKey(1)


# import cv2
# import dlib
# import face_recognition

# image_thibault = face_recognition.load_image_file('C:/Users/Thibault/Documents/mia/recognition_images/thibault.jpg')
# face_encoding = face_recognition.face_encodings(image_thibault)[0]

# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# while True:
#     gray_thibault = cv2.cvtColor(image_thibault, cv2.COLOR_BGR2GRAY)

#     faces_thibault = detector(gray_thibault)
#     for face_thibault in faces_thibault:
#         x1 = face_thibault.left()
#         y1 = face_thibault.top()
#         x2 = face_thibault.right()
#         y2 = face_thibault.bottom()
#         # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

#         landmarks = predictor(gray_thibault, face_thibault)

#         for n in range(0, 68):
#             x = landmarks.part(n).x
#             y = landmarks.part(n).y
#             cv2.circle(image_thibault, (x, y), 3, (255, 0, 0), 1)


# cap = cv2.VideoCapture(0)

# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# while True:
#     _, frame = cap.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     faces = detector(gray)
#     for face in faces:
#         x1 = face.left()
#         y1 = face.top()
#         x2 = face.right()
#         y2 = face.bottom()
#         # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

#         landmarks = predictor(gray, face)

#         for n in range(0, 68):
#             x = landmarks.part(n).x
#             y = landmarks.part(n).y
#             cv2.circle(frame, (x, y), 3, (255, 0, 0), 1)


#     cv2.imshow("Frame", frame)

#     results = face_encoding.compare_faces([face_encoding], )
#     if results[0]:
#         print("Wesh c'est la même tête.")
#     else:
#         print("Tête inconnue.")

#     key = cv2.waitKey(1)
#     if key == 27:
#         break




import cv2
import dlib
import PIL.Image
import numpy as np
from imutils import face_utils
import argparse
from pathlib import Path
import os
import ntpath


print('[INFO] Starting System...')
print('[INFO] Importing pretrained model...')
pose_predictor_68_point = dlib.shape_predictor('pretrained_model/shape_predictor_68_face_landmarks.dat')
pose_predictor_5_point = dlib.shape_predictor('pretrained_model/shape_predictor_5_face_landmarks.dat')
face_encoder = dlib.face_recognition_model_v1("pretrained_model/dlib_face_recognition_resnet_model_v1.dat")
face_detector = dlib.get_frontal_face_detector()


def transform(image, face_locations):
    coord_faces = []
    for face in face_locations:
        rect = face.top(), face.right(), face.bottom(), face.left()
        coord_face = max(rect[0], 0), min(rect[1], image.shape[1]), min(rect[2], image.shape[0]), max(rect[3], 0)
        coord_faces.append(coord_face)
    return coord_faces


def encode_face(image):
    face_locations = face_detector(image, 1)
    face_encoding_list = []
    landmarks_list = []
    for face_location in face_locations:
        shape = pose_predictor_68_point(image, face_location)
        face_encoding_list.append(np.array(face_encoder.compute_face_descriptor(image, shape, num_jitters=1)))
        shape = face_utils.shape_to_np(shape)
        landmarks_list.append(shape)
    face_locations = transform(image, face_locations)
    return face_encoding_list, face_locations, landmarks_list


def easy_face_reco(frame, known_face_encodings, known_face_names):
    # global test
    rgb_small_frame = frame[:, :, ::-1]
    # ENCODING FACE
    face_encodings_list, face_locations_list, landmarks_list = encode_face(rgb_small_frame)
    face_names = []
    for face_encoding in face_encodings_list:
        if len(face_encoding) == 0:
            return np.empty((0))
        # CHECK DISTANCE BETWEEN KNOWN FACES AND FACES DETECTED
        vectors = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
        tolerance = 0.6
        result = []
        for vector in vectors:
            if vector <= tolerance:
                result.append(True)
            else:
                result.append(False)
        if True in result:
            first_match_index = result.index(True)
            name = known_face_names[first_match_index]
        else:
            name = "Inconnu"
        face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations_list, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)
        cv2.rectangle(frame, (left, bottom + 40), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 30, bottom + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    for shape in landmarks_list:
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (255, 0, 255), -1)


if __name__ == '__main__':
    test = True

    print('[INFO] Importing faces...')
    face_to_encode_path = ['recognition_images/thibault.jpg', 'recognition_images/salome.jpg']
    known_face_encodings = []
    for face_to_encode_path in face_to_encode_path:
        image = PIL.Image.open(face_to_encode_path)
        image = np.array(image)
        face_encoded = encode_face(image)[0][0]
        known_face_encodings.append(face_encoded)
    known_face_names = ['Thibault', 'Salome']
    print('[INFO] Faces well imported')

    print('[INFO] Starting Webcam...')
    video_capture = cv2.VideoCapture(0)
    print('[INFO] Webcam well started')
    print('[INFO] Detecting...')
    while test:
        ret, frame = video_capture.read()
        easy_face_reco(frame, known_face_encodings, known_face_names)

        cv2.imshow('Reconnaissance Faciale', frame)

        rgb_small_frame = frame[:, :, ::-1]
        # ENCODING FACE
        face_encodings_list, face_locations_list, landmarks_list = encode_face(rgb_small_frame)
        face_names = []
        for face_encoding in face_encodings_list:
            vectors = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
            tolerance = 0.6
            result = []
            for vector in vectors:
                if vector <= tolerance:
                    result.append(True)
                else:
                    result.append(False)
            if True in result:
                first_match_index = result.index(True)
                name = known_face_names[first_match_index]
                if name == 'Thibault':
                    print('[INFO] Stopping System')
                    video_capture.release()
                    cv2.destroyAllWindows()
                    test = False
            else:
                name = "Inconnu"
            face_names.append(name)
        
        key = cv2.waitKey(1)
        if key == 27:
            break

return test



if __name__ == '__main__':
    test = True

    args = parser.parse_args()

    face_to_encode_path = Path(args.input)
    files = [file_ for file_ in face_to_encode_path.rglob('*.jpg')]

    for file_ in face_to_encode_path.rglob('*.png'):
        files.append(file_)
    if len(files)==0:
        raise ValueError('No faces detect in the directory: {}'.format(face_to_encode_path))
    known_face_names = [os.path.splitext(ntpath.basename(file_))[0] for file_ in files]

    known_face_encodings = []
    for file_ in files:
        image = PIL.Image.open(file_)
        image = np.array(image)
        face_encoded = encode_face(image)[0][0]
        known_face_encodings.append(face_encoded)

    print('[INFO] Starting Webcam...')
    video_capture = cv2.VideoCapture(0)
    print('[INFO] Facial Recognition...')
    while test:
        ret, frame = video_capture.read()
        easy_face_reco(frame, known_face_encodings, known_face_names)

        cv2.imshow('Facial Recognition', frame)

        rgb_small_frame = frame[:, :, ::-1]
        # ENCODING FACE
        face_encodings_list, face_locations_list, landmarks_list = encode_face(rgb_small_frame)
        face_names = []
        for face_encoding in face_encodings_list:
            vectors = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
            tolerance = 0.6
            result = []
            for vector in vectors:
                if vector <= tolerance:
                    result.append(True)
                else:
                    result.append(False)
            if True in result:
                first_match_index = result.index(True)
                name = known_face_names[first_match_index]
                
                if name == 'Thibault':
                    print('[INFO] Reconnaissance de Thibault')
                    print('[INFO] Stopping Webcam...\n')
                    video_capture.release()
                    cv2.destroyAllWindows()

                    test = False

                elif name == "Salome":
                    print('[INFO] Reconnaissance de Salomé')
                    print('[INFO] Stopping Webcam...\n')
                    video_capture.release()
                    cv2.destroyAllWindows()

                    hour = datetime.datetime.now().hour
                    if(hour >= 6 and hour < 20):
                        print("M.I.A : Bonjour Salomé, malheureusement vous n'avez pas accès à mes commandes...")
                        mia("Bonjour Salomé, malheureusement vous n'avez pas accès à mes commandes...")
                        print("M.I.A : Cheh")
                        mia("Cheh")
                    else:
                        print("M.I.A : Bonsoir Salomé, malheureusement vous n'avez pas accès à mes commandes...")
                        mia("Bonsoir Salomé, malheureusement vous n'avez pas accès à mes commandes...")
                        print("M.I.A : Cheh")
                        mia("Cheh")

                    WMI = GetObject('winmgmts:')
                    processes = WMI.InstancesOf('Win32_Process')

                    for p in WMI.ExecQuery('select * from Win32_Process where Name="cmd.exe"'):
                        print("Killing PID:", p.Properties_('ProcessId').Value)
                        os.system("taskkill /pid "+str(p.Properties_('ProcessId').Value))

                elif name == "Maman":
                    print('[INFO] Reconnaissance de la maman du Boss')
                    print('[INFO] Stopping Webcam...\n')
                    video_capture.release()
                    cv2.destroyAllWindows()

                    hour = datetime.datetime.now().hour
                    if(hour >= 6 and hour < 20):
                        print("M.I.A : Bonjour la maman du Boss, malheureusement vous n'êtes pas le Boss...")
                        mia("Bonjour la maman du Boss, malheureusement vous n'êtes pas le Boss...")
                        print("M.I.A : Salut")
                        mia("Salut")
                    else:
                        print("M.I.A : Bonsoir la maman du Boss, malheureusement vous n'êtes pas le Boss...")
                        mia("Bonsoir la maman du Boss, malheureusement vous n'êtes pas le Boss...")
                        print("M.I.A : Salut")
                        mia("Salut")

                    WMI = GetObject('winmgmts:')
                    processes = WMI.InstancesOf('Win32_Process')

                    for p in WMI.ExecQuery('select * from Win32_Process where Name="cmd.exe"'):
                        print("Killing PID:", p.Properties_('ProcessId').Value)
                        os.system("taskkill /pid "+str(p.Properties_('ProcessId').Value))

            else:
                name = "Inconnu"
            face_names.append(name)

        key = cv2.waitKey(1)
            if key == 27:
                break

    return test


if __name__ == '__main__':

            rgb_small_frame = frame[:, :, ::-1]
            # ENCODING FACE
            face_encodings_list, face_locations_list, landmarks_list = encode_face(rgb_small_frame)
            face_names = []
            for face_encoding in face_encodings_list:
                vectors = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
                tolerance = 0.6
                result = []
                for vector in vectors:
                    if vector <= tolerance:
                        result.append(True)
                    else:
                        result.append(False)
                if True in result:
                    first_match_index = result.index(True)
                    name = known_face_names[first_match_index]
                    
                    if name == 'Thibault':
                        print('[INFO] Reconnaissance de Thibault')
                        print('[INFO] Stopping Webcam...\n')
                        video_capture.release()
                        cv2.destroyAllWindows()

                        test = False

                    elif name == "Salome":
                        print('[INFO] Reconnaissance de Salomé')
                        print('[INFO] Stopping Webcam...\n')
                        video_capture.release()
                        cv2.destroyAllWindows()

                        hour = datetime.datetime.now().hour
                        if(hour >= 6 and hour < 20):
                            print("M.I.A : Bonjour Salomé, malheureusement vous n'avez pas accès à mes commandes...")
                            mia("Bonjour Salomé, malheureusement vous n'avez pas accès à mes commandes...")
                            print("M.I.A : Cheh")
                            mia("Cheh")
                        else:
                            print("M.I.A : Bonsoir Salomé, malheureusement vous n'avez pas accès à mes commandes...")
                            mia("Bonsoir Salomé, malheureusement vous n'avez pas accès à mes commandes...")
                            print("M.I.A : Cheh")
                            mia("Cheh")

                        WMI = GetObject('winmgmts:')
                        processes = WMI.InstancesOf('Win32_Process')

                        for p in WMI.ExecQuery('select * from Win32_Process where Name="cmd.exe"'):
                            print("Killing PID:", p.Properties_('ProcessId').Value)
                            os.system("taskkill /pid "+str(p.Properties_('ProcessId').Value))

                    elif name == "Maman":
                        print('[INFO] Reconnaissance de la maman du Boss')
                        print('[INFO] Stopping Webcam...\n')
                        video_capture.release()
                        cv2.destroyAllWindows()

                        hour = datetime.datetime.now().hour
                        if(hour >= 6 and hour < 20):
                            print("M.I.A : Bonjour la maman du Boss, malheureusement vous n'êtes pas le Boss...")
                            mia("Bonjour la maman du Boss, malheureusement vous n'êtes pas le Boss...")
                            print("M.I.A : Salut")
                            mia("Salut")
                        else:
                            print("M.I.A : Bonsoir la maman du Boss, malheureusement vous n'êtes pas le Boss...")
                            mia("Bonsoir la maman du Boss, malheureusement vous n'êtes pas le Boss...")
                            print("M.I.A : Salut")
                            mia("Salut")

                        WMI = GetObject('winmgmts:')
                        processes = WMI.InstancesOf('Win32_Process')

                        for p in WMI.ExecQuery('select * from Win32_Process where Name="cmd.exe"'):
                            print("Killing PID:", p.Properties_('ProcessId').Value)
                            os.system("taskkill /pid "+str(p.Properties_('ProcessId').Value))

                else:
                    name = "Inconnu"
                face_names.append(name)
            
            key = cv2.waitKey(1)
            if key == 27:
                break

    return test