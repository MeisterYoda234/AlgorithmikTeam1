"""Übersicht über den Dateiinhalt:

Implementiert die Disjoint-Set-Datenstruktur (Union-Find) mit `SetNode` und `Praktikumsgruppen`.
Ermöglicht das Zusammenfassen von Benutzern in Praktikumsgruppen (Gruppenbildung,
Union, Find mit Pfadkomprimierung).
"""

# Status: FINAL, dgaida2, 15.10.2024

# Definiert die Klassen Praktikumsgruppen und SetNode, implementiert als Menge von disjunkten Mengen (Praktikum 3) oder als Dictionary (Praktikum 1 und 2)
#
from typing import Any, List, Optional, Union


class SetNode:
    """Klasse zur Repräsentation eines Knotens in einer Disjoint-Set-Struktur (Union-Find).

    Attributes:
        _parent (SetNode): Zeiger auf den Eltern-Knoten (self bei Wurzeln).
        _weight (int): Anzahl der Knoten im Teilbaum.
        _praktikumsgruppe (int): Nummer der Gruppe im Praktikum
    """

    # TODO for students: die Klasse user.User erbt von SetNode. diese Klasse wird eigentlich erst in Praktikum 3 benötigt.
    #     für Praktikum 1 und 2 müsste User nicht von dieser Klasse erben

    # *** CONSTRUCTORS ***
    def __init__(self) -> None:
        """Initialisiert einen SetNode als eigene Wurzel mit Gewicht 1.

        Args:
            None

        Raises:
            None
        """
        self._praktikumsgruppe:  Optional[int] = None #Prak_1

        # TODO: werden nur für Praktikum 3 benötigt
        self._parent: SetNode = self   # parent Knoten des SetNode Objekts. self bedeutet, dass der Knoten ein Wurzelknoten ist
        self._weight: int = 1      # Gewicht (Anzahl Knoten) des (Teil-)Baumes, der in dem SetNode Objekt verwurzelt ist
    
        # Alternative: Rank-based Quick Union
        # self._rank = 0

    # *** PUBLIC methods to return class properties ***
    @property
    def praktikumsgruppe(self):
        return self._praktikumsgruppe

    # TODO: implementieren Sie in Praktikum 3 die benötigten Methoden

    # *** PUBLIC SET methods ***
    @praktikumsgruppe.setter
    def praktikumsgruppe(self, value):
        self._praktikumsgruppe = value 

    # TODO: implementieren Sie in Praktikum 3 die benötigten Methoden

class Praktikumsgruppen(dict):
    """Klasse zur Repräsentation einer Sammlung disjunkter Mengen (Praktikumsgruppen).

    In Praktikum 1 und 2: Dictionary containing all students. Die Klasse user.Users erbt von dieser Klasse.
    In Praktikum 3: Class representing a collection of disjoint sets for grouping users into practical groups.

    Methods:
        find(node): Finds the root of the set containing the node, with path compression.
        find_byid(user_id, return_id=False): Finds the root of the set containing the user by ID.
        union(user_id1, user_id2): Unions the sets containing the two users.
        create_groups(user_ids, groupnumbers): Creates groups from the provided user IDs and group numbers.
        get_groupmembers(user_id): Gets the members of the group containing the user.
        print_ds(): Prints the disjoint set structure.

    Attributes:
        None (erbt von dict).
    """

    # *** CONSTRUCTORS ***
    def __init__(self) -> None:
        """Initialisiert eine neue Praktikumsgruppen-Instanz.

        Args:
            None

        Raises:
            None
        """
        super().__init__()

    # *** PUBLIC methods ***

    # TODO in Praktikum 3: implement find(node), find_byid(user_id, return_id=False) and 
    #  union(user_id1, user_id2)

    def find_byid(self, user_id: str, return_id: bool = False) -> Union[Any, str]:
        """Findet die Wurzel der Praktikumsgruppe eines Benutzers anhand seiner ID.

        TODO students: die Methode existiert in der Studierendenversion nur aus Kompatibilitätsgründen und wird im 3. Praktikum implementiert

        Args:
            user_id (str): Benutzer-ID.
            return_id (bool): Wenn `True`, wird die Benutzer-ID der Wurzel zurückgegeben.

        Returns:
            Union[Any, str]: Das Wurzelobjekt oder dessen ID.

        Raises:
            KeyError: Falls `user_id` nicht im Wörterbuch existiert.
        """
        return user_id

    def create_groups(self, user_ids: List[str], groupnumbers: List[int]) -> None:
        """Erstellt Praktikumsgruppen aus Benutzer-IDs und Gruppennummern.

        Args:
            user_ids (List[str]): Liste von Benutzer-IDs.
            groupnumbers (List[int]): Zuordnende Gruppennummern.

        Returns:
            None

        Raises:
            None
        """
        for i, u in enumerate(user_ids):                       # Prak_1
            self[u]._praktikumsgruppe = groupnumbers[i]

    # *** PUBLIC GET methods ***

    def get_groupmembers(self, user_id: str) -> List[str]:
        """Gibt eine Liste aller Gruppenmitglieder der Gruppe des Benutzers zurück.

        Args:
            user_id (str): Benutzer-ID.

        Returns:
            List[str]: Liste von Benutzer-IDs der Gruppenmitglieder.

        Raises:
            KeyError: Falls `user_id` nicht im Wörterbuch existiert.
        """
        group: List[str] = []

        for u in self:                                                          # Prak_1
            if (self[u]._praktikumsgruppe == self[user_id]._praktikumsgruppe):
                group.append(u)
        return group

    def print_ds(self) -> None:
        """Gibt die Disjoint-Set-Struktur aus.

        Funktioniert erst, wenn Sie in Praktikum 3 die Methode parent() in SetNode implementiert haben.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        for user_id, user in self.items():
            print(user_id, self[user_id].parent().id())

    # *** PUBLIC STATIC methods ***

    # *** PRIVATE methods ***

    # *** PUBLIC methods to return class properties ***

    # *** PRIVATE variables ***
