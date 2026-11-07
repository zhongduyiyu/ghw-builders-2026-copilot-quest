"""Builder Quest: a short, family-friendly choose-your-own-adventure game."""


SCENES = {
    "gate": {
        "text": "You arrive at the sunny Builder Fair. A workshop and a creek lie ahead.",
        "choices": {
            "1": "Visit the workshop",
            "2": "Head straight to the creek",
            "3": "Head home",
        },
    },
    "workshop": {
        "text": "The workshop is full of friendly builders and useful supplies.",
        "choices": {
            "1": "Pack a sturdy toolkit and go to the creek",
            "2": "Go to the creek without supplies",
            "3": "Return to the fair entrance",
        },
    },
    "creek": {
        "text": "A little creek blocks the path to the hilltop beacon.",
        "choices": {
            "1": "Build a safe crossing",
            "2": "Try to leap across",
            "3": "Head home",
        },
    },
    "summit": {
        "text": "You made it to the hilltop! The fair's beacon is ready to light.",
        "choices": {
            "1": "Light the beacon",
            "2": "Race along the ridge",
            "3": "Head home",
        },
    },
}

ENDING_TEXT = {
    "win": "The beacon shines across the fair! Everyone cheers. You are a Builder Quest champion!",
    "loss": "Splash! You land safely in the shallow creek, but the beacon will have to wait. Quest over!",
    "retreat": "You head home with a smile, ready for another adventure. Thanks for playing!",
}


class Game:
    """Holds the game state and applies choices without performing input or output."""

    def __init__(self):
        self.scene = "gate"
        self.inventory = set()
        self.score = 0
        self.ending = None

    @property
    def ended(self):
        return self.ending is not None

    def finish(self, ending):
        """End the game with one of its named endings."""
        if ending not in ENDING_TEXT:
            raise ValueError(f"Unknown ending: {ending}")
        self.ending = ending
        self.scene = "ending"

    def choose(self, choice):
        """Apply a numbered choice, or 'q' to quit. Return an error if invalid."""
        if self.ended:
            return "The game is already over."

        choice = str(choice).strip().lower()
        if choice == "q":
            self.finish("retreat")
            return ""

        options = SCENES[self.scene]["choices"]
        if choice not in options:
            return "That isn't a valid choice. Please enter a listed number or q."

        if self.scene == "gate":
            self.scene = {"1": "workshop", "2": "creek", "3": "ending"}[choice]
            if choice == "3":
                self.finish("retreat")

        elif self.scene == "workshop":
            if choice == "1":
                self.inventory.add("toolkit")
                self.score += 1
                self.scene = "creek"
            elif choice == "2":
                self.scene = "creek"
            else:
                self.scene = "gate"

        elif self.scene == "creek":
            if choice == "1" and "toolkit" in self.inventory:
                self.score += 2
                self.scene = "summit"
            elif choice == "3":
                self.finish("retreat")
            else:
                self.finish("loss")

        elif self.scene == "summit":
            if choice == "1" or (choice == "2" and "toolkit" in self.inventory):
                self.score += 3
                self.finish("win")
            elif choice == "3":
                self.finish("retreat")
            else:
                self.finish("loss")

        return ""


def run_game(input_fn=None, output_fn=None):
    """Run the command-line game; input and output functions are injectable for tests."""
    if input_fn is None:
        input_fn = input
    if output_fn is None:
        output_fn = print

    game = Game()
    output_fn("Welcome to Builder Quest! Help light the beacon at the Builder Fair.")
    output_fn("Enter a choice number, or q at any time to quit.")

    while not game.ended:
        scene = SCENES[game.scene]
        output_fn("")
        output_fn(scene["text"])
        for number, description in scene["choices"].items():
            output_fn(f"{number}. {description}")

        try:
            choice = input_fn("> ")
        except EOFError:
            game.finish("retreat")
            output_fn("")
            output_fn("Input ended, so your quest is ending here.")
            break

        message = game.choose(choice)
        if message:
            output_fn(message)

    output_fn("")
    output_fn(ENDING_TEXT[game.ending])
    return game


if __name__ == "__main__":
    run_game()