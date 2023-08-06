"""
a casper7 plugin that reacts to wordle results

Usage:
    casper7-plugin-wordle-reactions [options] react <args>
    casper7-plugin-wordle-reactions --listeners
    casper7-plugin-wordle-reactions (-h | --help)
    casper7-plugin-wordle-reactions --version

Options:
    -g --guild GUILD_ID         Guild ID the message is coming from.
    -c --channel CHANNEL_ID     Channel ID the message is coming from.
    -u --user USER_ID           User ID the message is coming from.
    -m --message MESSAGE_ID     ID of the message that was sent.
    --listeners                 Get listener config JSON.
    -h --help                   Show this screen.
    --version                   Show version.
"""
import json
import re
from importlib.metadata import version

from docopt import docopt

from casper7_plugin_wordle_reactions.settings import settings

reactions = [
    (re.compile(r"wordle \d+ [1-6]/6"), ":brain:"),
    (re.compile(r"wordle \d+ X/6"), ":snail:"),
    (re.compile(r"daily duotrigordle #\d+\nguesses: \d+/37"), ":brain:"),
    (re.compile(r"daily duotrigordle #\d+\nguesses: X/37"), ":snail:"),
    (re.compile(r"scholardle \d+ [1-6]/6"), ":mortar_board:"),
    (re.compile(r"scholardle \d+ X/6"), ":snail:"),
    (re.compile(r"worldle #\d+ [1-6]/6 \(100%\)"), ":map"),
    (re.compile(r"worldle #\d+ X/6 \(\d+%\)"), ":snail:"),
    (re.compile(r"waffle\d+ [0-5]/5"), ":waffle:"),
    (re.compile(r"waffle\d+ 5/5"), ":star:"),
    (re.compile(r"waffle\d+ X/5"), ":snail:"),
    (re.compile(r"#wafflesilverteam"), ":second_place:"),
    (re.compile(r"#wafflegoldteam"), ":first_place:"),
    (re.compile(r"flowdle \d+ \[\d+ moves\]"), ":potable_water:"),
    (re.compile(r"jurassic wordle \(game #\d+\) - [1-8] / 8"), ":sauropod:"),
    (re.compile(r"jurassic wordle \(game #\d+\) - X / 8"), ":snail:"),
    (re.compile(r"jungdle \(game #\d+\) - [1-8] / 8"), ":lion:"),
    (re.compile(r"jungdle \(game #\d+\) - X / 8"), ":snail:"),
    (re.compile(r"dogsdle \(game #\d+\) - [1-8] / 8"), ":dog:"),
    (re.compile(r"dogsdle \(game #\d+\) - X / 8"), ":snail:"),
    # TODO: framed
    # TODO: moviedle
    # TODO: posterdle
    # TODO: namethatride
    # TODO: heardle
]


def print_listeners() -> None:
    """Print listener config JSON."""
    print(
        json.dumps(
            {
                "listeners": [
                    {
                        "name": "react",
                    }
                ]
            }
        )
    )


def maybe_react(message: str, *, channel_id: int, message_id: int) -> None:
    """Check if a message contains any known patterns and emit add_reaction events."""
    if channel_id not in settings.wordle_channels:
        return

    events = []
    for pattern, emoji in reactions:
        if pattern.search(message):
            events.append(
                {
                    "type": "add_reaction",
                    "channel_id": channel_id,
                    "message_id": message_id,
                    "emoji": emoji,
                }
            )
    print(json.dumps(events))


def plugin() -> None:
    """Plugin entrypoint."""
    args = docopt(
        __doc__, version=f"casper7-plugin-wordle-reactions {version(__package__)}"
    )

    if args["<args>"]:
        args["<args>"] = json.loads(args["<args>"])

    channel_id = args["--channel"]
    message_id = args["--message"]

    match args:
        case {"--listeners": True}:
            print_listeners()
        case {"react": True, "<args>": {"message": message}}:
            maybe_react(message, channel_id=channel_id, message_id=message_id)
