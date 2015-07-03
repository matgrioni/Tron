###########################################################
# Author: Matias Grioni
# Created: 7/3/15
#
# The server module that will be used to transfer info
# between players in online play. Mostly a skeleton for now
###########################################################
import PodSixNet

class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print data

class GameServer(PodSixNet.Server.Server):
    channelClass = ClientChannel

    def Connected(self, channel, addr):
        print("New connection > {}".format(channel))
