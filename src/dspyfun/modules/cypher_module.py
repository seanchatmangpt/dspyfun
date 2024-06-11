from typing import List, Optional, Union

import dspy
from pydantic import BaseModel
import re

class Property(BaseModel):
    key: str
    value: Union[str, int, float, bool]

    def to_cypher(self) -> str:
        if isinstance(self.value, str):
            return f'{self.key}: "{self.value}"'
        return f'{self.key}: {self.value}'

    @staticmethod
    def from_cypher(prop_str: str) -> 'Property':
        key, value = prop_str.split(':')
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value.strip('"')
        elif value.isdigit():
            value = int(value)
        elif re.match(r'^\d+\.\d+$', value):
            value = float(value)
        elif value.lower() in ('true', 'false'):
            value = value.lower() == 'true'
        return Property(key=key.strip(), value=value)

class Node(BaseModel):
    label: Optional[str]
    properties: Optional[List[Property]] = []

    def to_cypher(self) -> str:
        label_str = f':{self.label}' if self.label else ''
        props_str = "{" + ", ".join(prop.to_cypher() for prop in self.properties) + "}" if self.properties else ''
        return f'({label_str} {props_str})'.strip()

    @staticmethod
    def from_cypher(node_str: str) -> 'Node':
        label_match = re.search(r':(\w+)', node_str)
        label = label_match.group(1) if label_match else None
        properties = []
        props_match = re.search(r'\{(.*?)\}', node_str)
        if props_match:
            props_str = props_match.group(1)
            props = [prop.strip() for prop in props_str.split(',')]
            properties = [Property.from_cypher(prop) for prop in props]
        return Node(label=label, properties=properties)

class Relationship(BaseModel):
    type: Optional[str]
    properties: Optional[List[Property]] = []

    def to_cypher(self) -> str:
        type_str = f':{self.type}' if self.type else ''
        props_str = "{" + ", ".join(prop.to_cypher() for prop in self.properties) + "}" if self.properties else ''
        return f'-[{type_str} {props_str}]-'.strip()

    @staticmethod
    def from_cypher(rel_str: str) -> 'Relationship':
        type_match = re.search(r':(\w+)', rel_str)
        type_ = type_match.group(1) if type_match else None
        properties = []
        props_match = re.search(r'\{(.*?)\}', rel_str)
        if props_match:
            props_str = props_match.group(1)
            props = [prop.strip() for prop in props_str.split(',')]
            properties = [Property.from_cypher(prop) for prop in props]
        return Relationship(type=type_, properties=properties)

class Pattern(BaseModel):
    start_node: Node
    relationship: Optional[Relationship]
    end_node: Optional[Node]

    def to_cypher(self) -> str:
        start = self.start_node.to_cypher()
        relationship = self.relationship.to_cypher() if self.relationship else ''
        end = self.end_node.to_cypher() if self.end_node else ''
        return f'{start}{relationship}{end}'

    @staticmethod
    def from_cypher(pattern_str: str) -> 'Pattern':
        node_re = r'\((.*?)\)'
        rel_re = r'\[.*?\]'
        nodes = re.findall(node_re, pattern_str)
        rels = re.findall(rel_re, pattern_str)
        start_node = Node.from_cypher(nodes[0])
        relationship = Relationship.from_cypher(rels[0]) if rels else None
        end_node = Node.from_cypher(nodes[1]) if len(nodes) > 1 else None
        return Pattern(start_node=start_node, relationship=relationship, end_node=end_node)

class ReturnItem(BaseModel):
    expression: str
    alias: Optional[str] = None

    def to_cypher(self) -> str:
        return f'{self.expression} AS {self.alias}' if self.alias else self.expression

    @staticmethod
    def from_cypher(return_str: str) -> 'ReturnItem':
        parts = return_str.split(' AS ')
        expression = parts[0].strip()
        alias = parts[1].strip() if len(parts) > 1 else None
        return ReturnItem(expression=expression, alias=alias)

class CypherQuery(BaseModel):
    match_clause: List[Pattern]
    where: Optional[str] = None
    return_items: List[ReturnItem]

    def to_cypher(self) -> str:
        match_clause = 'MATCH ' + ', '.join(pattern.to_cypher() for pattern in self.match_clause)
        where_clause = f' WHERE {self.where}' if self.where else ''
        return_clause = ' RETURN ' + ', '.join(item.to_cypher() for item in self.return_items)
        return match_clause + where_clause + return_clause

    @staticmethod
    def from_cypher(query_str: str) -> 'CypherQuery':
        match_re = r'MATCH (.*?)(?: WHERE| RETURN|$)'
        where_re = r'WHERE (.*?)(?: RETURN|$)'
        return_re = r'RETURN (.*)'

        match_clause_str = re.search(match_re, query_str).group(1)
        where_clause_str = re.search(where_re, query_str).group(1) if re.search(where_re, query_str) else None
        return_clause_str = re.search(return_re, query_str).group(1)

        patterns = [Pattern.from_cypher(pattern.strip()) for pattern in match_clause_str.split(',')]
        return_items = [ReturnItem.from_cypher(item.strip()) for item in return_clause_str.split(',')]

        return CypherQuery(match_clause=patterns, where=where_clause_str, return_items=return_items)

# Example usage
query = CypherQuery(
    match_clause=[
        Pattern(
            start_node=Node(label="Person", properties=[Property(key="name", value="Alice")]),
            relationship=Relationship(type="KNOWS"),
            end_node=Node(label="Person", properties=[Property(key="name", value="Bob")])
        )
    ],
    where="age > 30",
    return_items=[ReturnItem(expression="n", alias="person")]
)

# cypher_str = query.to_cypher()
# print("Generated Cypher Query:", cypher_str)
#
# parsed_query = CypherQuery.from_cypher(cypher_str)
# print("Parsed Query:", parsed_query)



class CypherConverter(dspy.Signature):
    """
    Convert unstructured text into cypher language.
    """
    text = dspy.InputField(desc="The unstructured text that needs to be converted to cypher language.")
    cypher_language = dspy.InputField(desc="The language or type of cypher to use for conversion.")

    valid_cypher_text = dspy.OutputField(desc="The text converted into the specified cypher language.")


class CypherModule(dspy.Module):
    def forward(self, text):
        pred = dspy.ChainOfThought(CypherConverter)
        response = pred.forward(text=text, cypher_language="cypher").valid_cypher_text
        print(response)


def cypher_call(text: str):
    mod = CypherModule()
    return mod.forward(text)


cypher_str = """CREATE (person1 {name: 'Speaker'})
CREATE (person2 {name: 'Listener'})
CREATE (park {name: 'Park'})
CREATE (time {hour: 5, period: 'PM'})

MATCH (p1:Person), (p2:Person)
WHERE p1.name = 'Speaker' AND p2.name = 'Listener'
CREATE (meeting:Meeting {location: park, time: time})
CREATE (person1)-[:MEET]->(meeting)
CREATE (person2)-[:MEET]->(meeting)"""


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()

    print(cypher_call("Meet me at the park at 5PM"))
    # parsed_query = CypherQuery.from_cypher(cypher_str)
    # print(parsed_query)


if __name__ == '__main__':
    main()
