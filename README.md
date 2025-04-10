# discordModBot
* Add words to a ban list with '!words add', then if a member's message contains those words, the message is automatically deleted and given a strike.
  * Each strike, until the last will come with a timeout, though the punishments for strikes and maximum strikes are hopefully editable
  * If a member is given N strikes, where N is defaulted to 3, but setable with '!words set strikes', they will be banned (editing this should hopefully work) from the server.
  * The banned words list is also viewable with '!words list' and editable (coming soon)
