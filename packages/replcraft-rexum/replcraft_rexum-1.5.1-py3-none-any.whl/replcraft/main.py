import websocket
import json
from base64 import b64decode


class ReplCraft:
    def __init__(self, token):
        self.token = token.replace('http://', '')
        self.config = json.loads(b64decode(token.split('.')[1] + '===='))
        self.nonce = "0"

    # Logs in :)
    def login(self):
        self.ws = websocket.create_connection('ws://' + self.config['host'] + '/gateway')
        self._send(
            {
                "action": "authenticate",
                "token": self.token,
                "nonce": self.nonce
            }
        )

    # Retrieves a block at the given structure-local coordinates.
    def get_block(self, x, y, z):
        return self._send(
            {
                "action": "get_block",
                "x": x,
                "y": y,
                "z": z,
                "nonce": self.nonce
            }
        )

    # Retrieves the world coordinate location of the (0,0,0)
    def location(self, x, y, z):
        return self._send(
            {
                "action": "get_location",
                "x": x,
                "y": y,
                "z": z,
                "nonce": self.nonce
            }
        )

    # Retrieves the inner size of the structure.
    def get_size(self, x, y, z):
        return self._send(
            {
                "action": "get_size",
                "x": x,
                "y": y,
                "z": z,
                "nonce": self.nonce
            }
        )

    # Sets a block at the given structure-local coordinates. The block must be available
    # in the specified source chest or the structure inventory. Any block replaced by this call
    # is stored in the specified target chest or the structure inventory, or dropped in the
    # world if there's no space.
    #
    # :source_x, source_y, source_z: The container the block to set is in.
    # :target_x, target_y, target_z: The container the block replaced should go to.
    def set_block(self, x, y, z, blockdata, source_x=None, source_y=None, source_z=None, target_x=None, target_y=None,
                  target_z=None):
        return self._send(
            json.dumps({
                "action": "set_block",
                "x": x,
                "y": y,
                "z": z,
                "blockData": blockdata,
                "source_x": source_x,
                "source_y": source_y,
                "source_z": source_z,
                "target_x": target_x,
                "target_y": target_y,
                "target_z": target_z,
                "nonce": self.nonce
            })
        )

    # Retrieves the text of a sign at the given coordinates.
    def get_sign_text(self, x, y, z):
        return self._send(
            {
                "action": "get_sign_text",
                "x": x,
                "y": y,
                "z": z,
                "nonce": self.nonce
            }
        )

    # Sets the text of a sign at the given coordinates.
    def set_sign_text(self, x, y, z, lines):
        return self._send(
            {
                "action": "set_sign_text",
                "x": x,
                "y": y,
                "z": z,
                "lines": lines,
                "nonce": self.nonce
            }
        )

    # Begins watching a block for updates.
    def watch(self, x, y, z):
        return self._send(
            {
                "action": "watch",
                "x": x,
                "y": y,
                "z": z,
                "nonce": self.nonce
            }
        )

    # Stops watching a block for updates.
    def unwatch(self, x, y, z):
        return self._send(
            {
                "action": "unwatch",
                "x": x,
                "y": y,
                "z": z,
                "nonce": self.nonce
            }
        )

    # Begins watching all blocks in the structure for updates.
    def watch_all(self):
        return self._send(
            {
                "action": "watch_all",
                "nonce": self.nonce
            }
        )

    # Stops watching all blocks for updates.
    def unwatch_all(self):
        return self._send(
            {
                "action": "unwatch_all",
                "nonce": self.nonce
            }
        )

    # Begins polling all blocks in the structure for updates.
    # Updates will be very slow!
    def poll_all(self):
        return self._send(
            {
                "action": "poll_all",
                "nonce": self.nonce
            }
        )

    # Stops polling all blocks in the structure.
    def unpoll_all(self):
        return self._send(
            {
                "action": "unpoll_all",
                "nonce": self.nonce
            }
        )

    # Begins polling a block for updates.
    # Note that this catches all possible block updates, but only one block is polled per tick.
    # The more blocks you poll, the slower each individual block will be checked.
    # Additionally, if a block changes multiple times between polls, only the latest change
    # will be reported.
    def poll(self, x, y, z):
        return self._send(
            {
                "action": "poll",
                "x": x,
                "y": y,
                "z": z,
                "nonce": self.nonce
            }
        )

    # Stops watching a block for updates.
    def unpoll(self, x, y, z):
        return self._send(
            {
                "action": "unpoll",
                "x": x,
                "y": y,
                "z": z,
                "nonce": self.nonce
            }
        )

    # Gets all entities inside the region.
    def get_entities(self):
        return self._send(
            {
                "action": "get_entities",
                "nonce": self.nonce
            }
        )

    # Gets all items from a container such as a chest or hopper.
    def get_inventory(self, x, y, z):
        return self._send(
            {
                "action": "get_inventory",
                "x": x,
                "y": y,
                "z": z,
                "nonce": self.nonce
            }
        )

    # Moves an item between containers.
    def move_item(self, index, source_x, source_y, source_z, target_x, target_y, target_z, target_index=None, amount=None):
        return self._send(
            {
                "action": "move_item",
                "amount": amount,
                "index": index,
                "source_x": source_x,
                "source_y": source_y,
                "source_z": source_z,
                "target_index": target_index,
                "target_x": target_x,
                "target_y": target_y,
                "target_z": target_z,

                "nonce": self.nonce
            }
        )

    # Gets a block's redstone power level.
    def get_power_level(self, x, y, z):
        return self._send(
            {
                "action": "get_power_level",
                "x": x,
                "y": y,
                "z": z,
                "nonce": self.nonce
            }
        )

    # Crafts an item, which is then stored into the given container.
    def craft(self, x, y, z, recipe):
        return self._send(
            json.dumps({
                "action": "craft",
                "x": x,
                "y": y,
                "z": z,
                "ingredients": recipe,
                "nonce": self.nonce
            })
        )

    # Retrieves detailed information about fuel use, fuel sources, and active connections.
    def fuel_info(self):
        return self._send(
            {
                "action": "fuelinfo",
                "nonce": self.nonce
            }
        )

    # Sends a chat message to a player inside your structure
    def tell(self, target, message):
        return self._send(
            {
                "action": "tell",
                "target": target,
                "message": message,
                "nonce": self.nonce
            }
        )

    # Sends money to a player
    def pay(self, target, amount):
        return self._send(
            {
                "action": "tell",
                "target": target,
                "amount": amount,
                "nonce": self.nonce
            }
        )

    # Listen for any server communication, use after watch & poll methods.

    def listen(self):
        return self._recv()

    def disconnect(self):
        self.ws.close()

    # PRIVATE

    def _recv(self):
        return json.loads(self.ws.recv())

    def _send(self, data):
        self.ws.send(str(data))
        self.nonce = str(int(self.nonce) + 1)

        if 'nonce' in data:
            return self._recv()


# Index of an item withing a container.
#
# :index: index of the slot the time is in within the container.
# :x, y, z: the coordinates of the container.
class ItemIndex:
    def __init__(self, index, x, y, z):
        self.index = index  # The index of the chest slot the item is in.
        self.x = x
        self.y = y
        self.z = z

    def item(self):
        return {
            "index": self.index,
            "x": self.x,
            "y": self.y,
            "z": self.z
        }


# Recipe, matching its vanilla definition
#
# :s1-s9: crafting table slots
class Recipe:
    def __init__(self, s1=None, s2=None, s3=None, s4=None, s5=None, s6=None, s7=None, s8=None, s9=None):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.s4 = s4
        self.s5 = s5
        self.s6 = s6
        self.s7 = s7
        self.s8 = s8
        self.s9 = s9

    def table(self):
        return [
            self.s1, self.s2, self.s3,
            self.s4, self.s5, self.s6,
            self.s7, self.s8, self.s9
        ]
