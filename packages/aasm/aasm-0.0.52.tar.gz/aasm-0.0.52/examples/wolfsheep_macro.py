import copy
import datetime
import random
import httpx
import numpy
import orjson
import spade
import sys


class grass(spade.agent.Agent):
    def __init__(self, jid, password, backup_url = None, backup_period = 60, backup_delay = 0, logger = None, **kwargs):
        super().__init__(jid, password, verify_security=False)
        if logger: logger.debug(f'[{jid}] Received parameters: jid: {jid}, password: {password}, backup_url: {backup_url}, backup_period: {backup_period}, backup_delay: {backup_delay}, kwargs: {kwargs}')
        self.logger = logger
        self.backup_url = backup_url
        self.backup_period = backup_period
        self.backup_delay = backup_delay
        self.connections = kwargs.get("connections", [])
        self.msgRCount = self.limit_number(kwargs.get("msgRCount", 0))
        self.msgSCount = self.limit_number(kwargs.get("msgSCount", 0))
        self.dead_sheep = kwargs.get("dead_sheep", [])
        self.alive_sheep = kwargs.get("alive_sheep", [])
        self.dead_wolf = kwargs.get("dead_wolf", [])
        self.alive_wolf = kwargs.get("alive_wolf", [])
        self.spawn_candidate = kwargs.get("spawn_candidate", [])
        self.field = kwargs.get("field", [])
        if self.logger: self.logger.debug(f'[{self.jid}] Class dict after initialization: {self.__dict__}')
    
    @property
    def connCount(self):
        return self.limit_number(len(self.connections))
    
    def limit_number(self, value):
        return float(max(-2147483648, min(value, 2147483647)))
    
    def get_json_from_spade_message(self, msg):
        return orjson.loads(msg.body)
    
    def get_spade_message(self, receiver_jid, body):
        msg = spade.message.Message(to=receiver_jid)
        body["sender"] = str(self.jid)
        msg.metadata["type"] = body["type"]
        msg.metadata["performative"] = body["performative"]
        msg.body = str(orjson.dumps(body), encoding="utf-8")
        return msg
    
    def setup(self):
        if self.backup_url:
            BackupBehaviour_template = spade.template.Template()
            BackupBehaviour_template.set_metadata("reserved", "no_message_match")
            self.add_behaviour(self.BackupBehaviour(start_at=datetime.datetime.now() + datetime.timedelta(seconds=self.backup_delay), period=self.backup_period), BackupBehaviour_template)
        setup_template = spade.template.Template()
        setup_template.set_metadata("reserved", "no_message_match")
        self.add_behaviour(self.setup(), setup_template)
        regrow_grass_template = spade.template.Template()
        regrow_grass_template.set_metadata("reserved", "no_message_match")
        self.add_behaviour(self.regrow_grass(period=10), regrow_grass_template)
        recv_spawn_template = spade.template.Template()
        recv_spawn_template.set_metadata("type", "spawn")
        recv_spawn_template.set_metadata("performative", "Inform")
        self.add_behaviour(self.recv_spawn(), recv_spawn_template)
        recv_broadcast_template = spade.template.Template()
        recv_broadcast_template.set_metadata("type", "broadcast")
        recv_broadcast_template.set_metadata("performative", "Inform")
        self.add_behaviour(self.recv_broadcast(), recv_broadcast_template)
        eat_grass_template = spade.template.Template()
        eat_grass_template.set_metadata("type", "eat")
        eat_grass_template.set_metadata("performative", "Request")
        self.add_behaviour(self.eat_grass(), eat_grass_template)
        recv_kill_template = spade.template.Template()
        recv_kill_template.set_metadata("type", "kill")
        recv_kill_template.set_metadata("performative", "Inform")
        self.add_behaviour(self.recv_kill(), recv_kill_template)
        if self.logger: self.logger.debug(f'[{self.jid}] Class dict after setup: {self.__dict__}')
    
    class BackupBehaviour(spade.behaviour.PeriodicBehaviour):
        def __init__(self, start_at, period):
            super().__init__(start_at=start_at, period=period)
            self.http_client = httpx.AsyncClient(timeout=period)
        
        async def run(self):
            data = {
                "__timestamp__": int(datetime.datetime.timestamp(datetime.datetime.utcnow())),
                "jid": str(self.agent.jid),
                "type": "grass",
                "floats": {
                    "msgRCount": self.agent.msgRCount,
                    "msgSCount": self.agent.msgSCount,
                    "connCount": self.agent.connCount,
                },
                "enums": {
                },
                "connections": {
                    "connections": self.agent.connections,
                    "dead_sheep": self.agent.dead_sheep,
                    "alive_sheep": self.agent.alive_sheep,
                    "dead_wolf": self.agent.dead_wolf,
                    "alive_wolf": self.agent.alive_wolf,
                    "spawn_candidate": self.agent.spawn_candidate,
                },
                "messages": {
                },
                "float_lists": {
                    "field": self.agent.field,
                },
            }
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Sending backup data: {data}')
            try:
                await self.http_client.post(self.agent.backup_url, headers={"Content-Type": "application/json"}, data=orjson.dumps(data))
            except Exception as e:
                if self.agent.logger: self.agent.logger.error(f'[{self.agent.jid}] Backup error type: {e.__class__}, additional info: {e}')
    
    class setup(spade.behaviour.OneShotBehaviour):
        def setup_field(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action setup_field')
            
            # float declaration
            it = self.agent.limit_number(0)
            
            # float declaration
            amt = self.agent.limit_number(0)
            
            # while less than
            while self.agent.limit_number(it) < self.agent.limit_number(10000):
                
                # uniform distribution
                amt = self.agent.limit_number(random.uniform(self.agent.limit_number(0), self.agent.limit_number(10)))
                
                # add element
                self.agent.field.append(amt)
                
                # add
                it = self.agent.limit_number(it + self.agent.limit_number(1))
        
        async def broadcast(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action broadcast')
            send = { "type": "broadcast", "performative": "Inform", "typ": 0.0, "state": 0.0, }
            
            # set
            send["typ"] = self.agent.limit_number(0)
            
            # send
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Send message {send} to {self.agent.connections}')
            for receiver in self.agent.connections:
                await self.send(self.agent.get_spade_message(receiver, send))
                self.agent.msgSCount = self.agent.limit_number(self.agent.msgSCount + 1)
        
        async def run(self):
            self.setup_field()
            await self.broadcast()
    
    class regrow_grass(spade.behaviour.PeriodicBehaviour):
        def regrow(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action regrow')
            
            # float declaration
            it = self.agent.limit_number(0)
            
            # float declaration
            amt = self.agent.limit_number(0)
            
            # while less than
            while self.agent.limit_number(it) < self.agent.limit_number(10000):
                
                # list read
                if int(self.agent.limit_number(round(self.agent.limit_number(it)))) < 0 or int(self.agent.limit_number(round(self.agent.limit_number(it)))) >= int(self.agent.limit_number(len(self.agent.field))):
                    if self.agent.logger: self.agent.logger.warning(f'[{self.agent.jid}] Incorrect index (rounded, either negative or bigger than the list size): {int(self.agent.limit_number(round(self.agent.limit_number(it))))}')
                    return
                amt = self.agent.limit_number(self.agent.field[int(self.agent.limit_number(round(self.agent.limit_number(it))))])
                
                # add
                amt = self.agent.limit_number(amt + self.agent.limit_number(0.1))
                
                # if greater than
                if self.agent.limit_number(amt) > self.agent.limit_number(10):
                    
                    # set
                    amt = self.agent.limit_number(10)
                
                # list write
                if int(self.agent.limit_number(round(self.agent.limit_number(it)))) < 0 or int(self.agent.limit_number(round(self.agent.limit_number(it)))) >= int(self.agent.limit_number(len(self.agent.field))):
                    if self.agent.logger: self.agent.logger.warning(f'[{self.agent.jid}] Incorrect index (rounded, either negative or bigger than the list size): {int(self.agent.limit_number(round(self.agent.limit_number(it))))}')
                    return
                self.agent.field[int(self.agent.limit_number(round(self.agent.limit_number(it))))] = self.agent.limit_number(amt)
                
                # add
                it = self.agent.limit_number(it + self.agent.limit_number(1))
        
        async def run(self):
            self.regrow()
    
    class recv_spawn(spade.behaviour.CyclicBehaviour):
        def choose_spawn(self, rcv):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action choose_spawn')
            
            # clear
            self.agent.spawn_candidate.clear()
            
            # if equal
            if self.agent.limit_number(rcv["typ"]) == self.agent.limit_number(1):
                
                # subset
                if int(self.agent.limit_number(round(self.agent.limit_number(1)))) <= 0:
                    if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Non-positive subset size (rounded): {int(self.agent.limit_number(round(self.agent.limit_number(1))))}')
                    return
                self.agent.spawn_candidate = [copy.deepcopy(elem) for elem in random.sample(self.agent.dead_sheep, min(int(self.agent.limit_number(round(self.agent.limit_number(1)))), int(self.agent.limit_number(len(self.agent.dead_sheep)))))]
                
                # remove element
                if "spawn_candidate" in self.agent.dead_sheep: self.agent.dead_sheep.remove("spawn_candidate")
                
                # add element
                self.agent.alive_sheep.append("spawn_candidate")
            
            # if equal
            if self.agent.limit_number(rcv["typ"]) == self.agent.limit_number(2):
                
                # subset
                if int(self.agent.limit_number(round(self.agent.limit_number(1)))) <= 0:
                    if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Non-positive subset size (rounded): {int(self.agent.limit_number(round(self.agent.limit_number(1))))}')
                    return
                self.agent.spawn_candidate = [copy.deepcopy(elem) for elem in random.sample(self.agent.dead_wolf, min(int(self.agent.limit_number(round(self.agent.limit_number(1)))), int(self.agent.limit_number(len(self.agent.dead_wolf)))))]
                
                # remove element
                if "spawn_candidate" in self.agent.dead_wolf: self.agent.dead_wolf.remove("spawn_candidate")
                
                # add element
                self.agent.alive_wolf.append("spawn_candidate")
        
        async def spawn(self, rcv):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action spawn')
            send = { "type": "spawn", "performative": "Inform", "typ": 0.0, }
            
            # send
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Send message {send} to {self.agent.spawn_candidate}')
            for receiver in self.agent.spawn_candidate:
                await self.send(self.agent.get_spade_message(receiver, send))
                self.agent.msgSCount = self.agent.limit_number(self.agent.msgSCount + 1)
        
        async def run(self):
            rcv = await self.receive(timeout=100000)
            if rcv:
                rcv = self.agent.get_json_from_spade_message(rcv)
                self.agent.msgRCount = self.agent.limit_number(self.agent.msgRCount + 1)
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Received message: {rcv}')
                self.choose_spawn(rcv)
                await self.spawn(rcv)
    
    class recv_broadcast(spade.behaviour.CyclicBehaviour):
        def add_agent(self, rcv):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action add_agent')
            
            # if equal
            if self.agent.limit_number(rcv["typ"]) == self.agent.limit_number(1):
                
                # if equal
                if self.agent.limit_number(rcv["state"]) == self.agent.limit_number(0):
                    
                    # remove element
                    if "RCV.jid" in self.agent.alive_sheep: self.agent.alive_sheep.remove("RCV.jid")
                    
                    # add element
                    self.agent.dead_sheep.append("RCV.jid")
                
                # if equal
                if self.agent.limit_number(rcv["state"]) == self.agent.limit_number(1):
                    
                    # remove element
                    if "RCV.jid" in self.agent.dead_sheep: self.agent.dead_sheep.remove("RCV.jid")
                    
                    # add element
                    self.agent.alive_sheep.append("RCV.jid")
            
            # if equal
            if self.agent.limit_number(rcv["typ"]) == self.agent.limit_number(2):
                
                # if equal
                if self.agent.limit_number(rcv["state"]) == self.agent.limit_number(0):
                    
                    # remove element
                    if "RCV.jid" in self.agent.alive_wolf: self.agent.alive_wolf.remove("RCV.jid")
                    
                    # add element
                    self.agent.dead_wolf.append("RCV.jid")
                
                # if equal
                if self.agent.limit_number(rcv["state"]) == self.agent.limit_number(1):
                    
                    # remove element
                    if "RCV.jid" in self.agent.dead_wolf: self.agent.dead_wolf.remove("RCV.jid")
                    
                    # add element
                    self.agent.alive_wolf.append("RCV.jid")
        
        async def run(self):
            rcv = await self.receive(timeout=100000)
            if rcv:
                rcv = self.agent.get_json_from_spade_message(rcv)
                self.agent.msgRCount = self.agent.limit_number(self.agent.msgRCount + 1)
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Received message: {rcv}')
                self.add_agent(rcv)
    
    class eat_grass(spade.behaviour.CyclicBehaviour):
        async def parse_eat(self, rcv):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action parse_eat')
            send = { "type": "eat", "performative": "Inform", "energy": 0.0, }
            
            # float declaration
            index = self.agent.limit_number(rcv["x"])
            
            # multiply
            index = self.agent.limit_number(index * self.agent.limit_number(99))
            
            # add
            index = self.agent.limit_number(index + self.agent.limit_number(rcv["y"]))
            
            # float declaration
            grass_val = self.agent.limit_number(0)
            
            # list read
            if int(self.agent.limit_number(round(self.agent.limit_number(index)))) < 0 or int(self.agent.limit_number(round(self.agent.limit_number(index)))) >= int(self.agent.limit_number(len(self.agent.field))):
                if self.agent.logger: self.agent.logger.warning(f'[{self.agent.jid}] Incorrect index (rounded, either negative or bigger than the list size): {int(self.agent.limit_number(round(self.agent.limit_number(index))))}')
                return
            grass_val = self.agent.limit_number(self.agent.field[int(self.agent.limit_number(round(self.agent.limit_number(index))))])
            
            # float declaration
            send_flag = self.agent.limit_number(0)
            
            # if greater than
            if self.agent.limit_number(grass_val) > self.agent.limit_number(1):
                
                # set
                send_flag = self.agent.limit_number(1)
                
                # set
                send["energy"] = self.agent.limit_number(1)
                
                # subtract
                grass_val = self.agent.limit_number(grass_val - self.agent.limit_number(1))
                
                # list write
                if int(self.agent.limit_number(round(self.agent.limit_number(index)))) < 0 or int(self.agent.limit_number(round(self.agent.limit_number(index)))) >= int(self.agent.limit_number(len(self.agent.field))):
                    if self.agent.logger: self.agent.logger.warning(f'[{self.agent.jid}] Incorrect index (rounded, either negative or bigger than the list size): {int(self.agent.limit_number(round(self.agent.limit_number(index))))}')
                    return
                self.agent.field[int(self.agent.limit_number(round(self.agent.limit_number(index))))] = self.agent.limit_number(grass_val)
            
            # if equal
            if self.agent.limit_number(send_flag) == self.agent.limit_number(0):
                
                # set
                send["energy"] = self.agent.limit_number(0)
            
            # send
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Send message {send} to {"RCV.jid"}')
            await self.send(self.agent.get_spade_message("RCV.jid", send))
            self.agent.msgSCount = self.agent.limit_number(self.agent.msgSCount + 1)
        
        async def run(self):
            rcv = await self.receive(timeout=100000)
            if rcv:
                rcv = self.agent.get_json_from_spade_message(rcv)
                self.agent.msgRCount = self.agent.limit_number(self.agent.msgRCount + 1)
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Received message: {rcv}')
                await self.parse_eat(rcv)
    
    class recv_kill(spade.behaviour.CyclicBehaviour):
        def kill_creature(self, rcv):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action kill_creature')
            
            # if in list
            if "RCV.jid" in self.agent.alive_sheep:
                
                # remove element
                if "RCV.jid" in self.agent.alive_sheep: self.agent.alive_sheep.remove("RCV.jid")
                
                # add element
                self.agent.dead_sheep.append("RCV.jid")
            
            # if in list
            if "RCV.jid" in self.agent.alive_wolf:
                
                # remove element
                if "RCV.jid" in self.agent.alive_wolf: self.agent.alive_wolf.remove("RCV.jid")
                
                # add element
                self.agent.dead_wolf.append("RCV.jid")
        
        async def run(self):
            rcv = await self.receive(timeout=100000)
            if rcv:
                rcv = self.agent.get_json_from_spade_message(rcv)
                self.agent.msgRCount = self.agent.limit_number(self.agent.msgRCount + 1)
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Received message: {rcv}')
                self.kill_creature(rcv)
    


class sheep(spade.agent.Agent):
    def __init__(self, jid, password, backup_url = None, backup_period = 60, backup_delay = 0, logger = None, **kwargs):
        super().__init__(jid, password, verify_security=False)
        if logger: logger.debug(f'[{jid}] Received parameters: jid: {jid}, password: {password}, backup_url: {backup_url}, backup_period: {backup_period}, backup_delay: {backup_delay}, kwargs: {kwargs}')
        self.logger = logger
        self.backup_url = backup_url
        self.backup_period = backup_period
        self.backup_delay = backup_delay
        self.connections = kwargs.get("connections", [])
        self.msgRCount = self.limit_number(kwargs.get("msgRCount", 0))
        self.msgSCount = self.limit_number(kwargs.get("msgSCount", 0))
        self.energy = self.limit_number(kwargs.get("energy", 100))
        self.x = self.limit_number(kwargs.get("x", random.uniform(self.limit_number(0), self.limit_number(99))))
        self.y = self.limit_number(kwargs.get("y", random.uniform(self.limit_number(0), self.limit_number(99))))
        self.heading = self.limit_number(kwargs.get("heading", random.uniform(self.limit_number(0), self.limit_number(180))))
        self.invert = kwargs.get("invert", random.choices(["YES", "NO"], [0, 100])[0])
        self.dead = kwargs.get("dead", random.choices(["YES", "NO"], [0, 100])[0])
        self.field = kwargs.get("field", [])
        if self.logger: self.logger.debug(f'[{self.jid}] Class dict after initialization: {self.__dict__}')
    
    @property
    def connCount(self):
        return self.limit_number(len(self.connections))
    
    def limit_number(self, value):
        return float(max(-2147483648, min(value, 2147483647)))
    
    def get_json_from_spade_message(self, msg):
        return orjson.loads(msg.body)
    
    def get_spade_message(self, receiver_jid, body):
        msg = spade.message.Message(to=receiver_jid)
        body["sender"] = str(self.jid)
        msg.metadata["type"] = body["type"]
        msg.metadata["performative"] = body["performative"]
        msg.body = str(orjson.dumps(body), encoding="utf-8")
        return msg
    
    def setup(self):
        if self.backup_url:
            BackupBehaviour_template = spade.template.Template()
            BackupBehaviour_template.set_metadata("reserved", "no_message_match")
            self.add_behaviour(self.BackupBehaviour(start_at=datetime.datetime.now() + datetime.timedelta(seconds=self.backup_delay), period=self.backup_period), BackupBehaviour_template)
        setup_template = spade.template.Template()
        setup_template.set_metadata("reserved", "no_message_match")
        self.add_behaviour(self.setup(), setup_template)
        move_around_template = spade.template.Template()
        move_around_template.set_metadata("reserved", "no_message_match")
        self.add_behaviour(self.move_around(period=10), move_around_template)
        reproduce_template = spade.template.Template()
        reproduce_template.set_metadata("reserved", "no_message_match")
        self.add_behaviour(self.reproduce(period=20), reproduce_template)
        recv_spawn_template = spade.template.Template()
        recv_spawn_template.set_metadata("type", "spawn")
        recv_spawn_template.set_metadata("performative", "Inform")
        self.add_behaviour(self.recv_spawn(), recv_spawn_template)
        recv_kill_template = spade.template.Template()
        recv_kill_template.set_metadata("type", "kill")
        recv_kill_template.set_metadata("performative", "Inform")
        self.add_behaviour(self.recv_kill(), recv_kill_template)
        grass_eat_template = spade.template.Template()
        grass_eat_template.set_metadata("type", "eat")
        grass_eat_template.set_metadata("performative", "Inform")
        self.add_behaviour(self.grass_eat(), grass_eat_template)
        recv_broadcast_template = spade.template.Template()
        recv_broadcast_template.set_metadata("type", "broadcast")
        recv_broadcast_template.set_metadata("performative", "Inform")
        self.add_behaviour(self.recv_broadcast(), recv_broadcast_template)
        get_eaten_request_template = spade.template.Template()
        get_eaten_request_template.set_metadata("type", "eat")
        get_eaten_request_template.set_metadata("performative", "Request")
        self.add_behaviour(self.get_eaten_request(), get_eaten_request_template)
        if self.logger: self.logger.debug(f'[{self.jid}] Class dict after setup: {self.__dict__}')
    
    class BackupBehaviour(spade.behaviour.PeriodicBehaviour):
        def __init__(self, start_at, period):
            super().__init__(start_at=start_at, period=period)
            self.http_client = httpx.AsyncClient(timeout=period)
        
        async def run(self):
            data = {
                "__timestamp__": int(datetime.datetime.timestamp(datetime.datetime.utcnow())),
                "jid": str(self.agent.jid),
                "type": "sheep",
                "floats": {
                    "msgRCount": self.agent.msgRCount,
                    "msgSCount": self.agent.msgSCount,
                    "connCount": self.agent.connCount,
                    "energy": self.agent.energy,
                    "x": self.agent.x,
                    "y": self.agent.y,
                    "heading": self.agent.heading,
                },
                "enums": {
                    "invert": self.agent.invert,
                    "dead": self.agent.dead,
                },
                "connections": {
                    "connections": self.agent.connections,
                    "field": self.agent.field,
                },
                "messages": {
                },
                "float_lists": {
                },
            }
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Sending backup data: {data}')
            try:
                await self.http_client.post(self.agent.backup_url, headers={"Content-Type": "application/json"}, data=orjson.dumps(data))
            except Exception as e:
                if self.agent.logger: self.agent.logger.error(f'[{self.agent.jid}] Backup error type: {e.__class__}, additional info: {e}')
    
    class setup(spade.behaviour.OneShotBehaviour):
        async def broadcast(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action broadcast')
            send = { "type": "broadcast", "performative": "Inform", "typ": 0.0, "state": 0.0, }
            
            # set
            send["typ"] = self.agent.limit_number(1)
            
            # if equal
            if self.agent.dead == "YES":
                
                # set
                send["state"] = self.agent.limit_number(0)
            
            # if equal
            if self.agent.dead == "NO":
                
                # set
                send["state"] = self.agent.limit_number(1)
            
            # send
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Send message {send} to {self.agent.connections}')
            for receiver in self.agent.connections:
                await self.send(self.agent.get_spade_message(receiver, send))
                self.agent.msgSCount = self.agent.limit_number(self.agent.msgSCount + 1)
        
        async def run(self):
            await self.broadcast()
    
    class move_around(spade.behaviour.PeriodicBehaviour):
        def wiggle(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action wiggle')
            
            # if equal
            if self.agent.dead == "NO":
                
                # float declaration
                wiglR = self.agent.limit_number(0)
                
                # float declaration
                wiglL = self.agent.limit_number(0)
                
                # uniform distribution
                wiglR = self.agent.limit_number(random.uniform(self.agent.limit_number(0), self.agent.limit_number(90)))
                
                # uniform distribution
                wiglL = self.agent.limit_number(random.uniform(self.agent.limit_number(0), self.agent.limit_number(90)))
                
                # float declaration
                change_flag = self.agent.limit_number(0)
                
                # if equal
                if self.agent.invert == "YES":
                    
                    # set
                    change_flag = self.agent.limit_number(1)
                    
                    # add
                    self.agent.heading = self.agent.limit_number(self.agent.heading + self.agent.limit_number(wiglL))
                    
                    # subtract
                    self.agent.heading = self.agent.limit_number(self.agent.heading - self.agent.limit_number(wiglR))
                    
                    # if less than
                    if self.agent.limit_number(self.agent.heading) < self.agent.limit_number(0):
                        
                        # set
                        self.agent.invert = "NO"
                        
                        # add
                        self.agent.heading = self.agent.limit_number(self.agent.heading + self.agent.limit_number(180))
                    
                    # if greater than
                    if self.agent.limit_number(self.agent.heading) > self.agent.limit_number(180):
                        
                        # set
                        self.agent.invert = "NO"
                        
                        # subtract
                        self.agent.heading = self.agent.limit_number(self.agent.heading - self.agent.limit_number(180))
                
                # if equal
                if self.agent.invert == "NO":
                    
                    # if equal
                    if self.agent.limit_number(change_flag) == self.agent.limit_number(0):
                        
                        # add
                        self.agent.heading = self.agent.limit_number(self.agent.heading + self.agent.limit_number(wiglL))
                        
                        # subtract
                        self.agent.heading = self.agent.limit_number(self.agent.heading - self.agent.limit_number(wiglR))
                        
                        # if less than
                        if self.agent.limit_number(self.agent.heading) < self.agent.limit_number(0):
                            
                            # set
                            self.agent.invert = "YES"
                            
                            # add
                            self.agent.heading = self.agent.limit_number(self.agent.heading + self.agent.limit_number(180))
                        
                        # if greater than
                        if self.agent.limit_number(self.agent.heading) > self.agent.limit_number(180):
                            
                            # set
                            self.agent.invert = "YES"
                            
                            # subtract
                            self.agent.heading = self.agent.limit_number(self.agent.heading - self.agent.limit_number(180))
        
        def move(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action move')
            
            # if equal
            if self.agent.dead == "NO":
                
                # float declaration
                a = self.agent.limit_number(0)
                
                # float declaration
                b = self.agent.limit_number(0)
                
                # sin
                a = self.agent.limit_number(numpy.sin(numpy.deg2rad(self.agent.limit_number(self.agent.heading))))
                
                # sin
                b = self.agent.limit_number(numpy.sin(numpy.deg2rad(self.agent.limit_number(self.agent.heading))))
                
                # float declaration
                newx = self.agent.limit_number(self.agent.x)
                
                # float declaration
                newy = self.agent.limit_number(self.agent.y)
                
                # if greater than
                if self.agent.limit_number(self.agent.heading) > self.agent.limit_number(90):
                    
                    # subtract
                    newx = self.agent.limit_number(newx - self.agent.limit_number(a))
                
                # if greater than or equal
                if self.agent.limit_number(self.agent.heading) <= self.agent.limit_number(90):
                    
                    # add
                    newx = self.agent.limit_number(newx + self.agent.limit_number(a))
                
                # if equal
                if self.agent.invert == "YES":
                    
                    # subtract
                    newy = self.agent.limit_number(newy - self.agent.limit_number(b))
                
                # if equal
                if self.agent.invert == "NO":
                    
                    # add
                    newy = self.agent.limit_number(newy + self.agent.limit_number(b))
                
                # float declaration
                bump = self.agent.limit_number(0)
                
                # if less than
                if self.agent.limit_number(newx) < self.agent.limit_number(0):
                    
                    # set
                    bump = self.agent.limit_number(1)
                
                # if less than
                if self.agent.limit_number(newy) < self.agent.limit_number(0):
                    
                    # set
                    bump = self.agent.limit_number(1)
                
                # if greater than
                if self.agent.limit_number(newx) > self.agent.limit_number(99):
                    
                    # set
                    bump = self.agent.limit_number(1)
                
                # if greater than
                if self.agent.limit_number(newy) > self.agent.limit_number(99):
                    
                    # set
                    bump = self.agent.limit_number(1)
                
                # if equal
                if self.agent.limit_number(bump) == self.agent.limit_number(0):
                    
                    # set
                    self.agent.x = self.agent.limit_number(newx)
                    
                    # set
                    self.agent.y = self.agent.limit_number(newy)
                    
                    # subtract
                    self.agent.energy = self.agent.limit_number(self.agent.energy - self.agent.limit_number(1))
                
                # if equal
                if self.agent.limit_number(bump) == self.agent.limit_number(1):
                    
                    # add
                    self.agent.heading = self.agent.limit_number(self.agent.heading + self.agent.limit_number(90))
                    
                    # if greater than
                    if self.agent.limit_number(self.agent.heading) > self.agent.limit_number(180):
                        
                        # subtract
                        self.agent.heading = self.agent.limit_number(self.agent.heading - self.agent.limit_number(180))
                        
                        # float declaration
                        flag = self.agent.limit_number(0)
                        
                        # if equal
                        if self.agent.invert == "YES":
                            
                            # set
                            flag = self.agent.limit_number(1)
                            
                            # set
                            self.agent.invert = "NO"
                        
                        # if equal
                        if self.agent.invert == "NO":
                            
                            # if equal
                            if self.agent.limit_number(flag) == self.agent.limit_number(0):
                                
                                # set
                                self.agent.invert = "YES"
        
        def check_if_dead(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action check_if_dead')
            
            # if greater than or equal
            if self.agent.limit_number(self.agent.energy) <= self.agent.limit_number(0):
                
                # set
                self.agent.dead = "YES"
        
        async def eat(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action eat')
            send = { "type": "eat", "performative": "Request", "x": 0.0, "y": 0.0, }
            
            # if equal
            if self.agent.dead == "NO":
                
                # set
                send["x"] = self.agent.limit_number(self.agent.x)
                
                # set
                send["y"] = self.agent.limit_number(self.agent.y)
                
                # send
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Send message {send} to {self.agent.field}')
                for receiver in self.agent.field:
                    await self.send(self.agent.get_spade_message(receiver, send))
                    self.agent.msgSCount = self.agent.limit_number(self.agent.msgSCount + 1)
        
        async def run(self):
            self.wiggle()
            self.move()
            self.check_if_dead()
            await self.eat()
    
    class reproduce(spade.behaviour.PeriodicBehaviour):
        async def hatch(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action hatch')
            send = { "type": "spawn", "performative": "Inform", "typ": 0.0, }
            
            # if equal
            if self.agent.dead == "NO":
                
                # if equal
                if self.agent.limit_number(self.agent.energy) == self.agent.limit_number(100):
                    
                    # set
                    send["typ"] = self.agent.limit_number(1)
                    
                    # send
                    if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Send message {send} to {self.agent.field}')
                    for receiver in self.agent.field:
                        await self.send(self.agent.get_spade_message(receiver, send))
                        self.agent.msgSCount = self.agent.limit_number(self.agent.msgSCount + 1)
        
        async def run(self):
            await self.hatch()
    
    class recv_spawn(spade.behaviour.CyclicBehaviour):
        def spawn(self, rcv):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action spawn')
            
            # set
            self.agent.dead = "NO"
        
        async def run(self):
            rcv = await self.receive(timeout=100000)
            if rcv:
                rcv = self.agent.get_json_from_spade_message(rcv)
                self.agent.msgRCount = self.agent.limit_number(self.agent.msgRCount + 1)
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Received message: {rcv}')
                self.spawn(rcv)
    
    class recv_kill(spade.behaviour.CyclicBehaviour):
        async def die(self, rcv):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action die')
            send = { "type": "kill", "performative": "Inform", }
            
            # set
            self.agent.dead = "YES"
            
            # send
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Send message {send} to {self.agent.field}')
            for receiver in self.agent.field:
                await self.send(self.agent.get_spade_message(receiver, send))
                self.agent.msgSCount = self.agent.limit_number(self.agent.msgSCount + 1)
        
        async def run(self):
            rcv = await self.receive(timeout=100000)
            if rcv:
                rcv = self.agent.get_json_from_spade_message(rcv)
                self.agent.msgRCount = self.agent.limit_number(self.agent.msgRCount + 1)
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Received message: {rcv}')
                await self.die(rcv)
    
    class grass_eat(spade.behaviour.CyclicBehaviour):
        def change_energy(self, rcv):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action change_energy')
            
            # add
            self.agent.energy = self.agent.limit_number(self.agent.energy + self.agent.limit_number(rcv["energy"]))
        
        async def run(self):
            rcv = await self.receive(timeout=100000)
            if rcv:
                rcv = self.agent.get_json_from_spade_message(rcv)
                self.agent.msgRCount = self.agent.limit_number(self.agent.msgRCount + 1)
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Received message: {rcv}')
                self.change_energy(rcv)
    
    class recv_broadcast(spade.behaviour.CyclicBehaviour):
        def xd(self, rcv):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action xd')
            
            # if equal
            if self.agent.limit_number(rcv["typ"]) == self.agent.limit_number(0):
                
                # add element
                self.agent.field.append("RCV.jid")
        
        async def run(self):
            rcv = await self.receive(timeout=100000)
            if rcv:
                rcv = self.agent.get_json_from_spade_message(rcv)
                self.agent.msgRCount = self.agent.limit_number(self.agent.msgRCount + 1)
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Received message: {rcv}')
                self.xd(rcv)
    
    class get_eaten_request(spade.behaviour.CyclicBehaviour):
        async def kappa(self, rcv):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action kappa')
            send = { "type": "eat", "performative": "Inform", "energy": 0.0, }
            
            # if equal
            if self.agent.dead == "NO":
                
                # float declaration
                lowx = self.agent.limit_number(self.agent.x)
                
                # float declaration
                lowy = self.agent.limit_number(self.agent.y)
                
                # float declaration
                highx = self.agent.limit_number(self.agent.x)
                
                # float declaration
                highy = self.agent.limit_number(self.agent.y)
                
                # subtract
                lowx = self.agent.limit_number(lowx - self.agent.limit_number(1))
                
                # subtract
                lowy = self.agent.limit_number(lowy - self.agent.limit_number(1))
                
                # add
                highx = self.agent.limit_number(highx + self.agent.limit_number(1))
                
                # add
                highy = self.agent.limit_number(highy + self.agent.limit_number(1))
                
                # if less than
                if self.agent.limit_number(highx) < self.agent.limit_number(rcv["x"]):
                    
                    # if less than
                    if self.agent.limit_number(highy) < self.agent.limit_number(rcv["y"]):
                        
                        # if greater than
                        if self.agent.limit_number(lowx) > self.agent.limit_number(rcv["x"]):
                            
                            # if greater than
                            if self.agent.limit_number(lowy) > self.agent.limit_number(rcv["y"]):
                                
                                # set
                                send["energy"] = self.agent.limit_number(1)
                                
                                # send
                                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Send message {send} to {"RCV.jid"}')
                                await self.send(self.agent.get_spade_message("RCV.jid", send))
                                self.agent.msgSCount = self.agent.limit_number(self.agent.msgSCount + 1)
        
        async def run(self):
            rcv = await self.receive(timeout=100000)
            if rcv:
                rcv = self.agent.get_json_from_spade_message(rcv)
                self.agent.msgRCount = self.agent.limit_number(self.agent.msgRCount + 1)
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Received message: {rcv}')
                await self.kappa(rcv)
    


class wolf(spade.agent.Agent):
    def __init__(self, jid, password, backup_url = None, backup_period = 60, backup_delay = 0, logger = None, **kwargs):
        super().__init__(jid, password, verify_security=False)
        if logger: logger.debug(f'[{jid}] Received parameters: jid: {jid}, password: {password}, backup_url: {backup_url}, backup_period: {backup_period}, backup_delay: {backup_delay}, kwargs: {kwargs}')
        self.logger = logger
        self.backup_url = backup_url
        self.backup_period = backup_period
        self.backup_delay = backup_delay
        self.connections = kwargs.get("connections", [])
        self.msgRCount = self.limit_number(kwargs.get("msgRCount", 0))
        self.msgSCount = self.limit_number(kwargs.get("msgSCount", 0))
        self.energy = self.limit_number(kwargs.get("energy", 100))
        self.x = self.limit_number(kwargs.get("x", random.uniform(self.limit_number(0), self.limit_number(99))))
        self.y = self.limit_number(kwargs.get("y", random.uniform(self.limit_number(0), self.limit_number(99))))
        self.heading = self.limit_number(kwargs.get("heading", random.uniform(self.limit_number(0), self.limit_number(180))))
        self.invert = kwargs.get("invert", random.choices(["YES", "NO"], [0, 100])[0])
        self.dead = kwargs.get("dead", random.choices(["YES", "NO"], [0, 100])[0])
        self.is_eating = kwargs.get("is_eating", random.choices(["YES", "NO"], [0, 100])[0])
        self.field = kwargs.get("field", [])
        self.sheep = kwargs.get("sheep", [])
        if self.logger: self.logger.debug(f'[{self.jid}] Class dict after initialization: {self.__dict__}')
    
    @property
    def connCount(self):
        return self.limit_number(len(self.connections))
    
    def limit_number(self, value):
        return float(max(-2147483648, min(value, 2147483647)))
    
    def get_json_from_spade_message(self, msg):
        return orjson.loads(msg.body)
    
    def get_spade_message(self, receiver_jid, body):
        msg = spade.message.Message(to=receiver_jid)
        body["sender"] = str(self.jid)
        msg.metadata["type"] = body["type"]
        msg.metadata["performative"] = body["performative"]
        msg.body = str(orjson.dumps(body), encoding="utf-8")
        return msg
    
    def setup(self):
        if self.backup_url:
            BackupBehaviour_template = spade.template.Template()
            BackupBehaviour_template.set_metadata("reserved", "no_message_match")
            self.add_behaviour(self.BackupBehaviour(start_at=datetime.datetime.now() + datetime.timedelta(seconds=self.backup_delay), period=self.backup_period), BackupBehaviour_template)
        setup_template = spade.template.Template()
        setup_template.set_metadata("reserved", "no_message_match")
        self.add_behaviour(self.setup(), setup_template)
        move_around_template = spade.template.Template()
        move_around_template.set_metadata("reserved", "no_message_match")
        self.add_behaviour(self.move_around(period=10), move_around_template)
        recv_spawn_template = spade.template.Template()
        recv_spawn_template.set_metadata("type", "spawn")
        recv_spawn_template.set_metadata("performative", "Inform")
        self.add_behaviour(self.recv_spawn(), recv_spawn_template)
        rcv_eat_template = spade.template.Template()
        rcv_eat_template.set_metadata("type", "eat")
        rcv_eat_template.set_metadata("performative", "Inform")
        self.add_behaviour(self.rcv_eat(), rcv_eat_template)
        recv_broadcast_template = spade.template.Template()
        recv_broadcast_template.set_metadata("type", "broadcast")
        recv_broadcast_template.set_metadata("performative", "Inform")
        self.add_behaviour(self.recv_broadcast(), recv_broadcast_template)
        if self.logger: self.logger.debug(f'[{self.jid}] Class dict after setup: {self.__dict__}')
    
    class BackupBehaviour(spade.behaviour.PeriodicBehaviour):
        def __init__(self, start_at, period):
            super().__init__(start_at=start_at, period=period)
            self.http_client = httpx.AsyncClient(timeout=period)
        
        async def run(self):
            data = {
                "__timestamp__": int(datetime.datetime.timestamp(datetime.datetime.utcnow())),
                "jid": str(self.agent.jid),
                "type": "wolf",
                "floats": {
                    "msgRCount": self.agent.msgRCount,
                    "msgSCount": self.agent.msgSCount,
                    "connCount": self.agent.connCount,
                    "energy": self.agent.energy,
                    "x": self.agent.x,
                    "y": self.agent.y,
                    "heading": self.agent.heading,
                },
                "enums": {
                    "invert": self.agent.invert,
                    "dead": self.agent.dead,
                    "is_eating": self.agent.is_eating,
                },
                "connections": {
                    "connections": self.agent.connections,
                    "field": self.agent.field,
                    "sheep": self.agent.sheep,
                },
                "messages": {
                },
                "float_lists": {
                },
            }
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Sending backup data: {data}')
            try:
                await self.http_client.post(self.agent.backup_url, headers={"Content-Type": "application/json"}, data=orjson.dumps(data))
            except Exception as e:
                if self.agent.logger: self.agent.logger.error(f'[{self.agent.jid}] Backup error type: {e.__class__}, additional info: {e}')
    
    class setup(spade.behaviour.OneShotBehaviour):
        async def broadcast(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action broadcast')
            send = { "type": "broadcast", "performative": "Inform", "typ": 0.0, "state": 0.0, }
            
            # set
            send["typ"] = self.agent.limit_number(2)
            
            # if equal
            if self.agent.dead == "YES":
                
                # set
                send["state"] = self.agent.limit_number(0)
            
            # if equal
            if self.agent.dead == "NO":
                
                # set
                send["state"] = self.agent.limit_number(1)
            
            # send
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Send message {send} to {self.agent.connections}')
            for receiver in self.agent.connections:
                await self.send(self.agent.get_spade_message(receiver, send))
                self.agent.msgSCount = self.agent.limit_number(self.agent.msgSCount + 1)
        
        async def run(self):
            await self.broadcast()
    
    class move_around(spade.behaviour.PeriodicBehaviour):
        def wiggle(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action wiggle')
            
            # if equal
            if self.agent.dead == "NO":
                
                # float declaration
                wiglR = self.agent.limit_number(0)
                
                # float declaration
                wiglL = self.agent.limit_number(0)
                
                # uniform distribution
                wiglR = self.agent.limit_number(random.uniform(self.agent.limit_number(0), self.agent.limit_number(90)))
                
                # uniform distribution
                wiglL = self.agent.limit_number(random.uniform(self.agent.limit_number(0), self.agent.limit_number(90)))
                
                # float declaration
                change_flag = self.agent.limit_number(0)
                
                # if equal
                if self.agent.invert == "YES":
                    
                    # set
                    change_flag = self.agent.limit_number(1)
                    
                    # add
                    self.agent.heading = self.agent.limit_number(self.agent.heading + self.agent.limit_number(wiglL))
                    
                    # subtract
                    self.agent.heading = self.agent.limit_number(self.agent.heading - self.agent.limit_number(wiglR))
                    
                    # if less than
                    if self.agent.limit_number(self.agent.heading) < self.agent.limit_number(0):
                        
                        # set
                        self.agent.invert = "NO"
                        
                        # add
                        self.agent.heading = self.agent.limit_number(self.agent.heading + self.agent.limit_number(180))
                    
                    # if greater than
                    if self.agent.limit_number(self.agent.heading) > self.agent.limit_number(180):
                        
                        # set
                        self.agent.invert = "NO"
                        
                        # subtract
                        self.agent.heading = self.agent.limit_number(self.agent.heading - self.agent.limit_number(180))
                
                # if equal
                if self.agent.invert == "NO":
                    
                    # if equal
                    if self.agent.limit_number(change_flag) == self.agent.limit_number(0):
                        
                        # add
                        self.agent.heading = self.agent.limit_number(self.agent.heading + self.agent.limit_number(wiglL))
                        
                        # subtract
                        self.agent.heading = self.agent.limit_number(self.agent.heading - self.agent.limit_number(wiglR))
                        
                        # if less than
                        if self.agent.limit_number(self.agent.heading) < self.agent.limit_number(0):
                            
                            # set
                            self.agent.invert = "YES"
                            
                            # add
                            self.agent.heading = self.agent.limit_number(self.agent.heading + self.agent.limit_number(180))
                        
                        # if greater than
                        if self.agent.limit_number(self.agent.heading) > self.agent.limit_number(180):
                            
                            # set
                            self.agent.invert = "YES"
                            
                            # subtract
                            self.agent.heading = self.agent.limit_number(self.agent.heading - self.agent.limit_number(180))
        
        def move(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action move')
            
            # if equal
            if self.agent.dead == "NO":
                
                # float declaration
                a = self.agent.limit_number(0)
                
                # float declaration
                b = self.agent.limit_number(0)
                
                # sin
                a = self.agent.limit_number(numpy.sin(numpy.deg2rad(self.agent.limit_number(self.agent.heading))))
                
                # sin
                b = self.agent.limit_number(numpy.sin(numpy.deg2rad(self.agent.limit_number(self.agent.heading))))
                
                # float declaration
                newx = self.agent.limit_number(self.agent.x)
                
                # float declaration
                newy = self.agent.limit_number(self.agent.y)
                
                # if greater than
                if self.agent.limit_number(self.agent.heading) > self.agent.limit_number(90):
                    
                    # subtract
                    newx = self.agent.limit_number(newx - self.agent.limit_number(a))
                
                # if greater than or equal
                if self.agent.limit_number(self.agent.heading) <= self.agent.limit_number(90):
                    
                    # add
                    newx = self.agent.limit_number(newx + self.agent.limit_number(a))
                
                # if equal
                if self.agent.invert == "YES":
                    
                    # subtract
                    newy = self.agent.limit_number(newy - self.agent.limit_number(b))
                
                # if equal
                if self.agent.invert == "NO":
                    
                    # add
                    newy = self.agent.limit_number(newy + self.agent.limit_number(b))
                
                # float declaration
                bump = self.agent.limit_number(0)
                
                # if less than
                if self.agent.limit_number(newx) < self.agent.limit_number(0):
                    
                    # set
                    bump = self.agent.limit_number(1)
                
                # if less than
                if self.agent.limit_number(newy) < self.agent.limit_number(0):
                    
                    # set
                    bump = self.agent.limit_number(1)
                
                # if greater than
                if self.agent.limit_number(newx) > self.agent.limit_number(99):
                    
                    # set
                    bump = self.agent.limit_number(1)
                
                # if greater than
                if self.agent.limit_number(newy) > self.agent.limit_number(99):
                    
                    # set
                    bump = self.agent.limit_number(1)
                
                # if equal
                if self.agent.limit_number(bump) == self.agent.limit_number(0):
                    
                    # set
                    self.agent.x = self.agent.limit_number(newx)
                    
                    # set
                    self.agent.y = self.agent.limit_number(newy)
                    
                    # subtract
                    self.agent.energy = self.agent.limit_number(self.agent.energy - self.agent.limit_number(1))
                
                # if equal
                if self.agent.limit_number(bump) == self.agent.limit_number(1):
                    
                    # add
                    self.agent.heading = self.agent.limit_number(self.agent.heading + self.agent.limit_number(90))
                    
                    # if greater than
                    if self.agent.limit_number(self.agent.heading) > self.agent.limit_number(180):
                        
                        # subtract
                        self.agent.heading = self.agent.limit_number(self.agent.heading - self.agent.limit_number(180))
                        
                        # float declaration
                        flag = self.agent.limit_number(0)
                        
                        # if equal
                        if self.agent.invert == "YES":
                            
                            # set
                            flag = self.agent.limit_number(1)
                            
                            # set
                            self.agent.invert = "NO"
                        
                        # if equal
                        if self.agent.invert == "NO":
                            
                            # if equal
                            if self.agent.limit_number(flag) == self.agent.limit_number(0):
                                
                                # set
                                self.agent.invert = "YES"
        
        def check_if_dead(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action check_if_dead')
            
            # if greater than or equal
            if self.agent.limit_number(self.agent.energy) <= self.agent.limit_number(0):
                
                # set
                self.agent.dead = "YES"
        
        async def eat_sheep(self):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action eat_sheep')
            send = { "type": "eat", "performative": "Request", "x": 0.0, "y": 0.0, }
            
            # set
            send["x"] = self.agent.limit_number(self.agent.x)
            
            # set
            send["y"] = self.agent.limit_number(self.agent.y)
            
            # send
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Send message {send} to {self.agent.sheep}')
            for receiver in self.agent.sheep:
                await self.send(self.agent.get_spade_message(receiver, send))
                self.agent.msgSCount = self.agent.limit_number(self.agent.msgSCount + 1)
            
            # set
            self.agent.is_eating = "YES"
        
        async def run(self):
            self.wiggle()
            self.move()
            self.check_if_dead()
            await self.eat_sheep()
    
    class recv_spawn(spade.behaviour.CyclicBehaviour):
        def spawn(self, rcv):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action spawn')
            
            # set
            self.agent.dead = "NO"
        
        async def run(self):
            rcv = await self.receive(timeout=100000)
            if rcv:
                rcv = self.agent.get_json_from_spade_message(rcv)
                self.agent.msgRCount = self.agent.limit_number(self.agent.msgRCount + 1)
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Received message: {rcv}')
                self.spawn(rcv)
    
    class rcv_eat(spade.behaviour.CyclicBehaviour):
        async def eat_sheep(self, rcv):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action eat_sheep')
            send = { "type": "kill", "performative": "Inform", }
            
            # if equal
            if self.agent.is_eating == "YES":
                
                # set
                self.agent.is_eating = "NO"
                
                # send
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Send message {send} to {"RCV.jid"}')
                await self.send(self.agent.get_spade_message("RCV.jid", send))
                self.agent.msgSCount = self.agent.limit_number(self.agent.msgSCount + 1)
        
        async def run(self):
            rcv = await self.receive(timeout=100000)
            if rcv:
                rcv = self.agent.get_json_from_spade_message(rcv)
                self.agent.msgRCount = self.agent.limit_number(self.agent.msgRCount + 1)
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Received message: {rcv}')
                await self.eat_sheep(rcv)
    
    class recv_broadcast(spade.behaviour.CyclicBehaviour):
        def save_data(self, rcv):
            if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Run action save_data')
            
            # if equal
            if self.agent.limit_number(rcv["typ"]) == self.agent.limit_number(0):
                
                # add element
                self.agent.field.append("RCV.jid")
            
            # if equal
            if self.agent.limit_number(rcv["typ"]) == self.agent.limit_number(1):
                
                # add element
                self.agent.sheep.append("RCV.jid")
        
        async def run(self):
            rcv = await self.receive(timeout=100000)
            if rcv:
                rcv = self.agent.get_json_from_spade_message(rcv)
                self.agent.msgRCount = self.agent.limit_number(self.agent.msgRCount + 1)
                if self.agent.logger: self.agent.logger.debug(f'[{self.agent.jid}] Received message: {rcv}')
                self.save_data(rcv)
    

import random
import uuid
import numpy


def generate_graph_structure(domain):
    _num_grass = 1
    _num_sheep = 95
    _num_wolf = 5
    num_agents = _num_grass + _num_sheep + _num_wolf
    random_id = str(uuid.uuid4())[:5]
    jids = [f"{i}_{random_id}@{domain}" for i in range(num_agents)]
    agents = []
    next_agent_idx = 0
    for _ in range(_num_grass):
        num_connections = 100
        num_connections = max(min(num_connections, len(jids) - 1), 0)
        jid = jids[next_agent_idx]
        agents.append({
            "jid": jid,
            "type": "grass",
            "connections": random.sample([other_jid for other_jid in jids if other_jid != jid], num_connections),
        })
        next_agent_idx += 1
    for _ in range(_num_sheep):
        num_connections = 100
        num_connections = max(min(num_connections, len(jids) - 1), 0)
        jid = jids[next_agent_idx]
        agents.append({
            "jid": jid,
            "type": "sheep",
            "connections": random.sample([other_jid for other_jid in jids if other_jid != jid], num_connections),
        })
        next_agent_idx += 1
    for _ in range(_num_wolf):
        num_connections = 100
        num_connections = max(min(num_connections, len(jids) - 1), 0)
        jid = jids[next_agent_idx]
        agents.append({
            "jid": jid,
            "type": "wolf",
            "connections": random.sample([other_jid for other_jid in jids if other_jid != jid], num_connections),
        })
        next_agent_idx += 1
    return agents
