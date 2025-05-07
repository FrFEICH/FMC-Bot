import discord
from discord.ext import commands
from datetime import datetime, timezone
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

invite_cache = {}
invitation_count = {}

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")
    await asyncio.sleep(1)  # Laisse Discord initialiser les guilds

    for guild in bot.guilds:
        try:
            invites = await guild.invites()
            invite_cache[guild.id] = {invite.code: invite.uses for invite in invites}
        except Exception as e:
            print(f"Erreur lors de la récupération des invitations pour {guild.name} : {e}")

@bot.event
async def on_member_join(member):
    guild = member.guild
    welcome_channel = guild.get_channel(1349771541465923604)
    invite_channel = guild.get_channel(1367439123681509406)

    try:
        new_invites = await guild.invites()
    except Exception as e:
        print(f"Erreur lors de la récupération des nouvelles invitations : {e}")
        return

    old_invites = invite_cache.get(guild.id, {})
    invite_cache[guild.id] = {invite.code: invite.uses for invite in new_invites}

    inviter_user = None
    for invite in new_invites:
        old_uses = old_invites.get(invite.code, 0)
        if invite.uses > old_uses:
            inviter_user = invite.inviter
            break

    # Message de bienvenue
    if welcome_channel:
        await welcome_channel.send(f"👋 Bienvenue sur le serveur Discord [FMC] {member.mention} !")

        inviter_text = inviter_user.mention if inviter_user else "quelqu’un (invitation inconnue)"
        embed = discord.Embed(
            description=(
                "✨ Pour postuler, rends-toi dans <#1349694562192461890> puis dans <#1349729811953614858> pour postuler !\n"
                "Bonne chance 🍀\n\n"
                f"🧭 Il a été invité par {inviter_text}"
            ),
            color=discord.Color(0x007FFF)
        )
        embed.set_image(url="https://i.postimg.cc/JhVrnLMZ/IMG-20250503-180150.jpg")
        await welcome_channel.send(embed=embed)

    # Comptabiliser les invitations
    if invite_channel and inviter_user:
        inviter_id = inviter_user.id
        count = invitation_count.get(inviter_id, 0) + 1
        invitation_count[inviter_id] = count

        embed_invite = discord.Embed(
            description=(
                f"{inviter_user.mention} a invité {member.mention}.\n"
                f"🔢 Cela fait {count} invitation(s), "
                f"plus que {max(0, 30 - count)} pour gagner 10 Robux.\n"
                "Continue d'inviter des gens ! 🚀"
            ),
            color=discord.Color(0x007FFF)
        )
        await invite_channel.send(embed=embed_invite)

        if count == 30:
            reward_embed = discord.Embed(
                description=(
                    f"@everyone, {inviter_user.mention} a invité 30 personnes !\n"
                    f"Il vient de gagner **10 Robux**.\n"
                    f"{inviter_user.mention}, va voir <@1257714932561219635> pour obtenir ta récompense !"
                ),
                color=discord.Color.green()
            )
            await invite_channel.send(content="@everyone", embed=reward_embed)

@bot.event
async def on_member_remove(member):
    print(f"{member.name} a quitté le serveur.")
    join_date = member.joined_at

    if join_date is not None and join_date.tzinfo is None:
        join_date = join_date.replace(tzinfo=timezone.utc)
    if join_date is None:
        join_date = datetime.now(timezone.utc)

    days_on_server = (datetime.now(timezone.utc) - join_date).days

    channel = bot.get_channel(1364667632451584100)
    if channel:
        embed = discord.Embed(
            title=f"{member.name} vient de quitter le serveur Discord !",
            description=(
                f"Nous te souhaitons Bonne Route ! 👋\n"
                f"Il avait rejoint le serveur il y a {days_on_server} jours !"
            ),
            color=discord.Color.red()
        )
        await channel.send(embed=embed)

# Lancer le bot
bot.run("MTM2ODIwNTAxODcyOTI4MzU4NA.Ggz4qX.KfWEBZr3UzOT0ajOUiPo4bENbQ_4tq3ogblU90")
