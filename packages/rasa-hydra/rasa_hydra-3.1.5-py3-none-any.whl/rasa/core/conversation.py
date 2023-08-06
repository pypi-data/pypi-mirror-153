from typing import Dict, List, Text, Any

from rasa.core.events import Event


class Dialogue:
    """A dialogue comprises a list of Turn objects"""

    def __init__(self, name: Text, events: List["Event"], total_steps=0, total_errors=0) -> None:
        """This function initialises the dialogue with the dialogue name and the event
        list."""
        self.name = name
        self.total_steps = total_steps
        self.total_errors = total_errors
        self.events = events

    def __str__(self) -> Text:
        """This function returns the dialogue and turns."""
        return "Dialogue with name '{}' and turns:\n{}".format(
            self.name, "\n\n".join([f"\t{t}" for t in self.events])
        )

    def as_dict(self) -> Dict:
        """This function returns the dialogue as a dictionary to assist in
        serialization."""
        return {"events": [event.as_dict() for event in self.events], "name": self.name,
                "total_steps": self.total_steps, "total_errors": self.total_errors}

    @classmethod
    def from_parameters(cls, parameters: Dict[Text, Any]) -> "Dialogue":
        """Create `Dialogue` from parameters.

        Args:
            parameters: Serialised dialogue, should contain keys 'name' and 'events'.

        Returns:
            Deserialised `Dialogue`.

        """

        return cls(
            parameters.get("name"),
            [Event.from_parameters(evt) for evt in parameters.get("events")],
            parameters.get("total_steps"),
            parameters.get("total_errors"),
        )
