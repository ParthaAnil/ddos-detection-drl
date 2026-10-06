from mininet.topo import Topo

class DDoSTopo(Topo):
    def build(self):
        server = self.addHost('h1')
        attacker = self.addHost('h2')

        switch = self.addSwitch('s1')

        self.addLink(server, switch)
        self.addLink(attacker, switch)

topos = {'ddos': (lambda: DDoSTopo())}
