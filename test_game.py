import unittest

from game import ENDING_TEXT, Game, run_game


class GameTests(unittest.TestCase):
    def play(self, *choices):
        game = Game()
        for choice in choices:
            game.choose(choice)
        return game

    def test_toolkit_route_reaches_a_win(self):
        game = self.play("1", "1", "1", "1")
        self.assertEqual(game.ending, "win")
        self.assertIn("toolkit", game.inventory)
        self.assertEqual(game.score, 6)

    def test_safe_creek_crossing_requires_toolkit(self):
        game = self.play("2", "1")
        self.assertEqual(game.ending, "loss")
        self.assertNotIn("toolkit", game.inventory)

    def test_ridge_race_with_toolkit_is_a_win(self):
        game = self.play("1", "1", "1")
        self.assertEqual(game.scene, "summit")
        self.assertFalse(game.ended)
        game.choose("2")
        self.assertEqual(game.ending, "win")
        self.assertIn("toolkit", game.inventory)

    def test_ridge_race_without_toolkit_is_a_loss(self):
        # Defensive unit test: ordinary play requires the toolkit to reach the summit.
        game = Game()
        game.scene = "summit"
        game.choose("2")
        self.assertEqual(game.ending, "loss")

    def test_heading_home_from_gate(self):
        game = self.play("3")
        self.assertEqual(game.ending, "retreat")

    def test_heading_home_from_workshop_via_fair_entrance(self):
        game = self.play("1", "3", "3")
        self.assertEqual(game.ending, "retreat")

    def test_heading_home_from_creek(self):
        game = self.play("2", "3")
        self.assertEqual(game.ending, "retreat")

    def test_heading_home_from_summit(self):
        game = self.play("1", "1", "1", "3")
        self.assertEqual(game.ending, "retreat")

    def test_retreat_is_distinct_from_win(self):
        game = self.play("3")
        self.assertNotEqual(ENDING_TEXT[game.ending], ENDING_TEXT["win"])

    def test_quit_works_from_any_scene(self):
        for route in [(), ("1",), ("2",), ("1", "1", "1")]:
            with self.subTest(route=route):
                game = self.play(*route)
                self.assertFalse(game.ended)
                game.choose("q")
                self.assertEqual(game.ending, "retreat")

    def test_quit_accepts_uppercase_and_surrounding_whitespace(self):
        game = self.play("  Q  ")
        self.assertEqual(game.ending, "retreat")

    def test_invalid_choice_does_not_change_state(self):
        game = Game()
        before = (game.scene, set(game.inventory), game.score, game.ending)
        message = game.choose("9")
        self.assertIn("valid choice", message)
        self.assertEqual(
            (game.scene, game.inventory, game.score, game.ending), before
        )

    def test_invalid_choice_is_checked_for_current_scene(self):
        game = self.play("1")
        self.assertEqual(game.scene, "workshop")
        self.assertIn("valid choice", game.choose("4"))
        self.assertEqual(game.scene, "workshop")

    def test_new_game_starts_with_clean_state(self):
        first_game = self.play("1", "1")
        self.assertIn("toolkit", first_game.inventory)

        restarted_game = Game()
        self.assertEqual(restarted_game.scene, "gate")
        self.assertEqual(restarted_game.inventory, set())
        self.assertEqual(restarted_game.score, 0)
        self.assertIsNone(restarted_game.ending)

    def test_command_line_reprompts_after_invalid_input(self):
        inputs = iter(["invalid", "3"])
        output = []
        game = run_game(input_fn=lambda _prompt: next(inputs), output_fn=output.append)

        self.assertEqual(game.ending, "retreat")
        self.assertTrue(any("valid choice" in line for line in output))

    def test_eof_ends_gracefully(self):
        output = []

        def no_more_input(_prompt):
            raise EOFError

        game = run_game(input_fn=no_more_input, output_fn=output.append)
        self.assertEqual(game.ending, "retreat")
        self.assertTrue(any("Input ended" in line for line in output))
        self.assertTrue(any(ENDING_TEXT["retreat"] in line for line in output))

    def test_eof_after_progressing_to_workshop_ends_gracefully(self):
        inputs = iter(["1"])
        output = []

        def input_then_eof(_prompt):
            try:
                return next(inputs)
            except StopIteration:
                raise EOFError

        game = run_game(input_fn=input_then_eof, output_fn=output.append)
        self.assertEqual(game.ending, "retreat")
        self.assertTrue(any("workshop" in line.lower() for line in output))
        self.assertTrue(any("Input ended" in line for line in output))

    def test_game_rejects_choices_after_ending(self):
        game = self.play("q")
        self.assertIn("already over", game.choose("1"))
        self.assertEqual(game.ending, "retreat")


if __name__ == "__main__":
    unittest.main()
