import os
import contextlib

with contextlib.redirect_stdout(open(os.devnull, 'w')):
    #importations utiles sans les messages des librairies
    import cv2
    import matplotlib
    import numpy as np
    import matplotlib.pyplot as plt
    import mediapipe as mp
    import mediapipe.python.solutions.face_mesh_connections as fm
    from IPython.display import clear_output

class Nexd_utils:
    def __init__(self, *args, **kwargs):
        super(Nexd_utils, self).__init__()
        self.__author = "importFourmi"
        self.__args = args
        self.__kwargs = kwargs


    def ext_list(self, path=None, list_ext=[".png", ".jpg", ".jpeg"]):
        """
        Fonction qui liste les extensions d'un dossier.

        :param path: path du dossier (None si dossier courant)
        :param (list_ext): liste des extensions possibles (par défaut: liste des images)

        :return: la liste des chemins
        """

        return np.array([file for file in os.listdir(path) for ext in list_ext if file.endswith(ext)])


    def extension_rect(self, coords, coef):
        """
        Fonction qui multiplie les coordonnées par un coefficient (0: pas d'extension, 0.5: size*2, 1:size*3, etc.).
        Le format est le suivant: [[xmin, ymin, xmax, ymax]].

        :param coords: liste de coordonnées de rectangles
        :param coef: coefficient multiplicateur

        :return: les nouvelles coordonnées
        """

        # où mettre les nouvelles coordonnées
        result = []

        # si il y a qu'un seul rectangle
        if len(np.array(coords).shape) == 1:
            coords = np.array([coords])

        for coord in coords:

            width = coord[2] - coord[0]
            height = coord[3] - coord[1]

            result.append([ coord[0] - int((width*coef)/2),
                            coord[1] - int((height*coef)/2),
                            coord[2] + int((width*coef)/2),
                            coord[3] + int((height*coef)/2)
                          ] )

        return np.array(result)


class Data_utils:
    def __init__(self, *args, **kwargs):
        super(Data_utils, self).__init__()
        self.__author = "importFourmi"
        self.__args = args
        self.__kwargs = kwargs


    def data_draw_pixels(self, x, y, value=None, classes=None, title=None, xlabel=None, ylabel=None):
        """
        Fonction qui dessine les points.

        :param x: liste des x à dessiner
        :param y: liste des y à dessiner
        :param (value): liste des valeurs pour chaque point
        :param (classes): nom des classes de chaque point si value n'est pas explicite
        :param (title): titre de l'image
        :param (xlabel): xlabel de l'image
        :param (ylabel): ylabel de l'image

        :return: None
        """

        # si il y a un titre on l'affiche
        if title:
            plt.title(title)

        # si il y a un xlabel on l'affiche
        if xlabel:
            plt.xlabel(xlabel)

        # si il y a un ylabel on l'affiche
        if ylabel:
            plt.ylabel(ylabel)

        # on affiche les points
        scatter = plt.scatter(x, y, c=value, cmap=plt.cm.Set1)

        # si on a des valeurs
        if not(value is None):

            # si les valeurs ne sont pas labellisées
            if classes is None:
                classes = [str(val) for val in set(value)]

            # on ajoute la légende
            plt.legend(handles=scatter.legend_elements()[0], labels=classes)

        plt.show()


    def data_list_color_rgb(self):
        """
        Fonction qui retourne un dictionnaire des couleurs RGB.

        :return: le dictionnaire
        """

        return {
         'maroon': [128, 0, 0],
         'dark_red': [139, 0, 0],
         'brown': [165, 42, 42],
         'firebrick': [178, 34, 34],
         'crimson': [220, 20, 60],
         'red': [255, 0, 0],
         'tomato': [255, 99, 71],
         'coral': [255, 127, 80],
         'indian_red': [205, 92, 92],
         'light_coral': [240, 128, 128],
         'dark_salmon': [233, 150, 122],
         'salmon': [250, 128, 114],
         'light_salmon': [255, 160, 122],
         'orange_red': [255, 69, 0],
         'dark_orange': [255, 140, 0],
         'orange': [255, 165, 0],
         'gold': [255, 215, 0],
         'dark_golden_rod': [184, 134, 11],
         'golden_rod': [218, 165, 32],
         'pale_golden_rod': [238, 232, 170],
         'dark_khaki': [189, 183, 107],
         'khaki': [240, 230, 140],
         'olive': [128, 128, 0],
         'yellow': [255, 255, 0],
         'yellow_green': [154, 205, 50],
         'dark_olive_green': [85, 107, 47],
         'olive_drab': [107, 142, 35],
         'lawn_green': [124, 252, 0],
         'chartreuse': [127, 255, 0],
         'green_yellow': [173, 255, 47],
         'dark_green': [0, 100, 0],
         'green': [0, 128, 0],
         'forest_green': [34, 139, 34],
         'lime': [0, 255, 0],
         'lime_green': [50, 205, 50],
         'light_green': [144, 238, 144],
         'pale_green': [152, 251, 152],
         'dark_sea_green': [143, 188, 143],
         'medium_spring_green': [0, 250, 154],
         'spring_green': [0, 255, 127],
         'sea_green': [46, 139, 87],
         'medium_aqua_marine': [102, 205, 170],
         'medium_sea_green': [60, 179, 113],
         'light_sea_green': [32, 178, 170],
         'dark_slate_gray': [47, 79, 79],
         'teal': [0, 128, 128],
         'dark_cyan': [0, 139, 139],
         'aqua': [0, 255, 255],
         'cyan': [0, 255, 255],
         'light_cyan': [224, 255, 255],
         'dark_turquoise': [0, 206, 209],
         'turquoise': [64, 224, 208],
         'medium_turquoise': [72, 209, 204],
         'pale_turquoise': [175, 238, 238],
         'aqua_marine': [127, 255, 212],
         'powder_blue': [176, 224, 230],
         'cadet_blue': [95, 158, 160],
         'steel_blue': [70, 130, 180],
         'corn_flower_blue': [100, 149, 237],
         'deep_sky_blue': [0, 191, 255],
         'dodger_blue': [30, 144, 255],
         'light_blue': [173, 216, 230],
         'sky_blue': [135, 206, 235],
         'light_sky_blue': [135, 206, 250],
         'midnight_blue': [25, 25, 112],
         'navy': [0, 0, 128],
         'dark_blue': [0, 0, 139],
         'medium_blue': [0, 0, 205],
         'blue': [0, 0, 255],
         'royal_blue': [65, 105, 225],
         'blue_violet': [138, 43, 226],
         'indigo': [75, 0, 130],
         'dark_slate_blue': [72, 61, 139],
         'slate_blue': [106, 90, 205],
         'medium_slate_blue': [123, 104, 238],
         'medium_purple': [147, 112, 219],
         'dark_magenta': [139, 0, 139],
         'dark_violet': [148, 0, 211],
         'dark_orchid': [153, 50, 204],
         'medium_orchid': [186, 85, 211],
         'purple': [128, 0, 128],
         'thistle': [216, 191, 216],
         'plum': [221, 160, 221],
         'violet': [238, 130, 238],
         'magenta': [255, 0, 255],
         'orchid': [218, 112, 214],
         'medium_violet_red': [199, 21, 133],
         'pale_violet_red': [219, 112, 147],
         'deep_pink': [255, 20, 147],
         'hot_pink': [255, 105, 180],
         'light_pink': [255, 182, 193],
         'pink': [255, 192, 203],
         'antique_white': [250, 235, 215],
         'beige': [245, 245, 220],
         'bisque': [255, 228, 196],
         'blanched_almond': [255, 235, 205],
         'wheat': [245, 222, 179],
         'corn_silk': [255, 248, 220],
         'lemon_chiffon': [255, 250, 205],
         'light_golden_rod_yellow': [250, 250, 210],
         'light_yellow': [255, 255, 224],
         'saddle_brown': [139, 69, 19],
         'sienna': [160, 82, 45],
         'chocolate': [210, 105, 30],
         'peru': [205, 133, 63],
         'sandy_brown': [244, 164, 96],
         'burly_wood': [222, 184, 135],
         'tan': [210, 180, 140],
         'rosy_brown': [188, 143, 143],
         'moccasin': [255, 228, 181],
         'navajo_white': [255, 222, 173],
         'peach_puff': [255, 218, 185],
         'misty_rose': [255, 228, 225],
         'lavender_blush': [255, 240, 245],
         'linen': [250, 240, 230],
         'old_lace': [253, 245, 230],
         'papaya_whip': [255, 239, 213],
         'sea_shell': [255, 245, 238],
         'mint_cream': [245, 255, 250],
         'slate_gray': [112, 128, 144],
         'light_slate_gray': [119, 136, 153],
         'light_steel_blue': [176, 196, 222],
         'lavender': [230, 230, 250],
         'floral_white': [255, 250, 240],
         'alice_blue': [240, 248, 255],
         'ghost_white': [248, 248, 255],
         'honeydew': [240, 255, 240],
         'ivory': [255, 255, 240],
         'azure': [240, 255, 255],
         'snow': [255, 250, 250],
         'black': [0, 0, 0],
         'dim_gray': [105, 105, 105],
         'gray': [128, 128, 128],
         'dark_gray': [169, 169, 169],
         'silver': [192, 192, 192],
         'light_gray': [211, 211, 211],
         'gainsboro': [220, 220, 220],
         'white_smoke': [245, 245, 245],
         'white': [255, 255, 255]
         }



class Img_utils:
    def __init__(self, *args, **kwargs):
        super(Img_utils, self).__init__()
        self.__author = "importFourmi"
        self.__args = args
        self.__kwargs = kwargs


    def im_load(self, img_path):
        """
        Fonction qui télécharge l'image en RGB.

        :param img_path: path de l'image

        :return: l'image
        """

        if not(os.path.isfile(img_path)):
            print("Image not found")
            return np.array([])

        else :
            # l'image est créée avec OpenCV
            img = cv2.imread(img_path)

            # on met de la bonne couleur
            return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    def im_gray(self, img):
        """
        Fonction qui retourne l'image en gris (0.299*R+0.587*G+0.114*B).

        :param img: image

        :return: l'image en gris
        """

        return cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)


    def im_show(self, img, title="", dynamic=False, shape=True):
        """
        Fonction qui affiche l'image.

        :param img: image
        :param (title): titre de l'image
        :param (dynamic): permet de mettre l'image à jour
        :param (shape): permet de dire si on affiche la taille

        :return: None
        """

        img = img.copy()

        if shape:
            # on affiche les dimensions de l'image
            print(np.array(img).shape)

        # si il y a un titre on l'affiche
        if title:
            plt.title(title)

        # on n'affiche pas les axes
        plt.axis('off')

        # efface l'ancien output
        if dynamic:
            clear_output(wait=True)

        # si l'image est en niveau de gris
        if len(np.array(img).shape) == 2 or np.array(img).shape[2]==1:
            plt.imshow(img, cmap='gray')

        else:
            plt.imshow(img)
        plt.imshow(img)
        plt.show()


    def im_draw_pixels(self, img, x, y, value=None, color=[0, 255, 0], radius=None):
        """
        Fonction qui dessine les pixels sur l'image.

        :param img: image
        :param x: liste des x à dessiner
        :param y: liste des y à dessiner
        :param (value): liste des valeurs pour chaque pixel
        :param (color): couleur des pixels si il n'y a pas de valeurs pour chaque pixel
        :param (radius): radius des pixels

        :return: l'image avec les pixels
        """

        img = img.copy()

        if radius is None:
            radius = int(0.01*max(img.shape[0], img.shape[1]))

        if not(value is None):
            # normalise linéairement les données entre 0.0 et 1.0
            norm = matplotlib.colors.Normalize(vmin=min(value), vmax=max(value))

            # transforme les valeurs en couleurs
            rgba = plt.get_cmap('inferno')(norm(value.astype(np.float64)))

            # on dessine un cercle de 1% de la taille de l'image (de la couleur de la valeur)
            for i in range(len(x)):
                img = cv2.circle(img, (int(x[i]), int(y[i])), radius, rgba[i][:-1]*255, -1)

        else:
            # on dessine un cercle (en vert) de 1% de la taille de l'image
            for i in range(len(x)):
                img = cv2.circle(img, (int(x[i]), int(y[i])), radius, color, -1)

        return img


    def im_draw_rect(self, img, coords, color=(255, 0, 0), thickness=1):
        """
        Fonction qui dessine des rectangles sur une image.

        :param img: image sur laquelle on veut dessiner des rectangles
        :param coords: liste des coordonnées des rectangles (x_start, y_start, x_end, y_end)
        :param (color): couleur des rectangles à dessiner
        :param (thickness): épaisseur des rectangles (-1 pour un rectangle plein)

        :return: l'image avec les rectangles
        """
        img = img.copy()

        # si il y a qu'un seul rectangle
        if len(np.array(coords).shape) == 1:
            coords = np.array([coords])

        for coord in coords:
            # on dessine tous les rectangles
            img = cv2.rectangle(img, (coord[0], coord[1]), (coord[2], coord[3]), color, thickness)
        return img


    def im_redim(self, img, size=(500,500), interpolator=cv2.INTER_LANCZOS4):
        """
        Fonction qui redimensionne une image.

        :param img: liste des x à dessiner
        :param (size): taille de la nouvelle image
        :param (interpolator): interpolateur qui gère les pixels

        :return: la nouvelle image
        """

        return cv2.resize(img.copy(), (int(size[0]),int(size[1])), interpolation=interpolator)


    def im_stack(self, list_img):
        """
        Fonction qui retourne la superposition des images.

        :param list_img: liste des x à dessiner

        :return: le résultat de la superposition
        """

        return np.stack(list_img, axis=3).mean(axis=3)/255


    def im_affine_transform(self, img, pts1, pts2):
        """
        Fonction qui applique une transormation affine sur l'image.

        :param img: image
        :param pts1: liste des coordonnées d'origine des trois points
        :param pts2: liste des coordonnées de destinations des trois points

        :return: l'image transformée
        """

        rows, cols = img.shape[:2]

        M = cv2.getAffineTransform(np.float32(pts1), np.float32(pts2))
        return cv2.warpAffine(img.copy(), M, (cols, rows))


    def im_save(self, filename, img):
        """
        Fonction qui permet d'enregistrer une image.
        :param filename: string représentant le nom de l'image
        :param img: image à enregistrer

        :return: None
        """

        # ordre normal des paramètres
        if isinstance(filename, str) and not isinstance(img, str):
            plt.imsave(filename, img)

        # si on se trompe sur l'ordre des paramètres
        elif isinstance(img, str) and not isinstance(filename, str):
            plt.imsave(img, filename)


    def im_rotation(self, img, direction):
        """
        Fonction qui applique une rotation à l'image.

        :param img: image
        :param direction: sens de rotation de l'image

        :return: l'image retournée
        """

        if direction == "gauche" or direction == "left" or direction == -90:
            return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

        elif direction == "droite" or direction == "right" or direction == 90:
            return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

        elif direction == "180" or direction == "flip" or direction == 180:
            return cv2.rotate(img, cv2.ROTATE_180)
        else:
            print("Direction not found")
            return img

class Landmarks:
    def __init__(self, *args, **kwargs):
        super(Landmarks, self).__init__()
        self.__author = "importFourmi"
        self.__args = args
        self.__kwargs = kwargs

        self.parts_face = self.__set_parts_face__()
        self.set_landmarks_detector()
        self.__set_parts_face_global__()


    def __frozenset_list__(self, pFrozenset):
        """
        Fonction qui transforme un frozenset en liste de points.

        :param frozenset: frozenset avec les points

        :return: la liste des points
        """

        return sorted(set(np.array(list(pFrozenset)).reshape(-1)))


    def __set_parts_face__(self):
        """
        Fonction qui renvoie pour chaque partie du visage les landmarks correspondants.

        :return: le dictionnaire des parties du visage
        """

        return {
            "LEFT_EYE": self.__frozenset_list__(fm.FACEMESH_LEFT_EYE),
            "LEFT_EYEBROW": self.__frozenset_list__(fm.FACEMESH_LEFT_EYEBROW),
            "LEFT_IRIS": self.__frozenset_list__(fm.FACEMESH_LEFT_IRIS),
            "LIPS": self.__frozenset_list__(fm.FACEMESH_LIPS),
            "RIGHT_EYE": self.__frozenset_list__(fm.FACEMESH_RIGHT_EYE),
            "RIGHT_EYEBROW": self.__frozenset_list__(fm.FACEMESH_RIGHT_EYEBROW),
            "RIGHT_IRIS": self.__frozenset_list__(fm.FACEMESH_RIGHT_IRIS),
        }


    def set_landmarks_detector(self, max_num_faces=1, min_detection_confidence=0.9):
        """
        Fonction qui permet d'initialiser notre détecteur.

        :param (max_num_faces): nombre maximum de visages à détecter
        :param (min_detection_confidence): coeficient de certitude de détection

        :return: None
        """

        self.__landmarks_detector__ = mp.solutions.face_mesh.FaceMesh(max_num_faces=max_num_faces,
                                                                  refine_landmarks=True,
                                                                  min_detection_confidence=min_detection_confidence,
                                                                  static_image_mode=True,
                                                                 )


    def extract_landmarks(self, img, normalized=True):
        """
        Fonction qui retourne les landmarks d'un visage détécté sous le format [x, y, z(profondeur de chaque repère)].

        :param img: image
        :param (normalized): x et y normalisés si True / x et y en pixels si False

        :return: une liste de dimensions (478, 3) si un visage est détécté
        """

        results = self.__landmarks_detector__.process(img)
        if results.multi_face_landmarks:
            rows, cols = img.shape[:2]

            list_landmarks = list(results.multi_face_landmarks[0].landmark)
            if normalized:
                return np.array([[i.x, i.y, i.z] for i in list_landmarks])

            else:
                return np.array([[i.x*cols, i.y*rows, i.z] for i in list_landmarks])
        else:
            return np.array([])


    def parts_face_mean(self, img):
        """
        Fonction qui retourne un dictionnaire avec les coordonnées du centre de chaque partie du visage.

        :param img: image

        :return: le dictionnaire si un visage est détécté
        """

        landmarks = self.extract_landmarks(img)
        if np.any(landmarks):
            center_dic = {}
            for key, value in self.parts_face.items():
                center_dic[key] = np.array([landmarks[ld] for ld in value]).mean(axis=0)
            return center_dic

        else:
            return np.array([])


    def __parts_face_selected__(self, img):
        """
        Fonction qui retourne un dictionnaire avec le centre des lèvres et des iris.

        :param img: image

        :return: le dictionnaire si un visage est détécté
        """

        dictionnaire = self.parts_face_mean(img)
        if np.any(dictionnaire):
            select = ["LEFT_IRIS", "LIPS", "RIGHT_IRIS"]
            return {key: value for key, value in dictionnaire.items() if key in select}

        else:
            return np.array([])


    def __set_parts_face_global__(self, coef=0.3):
        """
        Fonction qui intialise les positions d'un visage moyen.

        :param (coef): coeficient de zoom ou dézoom

        :return: None
        """

        D = {}
        D["LEFT_IRIS"] = [0.65, 0.42]
        D["LIPS"] = [0.50,  0.75]
        D["RIGHT_IRIS"] = [0.35, 0.42]

        pts = np.array([D["LEFT_IRIS"], D["LIPS"], D["RIGHT_IRIS"]])
        self.__parts_face_global__ = (pts+coef/2)/(1+coef)


    def align_face(self, img):
        """
        Fonction qui aligne un visage toujours dans la même position.

        :param img: image

        :return: l'image alignée
        """

        rows, cols = img.shape[:2]

        pts1 = self.__parts_face_selected__(img)

        if np.any(pts1):

            pts1 = np.array([pts1["LEFT_IRIS"][:2], pts1["LIPS"][:2], pts1["RIGHT_IRIS"][:2]])
            pts2 = self.__parts_face_global__.copy()

            for i in range(3):
                pts1[i][0] *= cols
                pts1[i][1] *= rows

                pts2[i][0] *= cols
                pts2[i][1] *= rows


            M = cv2.getAffineTransform(np.float32(pts1), np.float32(pts2))
            return cv2.warpAffine(img.copy(), M, (cols, rows))

        else:
            return np.array([])



class Nexd(Nexd_utils, Data_utils, Img_utils, Landmarks):

    def __init__(self, *args, **kwargs):
        super(Nexd, self).__init__()
        self.__author = "importFourmi"
        self.__args = args
        self.__kwargs = kwargs
        self.methods = [f for f in dir(self) if not f.startswith('_')]


        if self.__kwargs.get("verbose") == 1:
            print("Bienvenue dans Nexd, les fonctions disponibles sont les suivantes et vous pouvez utiliser help(fonction) pour plus d'informations :")
            for fonction in self.methods:
                print("  -", fonction)
