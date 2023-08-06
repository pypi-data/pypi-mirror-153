import subprocess


def run_player(url: str, player: str = "mpv", **commands) -> None:
    """

    :param url: hls url
    :param player: local video player. Default mpv
    :param commands: send optional commands.
        key-param="value" convert to: --key-param=value or **{"my-key-param":"c"} = --my-key-param=c
    :return:
    """
    if commands:
        commands = " ".join((f'--{k}="{v}"' for k, v in commands.items()))
        subprocess.run([player, url, commands])
    else:
       subprocess.run([player, url])
