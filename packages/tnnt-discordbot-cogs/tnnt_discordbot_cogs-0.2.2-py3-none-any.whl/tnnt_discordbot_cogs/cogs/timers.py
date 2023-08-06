"""
All about the timers ....
"""

# Standard Library
import datetime
import logging

# Third Party
from aadiscordbot.app_settings import ADMIN_DISCORD_BOT_CHANNELS, get_site_url
from aadiscordbot.cogs.utils.decorators import message_in_channels
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands
from structuretimers.models import Timer

# Django
from django.apps import apps
from django.utils import timezone

# Alliance Auth
from allianceauth.eveonline.templatetags.evelinks import dotlan_solar_system_url

logger = logging.getLogger(__name__)


def structuretimers_active():
    """
    Check if "structuretimers" is installed
    :return:
    :rtype:
    """

    return apps.is_installed("structuretimers")


def timezones_active():
    """
    Check if "timezones" is installed
    :return:
    :rtype:
    """

    return apps.is_installed("timezones")


class Timers(commands.Cog):
    """
    TimerBoard Stuffs!
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @message_in_channels(ADMIN_DISCORD_BOT_CHANNELS)
    async def timer(self, ctx):
        """
        Gets the Next Timer!
        :param ctx:
        :return:
        """

        embed = Embed(title="Next Timer")

        next_timer = Timer.objects.filter(
            is_opsec=False,
            visibility=Timer.VISIBILITY_UNRESTRICTED,
            date__gte=datetime.datetime.utcnow().replace(tzinfo=timezone.utc),
        ).first()

        if next_timer is None:
            embed.description = "No upcoming timer"
        else:
            if next_timer.objective == Timer.OBJECTIVE_FRIENDLY:
                embed.colour = Color.blue()
            elif next_timer.objective == Timer.OBJECTIVE_HOSTILE:
                embed.colour = Color.red()
            elif next_timer.objective == Timer.OBJECTIVE_NEUTRAL:
                embed.colour = Color.light_gray()
            elif next_timer.objective == Timer.OBJECTIVE_UNDEFINED:
                embed.colour = Color.dark_gray()
            else:
                embed.colour = Color.from_rgb(255, 255, 255)

            user_has_profile = True

            if next_timer.user is not None:
                creator_name = next_timer.user.username

                try:
                    creator_profile = next_timer.user.profile
                except Exception:
                    user_has_profile = False

                if user_has_profile is True:
                    if creator_profile.main_character is not None:
                        creator_name = creator_profile.main_character.character_name

                embed.set_footer(
                    text="Timer added by {creator_name}".format(
                        creator_name=creator_name
                    )
                )

            embed.add_field(name="Structure:", value=next_timer.structure_type.name)

            embed.add_field(
                name="Location:",
                value="{system}\n{location}".format(
                    system="[{solar_system_name}]({solar_system_link})".format(
                        solar_system_name=next_timer.eve_solar_system.name,
                        solar_system_link=dotlan_solar_system_url(
                            next_timer.eve_solar_system
                        ),
                    ),
                    location=next_timer.location_details,
                ),
            )

            if timezones_active():
                embed.add_field(
                    name="Eve Time:",
                    value="{eve_time} ({tz_link})".format(
                        eve_time=next_timer.date.strftime("%Y-%m-%d %H:%M"),
                        tz_link="[{tz_lnk_text}]({tz_link_url}/)".format(
                            tz_lnk_text="Time Zone Conversion",
                            tz_link_url=get_site_url()
                            + "/timezones/"
                            + str(int(next_timer.date.timestamp())),
                        ),
                    ),
                    inline=False,
                )
            else:
                embed.add_field(
                    name="Eve Time:",
                    value=next_timer.eve_time.strftime("%Y-%m-%d %H:%M"),
                    inline=False,
                )

        return await ctx.send(embed=embed)


def setup(bot):
    """
    Setup the cog
    :param bot:
    """

    if structuretimers_active():
        bot.add_cog(Timers(bot))
    else:
        logger.debug("Timerboard not installed")
