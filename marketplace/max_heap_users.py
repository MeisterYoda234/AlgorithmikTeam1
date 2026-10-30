"""Übersicht über den Dateiinhalt:

Implementiert den MaxHeapUsers zur effizienten Ermittlung des am besten bewerteten Benutzers.
Der Benutzer mit dem höchsten Sterne-Durchschnitt befindet sich an der Spitze des Heaps.
Die Heap-Logik (inkl. Hashtabelle für die Positionen) wird vom MaxHeap geerbt; diese Klasse
stellt nur passende Methodennamen für Benutzer bereit.
"""

# Teilprojekt 2, Aufgabe 2

from typing import Optional, Tuple

from marketplace.max_heap import MaxHeap


class MaxHeapUsers(MaxHeap):
    """Max-Heap für bewertete Benutzer, Einträge sind (stars_mean, user_id).

    Attributes:
        heap (List[Tuple[float, str]]): Liste von (stars_mean, user_id) Tupeln (geerbt).
        auction_map (Dict[str, Tuple[float, int]]): Hash-Map (user_id -> (stars_mean, heap_index)) (geerbt).
    """

    # *** PUBLIC methods ***

    def add_user(self, user_id: str, stars_mean: float) -> None:
        """Fügt einen neuen Benutzer zum Max-Heap hinzu.

        Args:
            user_id (str): Benutzer-ID.
            stars_mean (float): Sterne-Durchschnitt des Benutzers.

        Returns:
            None

        Raises:
            ValueError: Wenn der Benutzer bereits im Heap existiert.
        """
        self.add(user_id, stars_mean)

    def update_user(self, user_id: str, new_stars_mean: float) -> None:
        """Aktualisiert den Sterne-Durchschnitt eines Benutzers im Heap.

        Der Durchschnitt kann durch eine schlechte Bewertung auch sinken,
        update() verschiebt deshalb je nach Richtung nach oben oder nach unten.

        Args:
            user_id (str): Benutzer-ID.
            new_stars_mean (float): Neuer Sterne-Durchschnitt.

        Returns:
            None

        Raises:
            ValueError: Wenn der Benutzer nicht im Heap existiert.
        """
        self.update(user_id, new_stars_mean)

    def get_top_user(self) -> Optional[Tuple[float, str]]:
        """Gibt den Benutzer mit dem höchsten Sterne-Durchschnitt zurück.

        Args:
            None

        Returns:
            Optional[Tuple[float, str]]: Tupel aus (stars_mean, user_id) oder `None`, wenn der Heap leer ist.

        Raises:
            None
        """
        return self.get_max()

    def get_user_stars(self, user_id: str) -> Optional[float]:
        """Gibt den gespeicherten Sterne-Durchschnitt eines Benutzers zurück.

        Args:
            user_id (str): Benutzer-ID.

        Returns:
            Optional[float]: Sterne-Durchschnitt oder `None`, falls der Benutzer nicht im Heap ist.

        Raises:
            None
        """
        return self.get_value(user_id)
