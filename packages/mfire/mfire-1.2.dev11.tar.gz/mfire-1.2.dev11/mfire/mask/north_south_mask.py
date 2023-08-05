"""Create divisions along cardinal points of a shapefile"""
from shapely import geometry as shp_geom
from shapely import affinity
from geojson import Feature, FeatureCollection

from mfire.settings import get_logger


LOGGER = get_logger(name="masks.processor.cardinals", bind="masks.processor")

PERCENT_ONE = 0.5  # pourcentage d'une zone (N, S, E, O) par rapport à l'ensemble
PERCENT_SMALL = 0.35  # pourcentage d'une zone "petite"
MIN_AREA = 10  # pourcentage minimal de la zone initiale pour conserver un découpage
MAX_AREA = 80  # pourcentage maximal
PERCENT_UNICITY = (
    0.85  # correspondance maximale entre deux zones (sinon on n'en conserve qu'une)
)

BUFFER_SIZE = 0.01  # pourcentage de simplification du découpage (par agrandissement)

# inutilisés dans cette version du module
# à supprimer après tests
PERCENT_BIG = 0.65
PERCENT_X = 0.8


def get_rid_duplicate(l_feat, percent=PERCENT_UNICITY):
    """
    Hypothesis : the region list is sort. Chosen region is the first encountered.
    This function delete "area" too closed (IoU > percent)

    Args:
        l_feat (list[Feature]): features that may be similar
        percent (float): maximal similarity allowed

    Returns:
        l_result (list[Feature])
    """
    l_result = list()
    for feat in l_feat:
        buffering = False
        geo = shp_geom.asShape(feat["geometry"])
        if geo.geometryType not in ["Polygon"]:
            buffering = True
            geo = geo.buffer(BUFFER_SIZE)
        for tested in l_result:
            other_geo = shp_geom.asShape(tested["geometry"])
            if buffering:
                other_geo = other_geo.buffer(BUFFER_SIZE)
            if geo.intersection(other_geo).area / other_geo.union(geo).area > percent:
                break
        else:
            l_result.append(feat)

    return l_result


def test_area(geo, sub, min_area, max_area):
    """
    Test si la nouvelle zone est bien "assez grande" mais "pas trop grande"
    par rapport à sa zone d'origine.

    Args:
        geo (shape): Zone géographique d'origine
        sub (shape): Découpe
        min_area (int): Pourcentage minimum de l'aire geographique
            (vis à vis de la zone d'origine)
        max_area (int): Pourcentage maximum de l'aire géographique
            (vis à vis de la zone d'origine)

    Returns:
        bool
    """
    if geo.geometryType not in ["Polygon"]:
        geo_t = geo.buffer(BUFFER_SIZE)
        sub_t = sub.buffer(BUFFER_SIZE)
    else:
        geo_t = geo
        sub_t = sub
    if (sub_t.area > geo_t.area * min_area / 100) and (
        sub_t.area < geo_t.area * max_area / 100
    ):
        return True
    return False


# unused, to be removed in next version
def return_name(collection, key="name"):
    """
    Fonction qui retourne les noms des polygones.
    Permet d'aider au choix (si on ne connait pas les noms c'est complexe).
    La clé utilisée est "key".
    """
    l_name = []
    for feature in collection["features"]:
        l_name.append(feature["properties"][key])
    return l_name


# unused, to be removed in next version
def return_poly(poly_list, name, key="name"):
    """
    Retourne le polygone ayant le nom name.
    La clé utilisée est "key"
    """
    for poly in poly_list["features"]:
        if poly["properties"][key] == name:
            return poly
    names = sorted(return_name(poly_list, key=key))
    raise ValueError(f"Name {name} not found. Possibilies are {names}.")


class CardinalMasks:
    """Crée les masques selon les points cardinaux."""

    def __init__(self, geo, area_id, cards=None):
        """
        args:
            geo(shape) : la zone à découper
            cards(list) : liste des découpages voulus (défaut à tous)
        """
        self.l_feat = []
        self.name_template = "dans {}{}"
        self.name_size = "une {} partie "

        self.geo = geo
        self.area_id = area_id
        self.min_lon, self.min_lat, self.max_lon, self.max_lat = self.geo.bounds
        self.delta_lat = self.max_lat - self.min_lat
        self.mid_lat = (self.max_lat + self.min_lat) / 2
        self.delta_lon = self.max_lon - self.min_lon
        self.mid_lon = (self.max_lon + self.min_lon) / 2

        self.bounding_rect = shp_geom.Polygon(
            [
                (self.min_lon, self.min_lat),
                (self.min_lon, self.max_lat),
                (self.max_lon, self.max_lat),
                (self.max_lon, self.min_lat),
            ]
        )

        self.cards = [
            "Nord",
            "Sud",
            "Est",
            "Ouest",
            "Sud-Est",
            "Sud-Ouest",
            "Nord-Est",
            "Nord-Ouest",
        ]
        if cards is not None:
            if any(x for x in cards if x not in self.cards):
                LOGGER.critical(
                    "une orientation du découpage demandée n'est pas configurée"
                )
                raise ValueError("bad parameter for the list of splits (cards)")
            self.cards = cards

        # nom du découpage associé
        # - aux arguments de transformation scalaire
        #               [x, y, (origin_x, origin_y] ('change_me' = proportions)
        # - au déterminant employé
        self.inputs = {
            "Nord": [(1, "change_me", (self.min_lon, self.max_lat)), "le "],
            "Sud": [(1, "change_me", (self.min_lon, self.min_lat)), "le "],
            "Est": [("change_me", 1, (self.max_lon, self.max_lat)), "l'"],
            "Ouest": [("change_me", 1, (self.min_lon, self.max_lat)), "l'"],
            "Sud-Est": [
                ("change_me", "change_me", (self.max_lon, self.min_lat)),
                "le ",
            ],
            "Sud-Ouest": [
                ("change_me", "change_me", (self.min_lon, self.min_lat)),
                "le ",
            ],
            "Nord-Est": [
                ("change_me", "change_me", (self.max_lon, self.max_lat)),
                "le ",
            ],
            "Nord-Ouest": [
                ("change_me", "change_me", (self.min_lon, self.max_lat)),
                "le ",
            ],
        }

        # possible utilisation de matrices avec affinity.affine_transform
        # mNorth = [1, 0, 0, x, 0, self.max_lat / 2]
        # mSouth = [1, 0, 0, 0.5, 0, self.min_lat / 2]
        # mEast = [0.5, 0, 0, 1, self.max_lon / 2, 0]
        # mWest = [0.5, 0, 0, 1, self.min_lon / 2, 0]

    def get_rect_mask(self, lon_scale, lat_scale, origin):
        """Returns a part of the bounding rectangle

        Args:
            lon_scale (float): scalar used to multiple longitude values
            lat_scale (float): scalar used to multiple latitude values
            origin (tuple): center point (lon, lat) of the transformation

        Returns:
            (shapefile) bounding rectangle transformed
        """
        return affinity.scale(self.bounding_rect, lon_scale, lat_scale, origin=origin)

    def get_central_squares(self):
        """Returns two lozenges in the center of the self.geo"""
        big_one = shp_geom.Polygon(
            [
                (self.mid_lon, self.mid_lat + self.delta_lat / 2 * PERCENT_ONE),
                (self.mid_lon + self.delta_lon / 2 * PERCENT_ONE, self.mid_lat),
                (self.mid_lon, self.mid_lat - self.delta_lat / 2 * PERCENT_ONE),
                (self.mid_lon - self.delta_lon / 2 * PERCENT_ONE, self.mid_lat),
            ]
        )
        # unused, but in case of
        small_one = affinity.scale(big_one, 0.5, 0.5)
        return big_one, small_one

    def make_name(self, card):
        """Create a geo mask descriptive name from templates
            ...in French...

        Args:
            card(string): compact cardinal mask name

        Returns:
            (string) name
        """
        if card.startswith("Small"):
            return self.name_template.format(self.name_size.format("petite"), card[5:])
        return self.name_template.format(self.inputs[card][1], card)

    def make_all_masks(self):
        """Make the masks according to cardinal points

        Returns:
            l_feat(FeatureCollection): geojsons
        """
        big_square, small_square = self.get_central_squares()
        for cardinal_point in self.cards:
            inpt = self.inputs[cardinal_point]
            for card_name, size in {
                cardinal_point: PERCENT_ONE,
                "Small" + cardinal_point: PERCENT_SMALL,
            }.items():
                scaling = [x if x != "change_me" else size for x in inpt[0]]
                rect_mask = self.get_rect_mask(*scaling)
                geo_mask = self.geo.intersection(rect_mask)
                if "-" in cardinal_point:
                    # we remove the center for intercardinals
                    geo_mask = geo_mask.difference(big_square)
                if test_area(self.geo, geo_mask, MIN_AREA, MAX_AREA):
                    name = self.make_name(card_name)
                    self.l_feat.append(
                        Feature(
                            geometry=geo_mask.buffer(BUFFER_SIZE),
                            id=self.area_id
                            + "_"
                            + card_name,  # vérif si le "-" est à enlever
                            properties={"name": name},
                        )
                    )

        return self.l_feat


def get_cardinal_masks(geo, parent_id="", cards=None):
    """Renvoi la liste des découpages géographique
    via la classe"""

    cm = CardinalMasks(geo, parent_id, cards)
    l_feat = cm.make_all_masks()
    if not l_feat:
        return FeatureCollection([]), []

    set_feat = get_rid_duplicate(l_feat, percent=PERCENT_UNICITY)
    l_names = [x["properties"]["name"] for x in set_feat]
    return FeatureCollection(set_feat), l_names
