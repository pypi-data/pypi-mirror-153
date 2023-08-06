"""Command line tool for sending messages to Discord server via gRPC."""
import argparse
import sys

from discordproxy.client import DiscordClient
from discordproxy.exceptions import DiscordProxyException

from . import _constants


def main():
    my_args = _parse_args(sys.argv[1:])
    target = f"{my_args.host}:{my_args.port}"
    client = DiscordClient(target=target)
    try:
        if my_args.type == "direct":
            client.create_direct_message(
                user_id=my_args.recipient_id, content=my_args.content
            )
        elif my_args.type == "channel":
            client.create_channel_message(
                channel_id=my_args.recipient_id, content=my_args.content
            )
        else:
            raise NotImplementedError(my_args.type)
    except DiscordProxyException as ex:
        print(f"ERROR: {ex}")
        exit(1)
    else:
        print("Message sent")


def _parse_args(sys_args: list) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Simple tool for sending messages via Discord Proxy. Connects via gRPC."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "type",
        choices=["direct", "channel"],
        help="wether to send a direct message or a channel message",
    )
    parser.add_argument(
        "recipient_id",
        type=int,
        help=(
            "ID of the recipient, i.e. the user ID for direct messages "
            "or the channel ID for channel messages"
        ),
    )
    parser.add_argument(
        "--host", default=_constants.DEFAULT_HOST, help="server host address"
    )
    parser.add_argument(
        "--port", type=int, default=_constants.DEFAULT_PORT, help="server port"
    )
    parser.add_argument("content", help="content of the message to be sent")
    return parser.parse_args(sys_args)


if __name__ == "__main__":
    main()
