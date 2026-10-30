"""Übersicht über den Dateiinhalt:

Implementiert den MaxHeap zur effizienten Verwaltung von Auktionen basierend
auf der Anzahl der abgegebenen Gebote. Die Auktion mit den meisten Geboten
befindet sich an der Spitze des Heaps.

Die eigentliche Heap-Logik steckt in allgemein benannten Methoden (add, update, remove,
get_max, get_value), damit derselbe Heap auch für andere Schlüssel/Werte genutzt werden kann
(s. MaxHeapUsers in max_heap_users.py). Die vorgegebenen Auktions-Methoden rufen diese nur auf.
"""

# Status: FINAL, dgaida2, 15.10.2024

# Die Klasse MaxHeap implementiert einen Max-Heap

from typing import Any, Dict, List, Optional, Tuple


class MaxHeap:
    """Klasse zur Repräsentation eines Max-Heaps für Auktionen.

    Attributes:
        heap (List[Tuple[Any, str]]): Liste von (wert, schlüssel) Tupeln, bei Auktionen (bid_count, auction_id).
        auction_map (Dict[str, Tuple[Any, int]]): Hash-Map (schlüssel -> (wert, heap_index)).
    """

    def __init__(self) -> None:
        """Initialisiert eine neue MaxHeap-Instanz.

        Args:
            None

        Raises:
            None
        """
        """ Initialisierung des Max-Heaps.
            Ein Knoten speichert die Anzahl der Bieter für eine Auktion sowie die ID-Nummer der Auktion.
            Die Auktion mit den meisten Bietern soll an der Spitze des Max-Heaps stehen.

        heap: Eine Liste zur Speicherung des Heaps, bestehend aus Tupeln in der Form (bid_count, auction_id).
        auction_map: Eine Hash-Map, welche die Position der Auktionen im Max-Heap speichert.
                     (key = auction_id, value = (bid_count, heap_index))
        """
        self.heap: List[Tuple[Any, str]] = []
        self.auction_map: Dict[str, Tuple[Any, int]] = {}

    # *** PUBLIC methods (allgemein) ***

    def add(self, key: str, value: Any) -> None:
        """Fügt einen neuen Eintrag zum Max-Heap hinzu.

        Args:
            key (str): Eindeutiger Schlüssel (z. B. Auktions-ID oder Benutzer-ID).
            value (Any): Vergleichbarer Wert, nach dem sortiert wird.

        Returns:
            None

        Raises:
            ValueError: Wenn der Schlüssel bereits im Heap existiert.
        """
        if key in self.auction_map:
            raise ValueError("Eintrag existiert bereits")

        index = len(self.heap)
        self.heap.append((value, key))
        self.auction_map[key] = (value, index)
        self._heapify_up(index)

    def update(self, key: str, new_value: Any) -> None:
        """Aktualisiert den Wert eines existierenden Eintrags im Heap.

        Je nach Richtung der Änderung wird der Eintrag nach oben oder unten verschoben.

        Args:
            key (str): Schlüssel des Eintrags.
            new_value (Any): Neuer Wert.

        Returns:
            None

        Raises:
            ValueError: Wenn der Schlüssel nicht im Heap existiert.
        """
        if key not in self.auction_map:
            raise ValueError("Eintrag existiert nicht")

        old_value, index = self.auction_map[key]
        self.heap[index] = (new_value, key)
        self.auction_map[key] = (new_value, index)
        if new_value > old_value:
            self._heapify_up(index)
        elif new_value < old_value:
            self._heapify_down(index)

    def remove(self, key: str) -> None:
        """Entfernt einen Eintrag aus dem Max-Heap.

        Args:
            key (str): Schlüssel des Eintrags (bei Auktionen die Auktions-ID).

        Returns:
            None

        Raises:
            ValueError: Wenn der Schlüssel nicht im Heap existiert.
        """
        if key not in self.auction_map:
            raise ValueError("Eintrag existiert nicht")

        _, index = self.auction_map[key]
        self._swap(index, len(self.heap) - 1)
        self.heap.pop()
        del self.auction_map[key]

        if index < len(self.heap):
            parent = (index - 1) // 2
            if index > 0 and self.heap[index][0] > self.heap[parent][0]:
                self._heapify_up(index)
            else:
                self._heapify_down(index)

    def get_max(self) -> Optional[Tuple[Any, str]]:
        """Gibt den Eintrag mit dem größten Wert an der Spitze des Heaps zurück.

        Args:
            None

        Returns:
            Optional[Tuple[Any, str]]: Tupel aus (wert, schlüssel) oder `None`, wenn der Heap leer ist.

        Raises:
            None
        """
        if not self.heap:
            return None
        return self.heap[0][0], self.heap[0][1]

    def get_value(self, key: str) -> Optional[Any]:
        """Gibt den gespeicherten Wert eines Eintrags zurück.

        Args:
            key (str): Schlüssel des Eintrags.

        Returns:
            Optional[Any]: Wert oder `None`, falls der Schlüssel nicht vorhanden ist.

        Raises:
            None
        """
        if key in self.auction_map:
            return self.auction_map[key][0]
        return None

    # *** PUBLIC methods (vorgegebene Auktions-Schnittstelle) ***

    def add_auction(self, auction_id: str, bid_count: int) -> None:
        """Fügt eine neue Auktion zum Max-Heap hinzu.

        Args:
            auction_id (str): Auktions-ID.
            bid_count (int): Gebotsanzahl.

        Returns:
            None

        Raises:
            ValueError: Wenn die Auktion bereits im Heap existiert.
        """
        self.add(auction_id, bid_count)

    def update_bidders(self, auction_id: str, new_bid_count: int) -> None:
        """Aktualisiert die Gebotsanzahl einer existierenden Auktion im Heap.

        Args:
            auction_id (str): Auktions-ID.
            new_bid_count (int): Neue Gebotsanzahl.

        Returns:
            None

        Raises:
            ValueError: Wenn die Auktion nicht im Heap existiert.
        """
        self.update(auction_id, new_bid_count)

    def get_auction_with_max_bidders(self) -> Optional[Tuple[int, str]]:
        """Gibt die Auktion mit den meisten Geboten an der Spitze des Heaps zurück.

        Args:
            None

        Returns:
            Optional[Tuple[int, str]]: Tupel aus (bid_count, auction_id) oder `None`.

        Raises:
            None
        """
        return self.get_max()

    def get_auction_bidders(self, auction_id: str) -> Optional[int]:
        """Gibt die Gebotsanzahl einer Auktion zurück.

        Args:
            auction_id (str): Auktions-ID.

        Returns:
            Optional[int]: Gebotsanzahl oder `None`, falls nicht vorhanden.

        Raises:
            None
        """
        return self.get_value(auction_id)

    # *** PRIVATE methods ***

    def _swap(self, i: int, j: int) -> None:
        """ Hilfsfunktion zum Tauschen von zwei Einträgen im Max-Heap.
            Aktualisiert ebenfalls die Position der Einträge in der auction_map.

        Args:
            i: Index des ersten Eintrags im Max-Heap.
            j: Index des zweiten Eintrags im Max-Heap.
        """
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        value_i, key_i = self.heap[i]
        value_j, key_j = self.heap[j]
        self.auction_map[key_i] = (value_i, i)
        self.auction_map[key_j] = (value_j, j)

    def _heapify_up(self, index: int) -> None:
        """ Führt das Heapify-Up-Verfahren durch, um die Heap-Eigenschaft nach oben hin wiederherzustellen.

        Args:
            index: Der Index des Elements, das nach oben "heapified" werden soll.
        """
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index][0] <= self.heap[parent][0]:
                break
            self._swap(index, parent)
            index = parent

    def _heapify_down(self, index: int) -> None:
        """ Führt das Heapify-Down-Verfahren durch, um die Heap-Eigenschaft nach unten hin wiederherzustellen.

        Args:
            index: Der Index des Elements, das nach unten "heapified" werden soll.
        """
        while 2 * index + 1 < len(self.heap):
            left = 2 * index + 1
            right = left + 1
            largest = left
            if right < len(self.heap) and self.heap[right][0] > self.heap[left][0]:
                largest = right
            if self.heap[index][0] >= self.heap[largest][0]:
                break
            self._swap(index, largest)
            index = largest
