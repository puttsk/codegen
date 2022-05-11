import re
from typing import Iterable
from io import TextIOWrapper

command_block_regex = re.compile(r"\s*<<\s*(?P<type>[a-zA-Z-]+)(\s+(?P<params>[a-zA-Z-]+(\s+[a-zA-Z-]+)*))?\s*>>\s*")
variable_regex = re.compile(r"(?P<var>{{\s*(?P<attr>[a-zA-Z0-9_]+)}})")

def create_block(type: str):
    if type == 'for-block':
        return ForBlock()
    else:
        return None
        
class Block:
    def __init__(self):
        self.body = []
        self.type = None

    def append_body(self, l: str):
        self.body.append(l)

    def process(self, data: Iterable, out: TextIOWrapper):
        for b in self.body:
            if isinstance(b, Block):
                b.process(data, out)
            else:
                out.write(b)

    def read_block(self, t: TextIOWrapper):
        while l := t.readline():
            # Check if the line contain command block
            if cmd := command_block_regex.match(l):
                cmd_type = cmd.group('type')
                cmd_params = cmd.group('params').split(' ')

                # Begin a new control block
                if cmd_params[0] == 'begin':
                    b = create_block(cmd_type)
                    b.read_block(t)
                    self.append_body(b)
                elif cmd_params[0] == 'end' and cmd_type == self.type:
                    break
            else:
                self.append_body(l)

    def __repr__(self) -> str:
        s = []
        for b in self.body:
            s.append(str(b))
        return ''.join(s)

    def __str__(self) -> str:
        s = []
        for b in self.body:
            s.append(str(b))
        return ''.join(s)

class ForBlock(Block):
    def __init__(self):
        super().__init__()
        self.type = 'for-block'
    pass

    def process(self, data: Iterable, out: TextIOWrapper):
        for d in data:
            for b in self.body:
                # b is block
                if isinstance(b, Block):
                    b.process(d, out)
                # b is string
                else:
                    new_line = b
                    for v in variable_regex.finditer(new_line):
                        var = v.group('var')
                        
                        if isinstance(d, dict):
                            attr = d[v.group('attr')]
                        else:
                            attr = getattr(d, v.group('attr'))
                        
                        new_line = new_line.replace(var, str(attr))
                    out.write(new_line)

    def __str__(self) -> str:
        s = []

        s.append('Begin for\n')
        for b in self.body:
            s.append(str(b))
        s.append('End for\n')
        return ''.join(s)
