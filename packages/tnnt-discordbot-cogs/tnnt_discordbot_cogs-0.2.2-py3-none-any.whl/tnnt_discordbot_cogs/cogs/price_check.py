"""
Market Price Checks
"""

# Standard Library
import logging

# Third Party
import requests
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands

logger = logging.getLogger(__name__)


class PriceCheck(commands.Cog):
    """
    Price checks on Jita, Amarr, Rens, Hek, Dodixie and Perimeter markets
    """

    imageserver_url = "https://images.evetech.net"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def price(self, ctx):
        """
        Check an item price on all major market hubs
        :param ctx:
        :return:
        """

        markets = [
            {"name": "Jita", "api_key": "jita"},
            {"name": "Amarr", "api_key": "amarr"},
            {"name": "Rens", "api_key": "rens"},
            {"name": "Hek", "api_key": "hek"},
            {"name": "Dodixie", "api_key": "dodixie"},
            {"name": "Perimeter", "api_key": "perimeter"},
        ]

        await ctx.trigger_typing()

        item_name = ctx.message.content[7:]

        await self.price_check(ctx=ctx, markets=markets, item_name=item_name)

    @commands.command(pass_context=True)
    async def jita(self, ctx):
        """
        Check an item price on Jita market
        :param ctx:
        :return:
        """

        markets = [
            {"name": "Jita", "api_key": "jita"},
        ]

        await ctx.trigger_typing()

        item_name = ctx.message.content[6:]

        await self.price_check(ctx=ctx, markets=markets, item_name=item_name)

    @commands.command(pass_context=True)
    async def amarr(self, ctx):
        """
        Check an item price on Amarr market
        :param ctx:
        :return:
        """

        markets = [
            {"name": "Amarr", "api_key": "amarr"},
        ]

        await ctx.trigger_typing()

        item_name = ctx.message.content[7:]

        await self.price_check(ctx=ctx, markets=markets, item_name=item_name)

    async def price_check(self, ctx, markets, item_name: str = None):
        """
        Do the price checks and post to Discord
        :param ctx:
        :param markets:
        :param item_name:
        :return:
        """

        has_thumbnail = False

        await ctx.trigger_typing()

        if item_name != "":
            embed = Embed(
                title=f"Price Lookup for {item_name}",
                color=Color.green(),
            )

            for market in markets:
                embed.add_field(
                    name=market["name"],
                    value=f'Prices for {item_name} on the {market["name"]} Market.',
                    inline=False,
                )

                market_data = requests.post(
                    "https://evepraisal.com/appraisal/structured.json",
                    json={
                        "market_name": market["api_key"],
                        "items": [{"name": item_name}],
                    },
                )

                if market_data.status_code == 200:
                    market_json = market_data.json()

                    type_id = market_json["appraisal"]["items"][0]["typeID"]
                    sell_min = market_json["appraisal"]["items"][0]["prices"]["sell"][
                        "min"
                    ]
                    sell_order_count = market_json["appraisal"]["items"][0]["prices"][
                        "sell"
                    ]["order_count"]
                    buy_max = market_json["appraisal"]["items"][0]["prices"]["buy"][
                        "max"
                    ]
                    buy_order_count = market_json["appraisal"]["items"][0]["prices"][
                        "buy"
                    ]["order_count"]
                    thumbnail_url = (
                        f"{self.imageserver_url}/types/{type_id}/icon?size=64"
                    )

                    if has_thumbnail is False:
                        embed.set_thumbnail(url=thumbnail_url)

                        has_thumbnail = True

                    # Sell order price
                    market_min_sell_order_price = f"{sell_min:,} ISK"

                    if sell_order_count == 0:
                        market_min_sell_order_price = "No sell orders found"

                    embed.add_field(
                        name=f"Sell Order Price ({sell_order_count} Orders)",
                        value=market_min_sell_order_price,
                        inline=True,
                    )

                    # Buy order price
                    market_max_buy_order_price = f"{buy_max:,} ISK"

                    if buy_order_count == 0:
                        market_max_buy_order_price = "No buy orders found"

                    embed.add_field(
                        name=f"Buy Order Price ({buy_order_count} Orders)",
                        value=market_max_buy_order_price,
                        inline=True,
                    )
                else:
                    embed.add_field(
                        name="API Error",
                        value=(
                            f"Could not not fetch the price "
                            f'for the {market["name"]} market.'
                        ),
                        inline=False,
                    )
        else:
            embed = Embed(
                title="Price Lookup",
                color=Color.red(),
            )

            embed.add_field(
                name="Error",
                value=(
                    "You forget to enter an item you want to lookup the price for ..."
                ),
                inline=False,
            )

        return await ctx.send(embed=embed)


def setup(bot):
    """
    Add the cogg
    :param bot:
    :return:
    """

    bot.add_cog(PriceCheck(bot))
