# Behaviours/EstimateProfit.py
import jsonpickle
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

from Behaviours.Event import EventBH

class EstimateProfitBH(PeriodicBehaviour):
    async def run(self):

        if len(self.agent.attDict) == 0 and len(self.agent.restDict) == 0:
            print("manager >> Profit check: no agents registered yet.")
            return

        replies_expected = len(self.agent.attDict) + len(self.agent.restDict)

        # pedir às atrações
        for att_jid in self.agent.attDict.keys():
            msg = Message(to=str(att_jid))
            msg.set_metadata("performative", "REQUEST")
            msg.set_metadata("thread", f"RP-Manager")
            await self.send(msg)

        # pedir aos restaurantes
        for rest_jid in self.agent.restDict.keys():
            msg = Message(to=str(rest_jid))
            msg.set_metadata("performative", "REQUEST")
            msg.set_metadata("thread", f"RP-Manager")
            await self.send(msg)

        received = 0

        # receber respostas
        while received < replies_expected:
            reply = await self.receive(timeout=1)
            if reply is None:
                break

            perf = reply.get_metadata("performative")
            ont = reply.get_metadata("ontology")
            if not perf == "INFORM":
                continue

            try:
                stats = jsonpickle.decode(reply.body)

                # aceitar dict OU objeto
                if isinstance(stats, dict):
                    profit = float(stats.get("profit", 0.0))
                else:
                    profit = float(stats.getProfit() if hasattr(stats, "getProfit") else stats.profit)

                sender = str(reply.sender)

                # atualizar profit para atrações
                if sender in self.agent.attDict:
                    # attDict[sender] = [available, subscription]
                    sub = self.agent.attDict[sender][1]
                    num = sub.getNum()
                    zone = sub.getZone()

                    # 3 atrações por zona → idx 0..2
                    idx = (num - 1) % 3
                    self.agent.profit["attractions"][zone][idx] = profit

                # atualizar profit para restaurantes
                elif sender in self.agent.restDict:
                    # restDict[sender] = (veganFriendly, subscription)
                    sub = self.agent.restDict[sender][1]
                    num = sub.getNum()

                    idx = num - 1  # 3 restaurantes → 0..2
                    if 0 <= idx < len(self.agent.profit["restaurants"]):
                        self.agent.profit["restaurants"][idx] = profit

                received += 1

            except Exception as e:
                print(f"{self.agent.agentName} >> Error decoding PARK_STATS:", e)

        # calcular totais
        total_rest = sum(self.agent.profit["restaurants"])
        zone_totals = {z: sum(self.agent.profit["attractions"][z]) for z in self.agent.profit["attractions"]}
        zone_totals = dict(sorted(zone_totals.items(), key=lambda item: item[1], reverse=True))
        total_attr = sum(zone_totals.values())
        total_park = total_rest + total_attr

        print(
            f"manager >> Park Profit:\n\n"
            f"======== Profit ========\n"  
            f"- profit: {total_park:.2f}€\n"
            f"----------------------------\n"
            f"- events: \n"
            f"- restaurants: {total_rest:.2f}€ \n"
            f"- attractions: {total_attr:.2f}€ \n"
            f"======== Stats ========\n"
            + "".join(f"- Z{zone}: {profit:.2f}€\n" for zone, profit in zone_totals.items()) +
            # f"replies {received}/{replies_expected}\n"
            f"=======================\n"
        )

        # TODO: Implement Event Trigger
        # last = zone_totals.popitem()
        # print(last)
        # eventPosition = self.agent.eventLocations[last[0] - 1]
        # print(eventPosition)
        # eBH = EventBH(self.agent.eventPosition)
        # self.agent.add_behaviour(eBH)