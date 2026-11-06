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
        self.praktikumsgruppe:  Optional[int] = None #Prak_1

        # TODO: werden nur für Praktikum 3 benötigt
        self._parent: SetNode = self   # parent Knoten des SetNode Objekts. self bedeutet, dass der Knoten ein Wurzelknoten ist
        self._weight: int = 1      # Gewicht (Anzahl Knoten) des (Teil-)Baumes, der in dem SetNode Objekt verwurzelt ist
    
        # Alternative: Rank-based Quick Union
        # self._rank = 0

    # *** PUBLIC methods to return class properties ***
    @property
    def praktikumsgruppe(self):
        return self._praktikumsgruppe

    def parent(self):
        return self._parent

    @property
    def weight(self):
        return self._weight

    # *** PUBLIC SET methods ***
    @praktikumsgruppe.setter
    def praktikumsgruppe(self, value):
        self._praktikumsgruppe = value 

    def set_parent(self, value):
        self._parent = value

    @weight.setter
    def weight(self, value):
        self._weight = value

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

    def find(self, node: SetNode) -> SetNode:
        """Findet die Wurzel der Menge, in der sich der Knoten befindet, mit Pfadverkürzung.

        Args:
            node (SetNode): Knoten (User-Objekt), dessen Wurzel gesucht wird.

        Returns:
            SetNode: Die Wurzel der Menge.

        Raises:
            None
        """
        # Wurzel suchen: hochlaufen, bis ein Knoten auf sich selbst zeigt
        root = node
        while root.parent() is not root:
            root = root.parent()

        # Pfadverkürzung: jeden Knoten auf dem Weg direkt an die Wurzel hängen
        while node is not root:
            next_node = node.parent()
            node.set_parent(root)
            node = next_node

        return root

    def find_byid(self, user_id: str, return_id: bool = False) -> Union[Any, str]:
        """Findet die Wurzel der Praktikumsgruppe eines Benutzers anhand seiner ID.

        Args:
            user_id (str): Benutzer-ID.
            return_id (bool): Wenn `True`, wird die Benutzer-ID der Wurzel zurückgegeben.

        Returns:
            Union[Any, str]: Das Wurzelobjekt oder dessen ID.

        Raises:
            KeyError: Falls `user_id` nicht im Wörterbuch existiert.
        """
        root = self.find(self[user_id])
        if return_id:
            return root.id()
        return root

    def union(self, user_id1: str, user_id2: str) -> None:
        """Vereinigt die Mengen (Praktikumsgruppen) der beiden Benutzer (weighted Quick-Union).

        Der kleinere Baum wird unter die Wurzel des größeren gehängt, damit die Bäume flach bleiben.

        Args:
            user_id1 (str): Erste Benutzer-ID.
            user_id2 (str): Zweite Benutzer-ID.

        Returns:
            None

        Raises:
            KeyError: Falls eine der IDs nicht im Wörterbuch existiert.
        """
        root1 = self.find_byid(user_id1)
        root2 = self.find_byid(user_id2)

        # schon in derselben Gruppe
        if root1 is root2:
            return

        # kleineren Baum unter den größeren hängen und Gewicht der neuen Wurzel erhöhen
        if root1.weight < root2.weight:
            root1.set_parent(root2)
            root2.weight = root2.weight + root1.weight
        else:
            root2.set_parent(root1)
            root1.weight = root1.weight + root2.weight

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
            self[u].praktikumsgruppe = groupnumbers[i]

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
            if (self[u].praktikumsgruppe == self[user_id]._praktikumsgruppe):
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
