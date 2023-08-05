import logging
from contextlib import suppress
from datetime import datetime

from typing_extensions import Self

from ._util import _frmt_str_to_datetime, _regex_it
from .api import _APIClient
from .base import PlayerObject
from .config import get_from_cache, set_in_cache
from .constants import _TMIO
from .errors import TMIOException
from .matchmaking import PlayerMatchmaking
from .trophy import PlayerTrophies

_log = logging.getLogger(__name__)

__all__ = (
    "PlayerMetaInfo",
    "PlayerZone",
    "PlayerSearchResult",
    "PlayerMatchmaking",
    "Player",
)


class PlayerMetaInfo(PlayerObject):
    """
    .. versionadded :: 0.1.0

    Represents Player Meta Data, which inclues YT, Twitch, Twitter or TMIO Vanity Link

    Parameters
    ----------
    display_url : str
        The URL to the player's profile
    in_nadeo : bool
        Whether the player is in Nadeo
    in_tmgl : bool
        Whether the player is in TMGL
    in_tmio_dev_team : bool
        Whether the player is in TMIO Dev Team
    is_sponsor : bool
        Whether the player is a sponsor
    sponsor_level : int | None
        The sponsor level of the player
    twitch : str | None
        The Twitch URL of the player, `NoneType` if the player has no Twitch
    twitter : str | None
        The Twitter URL of the player, `NoneType` if the player has no Twitter
    youtube : str | None
        The YouTube URL of the player, `NoneType` if the player has no YouTube
    vanity : str | None
        The TMIO Vanity URL of the player, `NoneType` if the player has no TMIO Vanity URL
    """

    def __init__(
        self,
        display_url: str,
        in_nadeo: bool,
        in_tmgl: bool,
        in_tmio_dev_team: bool,
        is_sponsor: bool,
        sponsor_level: int | None,
        twitch: str | None,
        twitter: str | None,
        youtube: str | None,
        vanity: str | None,
    ):
        """
        Constructor method.
        """
        self.display_url = display_url
        self.in_nadeo = in_nadeo
        self.in_tmgl = in_tmgl
        self.in_tmio_dev_team = in_tmio_dev_team
        self.is_sponsor = is_sponsor
        self.sponsor_level = sponsor_level
        self.twitch = twitch
        self.twitter = twitter
        self.youtube = youtube
        self.vanity = vanity

    @classmethod
    def _from_dict(cls, meta_data: dict) -> Self:
        """
        .. versionadded :: 0.1.0

        Parses the meta data into a PlayerMetaInfo object.

        Parameters
        ----------
        meta_data : dict
            The meta data to parse
        Returns
        -------
        :class:`PlayerMetaInfo`
            The parsed meta data
        """
        _log.debug(f"Creating a PlayerMetaInfo class from the given dictionary.")

        return cls(
            display_url=meta_data.get("displayurl"),
            in_nadeo=meta_data.get("nadeo", False),
            in_tmgl=meta_data.get("tmgl", False),
            in_tmio_dev_team=meta_data.get("team", False),
            is_sponsor=meta_data.get("sponsor", False),
            sponsor_level=meta_data.get("sponsor_level", 0),
            twitch=meta_data.get("twitch"),
            twitter=meta_data.get("twitter"),
            youtube=meta_data.get("youtube"),
            vanity=meta_data.get("vanity"),
        )


class PlayerZone(PlayerObject):
    """
    .. versionadded :: 0.1.0

    Class that represents the player zone

    Parameters
    ----------
    flag : str
        The flag of the zone
    zone : str
        The zone name
    rank : int
        The rank of the player in the zone
    """

    def __init__(self, flag: str, zone: str, rank: int):
        """Constructor method."""
        self.flag = flag
        self.zone = zone
        self.rank = rank

    @classmethod
    def _parse_zones(cls: Self, zones: dict, zone_positions: list[int]) -> list[Self]:
        """
          .. versionadded :: 0.1.0

        Parses the Data from the API into a list of PlayerZone objects.

         Parameters
         ----------
         zones : :class:`dict`
             the zones data from the API.
         zone_positions : :class:`list[int]`
             The zone positions data from the API.
         Returns
         -------
         class:`list[PlayerZone]`
             The list of :class:`PlayerZone` objects.
        """
        _log.debug("Parsing Zones")
        player_zone_list: list = []
        i: int = 0

        while "name" in zones:
            _log.debug(f"Gone {i} Levels Deep")
            player_zone_list.append(
                cls(zones["flag"], zones["name"], zone_positions[i])
            )
            i += 1

            if "parent" in zones:
                zones = zones["parent"]
            else:
                break

        return player_zone_list

    @staticmethod
    def to_string(
        player_zones: list[Self] | None, add_pos: bool = True, inline: bool = False
    ) -> str | None:
        """
        .. versionadded :: 0.4.0

        Prints a list of zones in a readable format.

        Parameters
        ----------
        player_zones : :class:`list[Self]`
            The list of :class:`PlayerZone` objects.
        add_pos : bool
            .. versionadded:: 0.4.0
            Whether to add the position of the zone.
        inline : bool
            .. versionadded :: 0.4.0
            Whether to print the zones in a single line.

        Returns
        -------
        str
            The list of zones in a readable format.
        """
        if player_zones is None:
            return None

        zone_str = ""

        if not inline:
            if add_pos:
                for zone in player_zones:
                    zone_str = zone_str + zone.zone + " - " + str(zone.rank) + "\n"
            else:
                for zone in player_zones:
                    zone_str = zone_str + zone.zone + "\n"
        else:
            if add_pos:
                zone_str = ", ".join(
                    f"{zone.zone} - {zone.rank}" for zone in player_zones
                )
            else:
                zone_str = ", ".join(zone.zone for zone in player_zones)

        return zone_str


class PlayerSearchResult(PlayerObject):
    """
    .. versionadded :: 0.1.0

    Represents 1 Player from a Search Result

    Parameters
    ----------
    club_tag : str | None.
        The club tag of the player, `NoneType` if the player is not in a club.
    name : str
        Name of the player.
    player_id : str
        The Trackmania ID of the player.
    zone : :class:`list[PlayerZone]`, optional
        The zone of the player as a list.
    threes : :class:`PlayerMatchmaking`, optional
        The 3v3 data of the player.
    royal : :class:`PlayerMatchmaking`, optional
        The royal data of the player.
    """

    def __init__(
        self,
        club_tag: str | None,
        name: str,
        player_id: str,
        zone: list[PlayerZone],
        threes: PlayerMatchmaking | None,
        royal: PlayerMatchmaking | None,
    ):
        self.club_tag = club_tag
        self.name = name
        self.player_id = player_id
        self.zone = zone
        self.threes = threes
        self.royal = royal

    @classmethod
    def _from_dict(cls: Self, player_data: dict) -> Self:
        _log.debug("Creating a PlayerSearchResult class from given dictionary")

        zone = (
            PlayerZone._parse_zones(player_data["player"]["zone"], [0, 0, 0, 0, 0])
            if "zone" in player_data["player"]
            else None
        )
        club_tag = _regex_it(player_data.get("player").get("club_tag", None))
        name = _regex_it(player_data.get("player").get("name"))
        player_id = player_data.get("player").get("id")
        matchmaking = PlayerMatchmaking._from_dict(
            player_data.get("matchmaking"), player_id
        )

        return cls(club_tag, name, player_id, zone, matchmaking[0], matchmaking[1])


class Player(PlayerObject):
    """
    .. versionadded :: 0.1.0

    Represents a Player in Trackmania

    Parameters
    ----------
    club_tag : str | None.
        The club tag of the player, `NoneType` if the player is not in a club.
    first_login : :class:`datetime` | None
        The date of the first login of the player.
    player_id : str
        The Trackmania ID of the player.
    last_club_tag_change : str
        The date of the last club tag change of the player.
    meta : :class:`PlayerMetaInfo`.
        Meta data of the player.
    name : str
        Name of the player.
    trophies : :class:`PlayerTrophies`, optional
        The trophies of the player.
    zone : :class:`list[PlayerZone]`, optional
        The zone of the player as a list.
    m3v3_data : :class:`PlayerMatchmaking`, optional
        The 3v3 data of the player.
    royal_data : :class:`PlayerMatchmaking`, optional
        The royal data of the player.
    """

    def __init__(
        self,
        club_tag: str | None,
        first_login: datetime | None,
        player_id: str,
        last_club_tag_change: str,
        meta: PlayerMetaInfo,
        name: str,
        trophies: PlayerTrophies | None = None,
        zone: list[PlayerZone] | None = None,
        m3v3_data: PlayerMatchmaking | None = None,
        royal_data: PlayerMatchmaking | None = None,
    ):
        """Constructor of the class."""
        self.club_tag = club_tag
        self._first_login = first_login
        self._id = player_id
        self.last_club_tag_change = last_club_tag_change
        self.meta = meta
        self.name = name
        self.trophies = trophies
        self.zone = zone
        self.m3v3_data = m3v3_data
        self.royal_data = royal_data

    def __str__(self) -> str:
        """String representation of the class."""
        return f"Player: {self.name} ({self.player_id})"

    @property
    def first_login(self):
        """first login property."""
        return self._first_login

    @property
    def player_id(self):
        """player id property."""
        return self._id

    @classmethod
    async def get_player(cls: Self, player_id: str) -> Self:
        """
        .. versionadded :: 0.1.0

        Gets a player's data from their player_id

        Parameters
        ----------
        player_id : str
            The player id of the player
        """
        _log.debug(f"Getting {player_id}'s data")

        player_data = get_from_cache(f"player:{player_id}")
        if player_data is not None:
            return cls(**Player._parse_player(player_data))

        api_client = _APIClient()
        player_data = await api_client.get(_TMIO.build([_TMIO.TABS.PLAYER, player_id]))
        await api_client.close()

        with suppress(KeyError, TypeError):
            raise TMIOException(player_data["error"])

        set_in_cache(f"player:{player_id}", player_data, ex=21600)
        set_in_cache(f"{player_data['displayname'].lower()}:id", player_id)

        return cls(**Player._parse_player(player_data))

    @staticmethod
    async def search(
        username: str,
    ) -> list[PlayerSearchResult]:
        """
        .. versionadded :: 0.1.0
        .. versionchanged :: 0.3.4
            The function no longer returns a single :class:`PlayerSearchResult`. It will now always return a `list` or `None`
        .. versionchanged :: 0.5.0
            The function no longer returns a NoneType. It will return an empty list instead.

        Searches for a player's information using their username.

        Parameters
        ----------
        username : str
            The player's username to search for

        Returns
        -------
        :class:`list[PlayerSearchResult]`
            Returns a list of :class:`PlayerSearchResult` with users who have similar usernames. Returns an empty list
            if no user with that username can be found.
        """
        _log.debug(f"Searching for players with the username -> {username}")

        api_client = _APIClient()
        search_result = await api_client.get(
            _TMIO.build([_TMIO.TABS.PLAYERS]) + f"/find?search={username}"
        )
        await api_client.close()

        with suppress(KeyError, TypeError):
            raise TMIOException(search_result["error"])

        if len(search_result) == 0:
            return []

        players = []
        for player in search_result:
            players.append(PlayerSearchResult._from_dict(player))

        return players

    @staticmethod
    async def get_id(username: str) -> str:
        """
        .. versionadded :: 0.1.0
        .. versionadded :: 0.3.4
            Updated to work with the change in `search` function

        Gets a player's id from the given username

        Parameters
        ----------
        username : str
            The player's username to get the ID for.

        Returns
        -------
        str
            The player's id.
        """
        _log.debug(f"Getting {username}'s id")

        player_id = get_from_cache(f"{username.lower()}:id")
        if player_id is not None:
            return player_id

        players = await Player.search(username)

        set_in_cache(f"{username.lower()}:id", players[0].player_id)

        return players[0].player_id

    @staticmethod
    async def get_username(player_id: str) -> str:
        """
        .. versionadded :: 0.1.0

        Gets a player's username from their player id

        Parameters
        ----------
        player_id : str
            The player id of the player

        Returns
        -------
        str
            The player's username
        """
        _log.debug(f"Getting the username for {player_id}")

        player_username = get_from_cache(f"{player_id}:username")
        if player_username is not None:
            return player_username

        player: Player = await Player.get_player(player_id)

        set_in_cache(f"{player_id}:username", player.name)

        return player.name

    @staticmethod
    def _parse_player(player_data: dict) -> dict:
        """
        .. versionadded :: 0.1.0
        .. versionchanged :: 0.4.0
            Optimized everything!

        Parses the player data

        Parameters
        ----------
        player_data : :class:`dict`
            The player data as a dictionary

        Returns
        -------
        :class:`dict`
            The parsed player data formatted kwargs friendly for the :class:`Player` constructors
        """
        first_login = _frmt_str_to_datetime(player_data.get("timestamp"))

        last_club_tag_change = _frmt_str_to_datetime(
            player_data.get("clubtagtimestamp")
        )

        # Parsing Meta
        if player_data.get("meta") is not None:
            if isinstance(player_data["meta"], PlayerMetaInfo):
                player_meta = player_data.get("meta")
            else:
                player_meta = PlayerMetaInfo._from_dict(player_data.get("meta"))
        else:
            player_meta = PlayerMetaInfo._from_dict(dict())

        # Parsing Trophies
        player_trophies = player_data.get("trophies")
        if player_trophies is not None:
            player_trophies = PlayerTrophies._from_dict(
                player_trophies,
                player_data.get("accountid", player_data.get("player_id")),
            )

        # Parsing Zones
        if (
            player_trophies is not None
            and player_data.get("trophies").get("zone") is not None
        ):
            player_zone = PlayerZone._parse_zones(
                player_data.get("trophies").get("zone"),
                player_data.get("trophies").get("zonepositions"),
            )
        else:
            player_zone = False

        # Parsing player id
        player_id = player_data.get(
            "accountid", player_data.get("id", player_data.get("playerid", None))
        )

        # Parsing Matchmaking
        matchmaking = (
            PlayerMatchmaking._from_dict(player_data["matchmaking"], player_id)
            if "matchmaking" in player_data
            else [None, None]
        )

        # Parsing Club Tag
        club_tag = player_data.get("clubtag", player_data.get("tag", None))
        club_tag = _regex_it(club_tag)

        # Parsing Name
        name = player_data.get("displayname", player_data.get("name", None))
        name = _regex_it(name)

        return {
            "club_tag": club_tag,
            "first_login": first_login,
            "name": name,
            "player_id": player_id,
            "last_club_tag_change": last_club_tag_change,
            "meta": player_meta,
            "trophies": player_trophies,
            "zone": player_zone,
            "m3v3_data": matchmaking[0],
            "royal_data": matchmaking[1],
        }
