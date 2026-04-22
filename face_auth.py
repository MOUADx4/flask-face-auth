import base64
import numpy as np
import face_recognition
import cv2


# ---------------------------------------------------------
#   EXTRACTION ENCODAGE FACIAL DEPUIS BASE64
# ---------------------------------------------------------
def extract_face_encoding(base64_image):
    """
    Reçoit une image base64 (data:image/jpeg;base64,...)
    Retourne un vecteur d'encodage facial (numpy array 128D)
    ou None si aucun visage détecté.
    """
    try:
        # Décoder le base64 → bytes
        img_data = base64.b64decode(base64_image.split(",")[-1])

        # Convertir en tableau numpy
        np_arr = np.frombuffer(img_data, np.uint8)

        # Lire l'image avec OpenCV
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if img is None:
            print("Erreur : image non décodable")
            return None

        # Convertir en RGB (face_recognition utilise RGB)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Extraire les encodages
        encodings = face_recognition.face_encodings(rgb)

        if len(encodings) == 0:
            return None  # Aucun visage détecté

        # Retourner un numpy array (pas .tolist())
        return encodings[0]

    except Exception as e:
        print("Erreur extraction encodage :", e)
        return None


# ---------------------------------------------------------
#   COMPARAISON DES ENCODAGES
# ---------------------------------------------------------
def compare_encodings(known_encoding, new_encoding, tolerance=0.45):
    """
    known_encoding : encodage stocké en base (list ou numpy array)
    new_encoding   : encodage extrait de l'image (numpy array)
    """
    try:
        # Convertir en numpy array si nécessaire
        known = np.array(known_encoding)
        new = np.array(new_encoding)

        results = face_recognition.compare_faces(
            [known],
            new,
            tolerance=tolerance
        )
        return results[0]

    except Exception as e:
        print("Erreur comparaison :", e)
        return False
