"""Übersicht über den Dateiinhalt:

Die Klasse Users verwaltet alle Benutzer des Online-Marktplatzes.
Sie erbt von `Praktikumsgruppen` und liest Benutzer- sowie Freundschaftsdaten
aus den CSV-Dateien (`user.csv`, `friends.csv`) ein. Sie stellt Methoden zur
Passwortüberprüfung, Freundschaftsempfehlung, Abstands- und Verbindungsberechnung bereit.
"""

# Status: FINAL, dgaida2, 15.10.2024

# definiert die Klasse Users.
# Users ist eine Menge von disjunkten Mengen (nur für drittes Praktikum) von der Klasse User,
# damit man Users in Praktikumsgruppen einsortieren kann. Für das erste und zweite Praktikum ist die Klasse
# Praktikumsgruppe lediglich ein Dictionary
# in der Klasse werden die csv-Dateien user.csv und friends.csv gelesen.

from typing import Any, Dict, List, Optional, Tuple, Union
import ast
import csv
import os
import networkx as nx
import osmnx as ox
import marketplace.user
import marketplace.praktikumsgruppen


class Users(marketplace.praktikumsgruppen.Praktikumsgruppen):
    """Klasse zur Verwaltung aller registrierten Benutzer und ihrer Freundschaften.

    Attributes:
        _groupnumbers (List[int]): Liste der Gruppennummern der eingelesenen Benutzer.
        MAP_FILE (str): Datei, in der der Straßengraph lokal gespeichert wird.
        ROAD_FILTER (str): osmnx-Filter, damit nur größere Straßen (inkl. Auf-/Abfahrten) geladen werden.
        _map_graph (Optional[nx.MultiDiGraph]): Straßengraph, wird nur einmal geladen.
        _map_nodes (Dict[str, int]): Nächster Knoten im Straßengraph je Benutzer-ID.
        _distance_cache (Dict[Tuple[str, str], float]): Bereits berechnete Fahrstrecken in km.
    """

    # Straßengraph für das Gebiet aller Wohnorte: einmal herunterladen, lokal speichern, danach nur laden
    MAP_FILE: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "nrw_roads.graphml")
    ROAD_FILTER: str = ('["highway"~"motorway|motorway_link|trunk|trunk_link|'
                        'primary|primary_link|secondary|secondary_link"]')
    _map_graph: Optional[nx.MultiDiGraph] = None
    _map_nodes: Dict[str, int] = {}
    _distance_cache: Dict[Tuple[str, str], float] = {}

    # *** CONSTRUCTORS ***
    def __init__(self, csvfile: str, *args: Any) -> None:
        """Initialisiert das Users-Objekt und liest Daten aus CSV-Dateien ein.

        Args:
            csvfile (str): Pfad zur Benutzer-CSV-Datei (z. B. 'user.csv').
            *args (Any): Variable Argumente.

        Raises:
            FileNotFoundError: Falls die CSV-Datei nicht gefunden wurde.
        """
        super().__init__()

        self._read_users_from_csvfile(csvfile)
        self._read_friends_csv('friends.csv')

        # erstelle Praktikumsgruppen als Menge disjunkter Mengen bzw. als dictionary (1. und 2. Praktikum)
        super().create_groups(list(self.keys()), self._groupnumbers)

    # *** PUBLIC SET methods ***

    # *** PUBLIC methods ***

    def add(self, user_id: str, password: str, name_family: str = "", name_first: str = "",
            gps_coord: Tuple[Optional[float], Optional[float]] = (None, None), address: str = "") -> None:
        """Adds the given user with user_id to the internal dictionary.

        Args:
            user_id (str): GM-ID / unique user identifier.
            password (str): Password of user.
            name_family (str, optional): Family name of user. Defaults to "".
            name_first (str, optional): First name of user. Defaults to "".
            gps_coord (tuple, optional): (latitude, longitude) coordinates. Defaults to (None, None).
            address (str, optional): Address string corresponding to GPS coordinates. Defaults to "".
        """
        self[user_id] = marketplace.user.User(user_id, password, name_family, name_first, gps_coord, address)

    def calc_distance_between_users(self, user_id1: str, user_id2: str) -> float:
        """Berechnet die Fahrstrecke zwischen den Wohnorten zweier Benutzer (kürzester Weg im Straßengraph).

        Args:
            user_id1 (str): First user ID.
            user_id2 (str): Second user ID.

        Returns:
            float: Länge der kürzesten Route in km, `inf`, falls es keine Route gibt.
        """
        key = (user_id1, user_id2)
        if key not in self._distance_cache:
            graph = self._get_map_graph()
            origin = self._get_map_node(user_id1)
            destination = self._get_map_node(user_id2)
            path = ox.routing.shortest_path(graph, origin, destination, weight="length")
            if path is None:
                distance = float("inf")
            else:
                distance = nx.path_weight(graph, path, weight="length") / 1000
            self._distance_cache[key] = distance
        return self._distance_cache[key]

    # *** PUBLIC GET methods ***

    def get_name_of_user(self, user_id: str) -> str:
        """Gibt den vollständigen Namen des Benutzers zurück.

        Args:
            user_id (str): Benutzer-ID.

        Returns:
            str: Name des Benutzers.

        Raises:
            KeyError: Falls die `user_id` nicht existiert.
        """
        node = self[user_id]
        return node.name()

    def num_users(self) -> int:
        """Gibt die Gesamtanzahl registrierter Benutzer zurück.

        Args:
            None

        Returns:
            int: Anzahl der Benutzer.

        Raises:
            None
        """
        return len(self.keys())

    def password_valid(self, user_id: str, password: str) -> bool:
        """Prüft, ob das Passwort für den angegebenen Benutzer gültig ist.

        Args:
            user_id (str): Benutzer-ID.
            password (str): Passwort.

        Returns:
            bool: `True`, wenn Passwort korrekt, sonst `False`.

        Raises:
            KeyError: Falls die `user_id` nicht existiert.
        """
        return self[user_id].password_valid(password)

    def get_user_pretty_print_for_list(self, user_id: str) -> str:
        """Erstellt eine formatierte Repräsentation eines Benutzers für Listboxen.

        Args:
            user_id (str): Benutzer-ID.

        Returns:
            str: Der formatierte Benutzer-String inkl. Praktikumsgruppen-Info.

        Raises:
            KeyError: Falls `user_id` nicht existiert.
        """
        return (self[user_id].pretty_print() + "\t in Praktikumsgruppe repräsentiert durch: " +
                str(self.find_byid(user_id, True)))

    def get_friends_andgroupmembers_pretty_print(self, user_id: str) -> List[str]:
        """Returns list of friends and group members for the given user_id that is shown on GUI.

        Args:
            user_id (str): usually the current user id

        Returns:
            List[str]: Liste formatierter Strings.

        Raises:
            KeyError: Falls `user_id` nicht existiert.
        """
        friends = self[user_id].friends()
        friend_names = [self.get_user_pretty_print_for_list(friend) for friend in friends]

        group_members = self.get_groupmembers(user_id)
        if group_members is None:
            return friend_names

        # entferne mich selbst aus der Gruppe, da ich ja weiß, dass ich (user_id) in der Gruppe bin
        if user_id in group_members:
            group_members.remove(user_id)

        group_members_pp = [self.get_user_pretty_print_for_list(member) for member in group_members]
        return friend_names + group_members_pp

    def get_mutual_friends(self, user_id: str) -> Dict[str, int]:
        """Ermittelt gemeinsame Freunde (Freunde von Freunden) und deren Häufigkeit.

        Args:
            user_id (str): usually the current user id

        Returns:
            Dict[str, int]: dictionary with friends of the friends of given user_id together with the information with how many friends of user_id these friends are friends with

        Raises:
            KeyError: Falls `user_id` nicht existiert.
        """
        friends = self[user_id].friends()
        mutual_friends_count: Dict[str, int] = {}

        for friend in friends:
            friend_friends = self[friend].friends()
            for mutual_friend in friend_friends:
                if mutual_friend != user_id and mutual_friend not in friends:
                    if mutual_friend in mutual_friends_count:
                        mutual_friends_count[mutual_friend] += 1
                    else:
                        mutual_friends_count[mutual_friend] = 1

        return mutual_friends_count

    def suggest_friends(self, user_id: str, num_common_friends: int = 2,
                        distance_threshold: float = 20.0, pretty_print: bool = True) -> List[str]:
        """Suggests users to the given user_id that
        (1) are friends with at least num_common_friends friends of user_id or
        (2) that live nearby the given user_id (closer as distance_threshold) and are friends of friends of friends...
        (see are_users_connected())

        Args:
            user_id (str): usually the current user id
            num_common_friends (int): only suggest users that are at least friends with two of the user_ids friends
            distance_threshold (float): only suggest users that live closer to the given user_id as this threshold value
                (Fahrstrecke in km)
            pretty_print (bool): if True, then call pretty_print() on all suggested friends before returning them

        Returns:
            List[str]: list of suggested friends. the first part of the list should contain common friends, ordered so that users with maximum number of common friends appear first. the second part of the list should contain all users that live close by, again sorted, so that the direct neighbour comes first.

        Raises:
            KeyError: Falls `user_id` nicht existiert.
        """
        mutual_friends_count = self.get_mutual_friends(user_id)
        # TODO for students: Implement this method by filling the list suggested_friends

        suggested_friends = [
            friend
            for friend, count in sorted(
                mutual_friends_count.items(),
                key=lambda item: item[1],
                reverse=True
            )
            if count >= num_common_friends
        ]

        # (2) Nutzer, die über das Freundesnetzwerk verbunden sind und näher als distance_threshold wohnen,
        #     sortiert nach Fahrstrecke (direkter Nachbar zuerst)
        friends = self[user_id].friends()
        nearby = []
        for other_id in self:
            if other_id == user_id or other_id in friends or other_id in suggested_friends:
                continue
            if not self.are_users_connected(user_id, other_id):
                continue
            distance = self.calc_distance_between_users(user_id, other_id)
            if distance < distance_threshold:
                nearby.append((distance, other_id))
        nearby.sort()
        suggested_friends += [other_id for distance, other_id in nearby]

        if pretty_print:
            suggested_friends = [self[friend].pretty_print() for friend in suggested_friends]

        return suggested_friends

    def are_users_connected(self, user_id1: str, user_id2: str, degree: int = 3) -> bool:
        """Prüft mittels Breitensuche, ob zwei Benutzer über Freundschaftskanten verbunden sind.

        Args:
            user_id1 (str): a user that we are searching a friend for
            user_id2 (str): another user, where we want to check whether it is somehow friends with user_id1 over some other shared friends
            degree (int): only look for possible friend connections up to this degree of friendship. Defaults to 3.

        Returns:
            bool: True, if user_id1 and user_id2 are friends over some edges up to the given degree, else False

        Raises:
            None
        """
        if user_id1 not in self or user_id2 not in self:
            return False

        # TODO for students: Implement this method
        visited = {user_id1}
        current_level = [user_id1]
        
        for _ in range(degree):
            next_level = []

            for user_id in current_level:
                for friend in self[user_id].friends():
                    if friend == user_id2:
                        return True

                    if friend not in visited:
                        visited.add(friend)
                        next_level.append(friend)

                current_level = next_level



        return False

    # *** PUBLIC STATIC methods ***

    # *** PRIVATE methods ***

    def _get_map_graph(self) -> nx.MultiDiGraph:
        """Lädt den Straßengraph einmal: aus MAP_FILE, sonst per Download über eine Bounding Box um alle Wohnorte.

        Returns:
            nx.MultiDiGraph: Straßengraph für das Gebiet aller Benutzer.
        """
        if Users._map_graph is None:
            if os.path.exists(Users.MAP_FILE):
                Users._map_graph = ox.load_graphml(Users.MAP_FILE)
            else:
                lats = [user.gps_coords()[0] for user in self.values()]
                lons = [user.gps_coords()[1] for user in self.values()]
                margin = 0.1    # ca. 10 km Rand, damit Wohnorte am Rand noch Straßen haben
                # Bounding Box in der Reihenfolge (left, bottom, right, top) = (min Länge, min Breite, max Länge, max Breite)
                bbox = (min(lons) - margin, min(lats) - margin, max(lons) + margin, max(lats) + margin)
                Users._map_graph = ox.graph.graph_from_bbox(bbox, custom_filter=Users.ROAD_FILTER)
                ox.save_graphml(Users._map_graph, Users.MAP_FILE)
        return Users._map_graph

    def _get_map_node(self, user_id: str) -> int:
        """Gibt den Knoten im Straßengraph zurück, der dem Wohnort des Benutzers am nächsten liegt.

        Args:
            user_id (str): Benutzer-ID.

        Returns:
            int: ID des nächsten Knotens.
        """
        if user_id not in self._map_nodes:
            lat, lon = self[user_id].gps_coords()
            # nearest_nodes erwartet erst den Längengrad (X), dann den Breitengrad (Y)
            self._map_nodes[user_id] = ox.distance.nearest_nodes(self._get_map_graph(), lon, lat)
        return self._map_nodes[user_id]

    def _read_users_from_csvfile(self, csvfile: str) -> None:
        """
        Read the given csvfile that contains all students that want to do the Praktikum in this semester
        including their GM-ID, Names and number of their Praktikumsgruppe

        :param csvfile: csv file that has to be created at the beginning of the semester containing all students
        in this semester
        """
        with open(csvfile, newline='', encoding='utf-8-sig') as f:
            csvreader = csv.reader(f)
            # Skip header row
            next(csvreader)

            # private member variable containing the Praktikumsgruppe number of the students in the order that the
            # students are read from the csv file
            self._groupnumbers = []

            for row in csvreader:
                user_id, name_family, name_first, password, groupnum, gps_coords, address = row
                # macht aus String wieder das Tuple mit long und lat Koordinaten
                # (literal_eval statt eval, damit aus der CSV-Datei kein beliebiger Code ausgeführt werden kann)
                gps_coords_tuple = ast.literal_eval(gps_coords)
                self.add(user_id, password, name_family, name_first, gps_coords_tuple, address)
                self._groupnumbers.append(int(groupnum))

    def _read_friends_csv(self, file_path: str) -> None:
        """
        Funktion, um die friends.csv-Datei einzulesen und ein Dictionary zu erstellen
        :param file_path: path to friends.csv file
        """
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            csvreader = csv.reader(f)
            next(csvreader)  # Überspringe die Header-Zeile
            for row in csvreader:
                user_id = row[0]
                friends = row[1].split(', ')
                self[user_id].friends_add_list(friends)
                for friend in friends:  # gehe alle Freunde durch und füge user_id ebenfalls als Freund hinzu
                    self[friend].friends_add(user_id)

    # *** PUBLIC methods to return class properties ***

    # *** PRIVATE variables ***
