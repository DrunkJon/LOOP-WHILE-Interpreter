class Node:
    def eval(self, context: dict):
        pass


class BinaryNode(Node):
    left: Node
    right: Node


class UnaryNode(Node):
    right: Node


class LeafNode(Node):
    var: any


class BlockNode(Node):
    inner: list

    def eval(self, context: dict):
        for node in self.inner:
            # relies on context getting changed by AssignNodes
            node.eval(context)


class NameDefNode(Node):
    name: str
    inner: list
    # list of numbers that will be converted to var names in new context
    inputs: list

    def __init__(self, name: str, inner: list, inputs: list):
        self.name = name
        self.inner = inner
        self.inputs = inputs
        
    def eval(self, context: dict):
        context["NAME"][self.name] = self

    def build_context(self, inputs: list) -> dict:
        assert len(inputs) == len(self.inputs)
        # expressly forbids recursion
        context = {
            "VAR": {},
            "NAME": {}
        }
        for i, x in zip(self.inputs, inputs):
            context["VAR"][f"x{i}"] = x
        return context

    def get_inner(self):
        return self.inner


class NameCallNode(Node):
    name: str
    # list of var names
    inputs: list

    def __init__(self, name, inputs):
        self.name = name
        self.inputs = inputs

    def eval(self, context):
        inputs = [x.eval(context) for x in self.inputs]
        definition = context["NAME"][self.name]
        inner_context = definition.build_context(inputs)
        inner = definition.get_inner()
        for node in inner:
            node.eval(inner_context)

        # return x0 val from inner context
        output_node = VarNode("x0")
        return output_node.eval(inner_context)


class VarNode(LeafNode):
    val: str

    def __init__(self, val):
        self.val = val

    def eval(self, context: dict):
        if self.val not in context["VAR"].keys():
            context["VAR"][self.val] = 0
        return context["VAR"][self.val]


class ConstNode(LeafNode):
    val: int

    def __init__(self, val: int):
        self.val = val

    def eval(self, context):
        return self.val


class PlusNode(BinaryNode):
    left: VarNode
    right: ConstNode

    def __init__(self, var: VarNode, const: ConstNode):
        self.left = var
        self.right = const

    def eval(self, context):
        return self.left.eval(context) + self.right.eval(context)


class MinusNode(BinaryNode):
    left: VarNode
    right: ConstNode

    def __init__(self, var: VarNode, const: ConstNode):
        self.left = var
        self.right = const

    def eval(self, context):
        return self.left.eval(context) - self.right.eval(context)


class AssignNode(BinaryNode):
    left: VarNode
    right: BinaryNode

    def __init__(self, var: VarNode, right: BinaryNode):
        self.left = var
        self.right = right

    def eval(self, context):
        context["VAR"][self.left.val] = self.right.eval(context)


class LoopNode(BlockNode):
    counter: VarNode
    inner = []

    def __init__(self, counter: VarNode, inner: list = None):
        self.counter = counter
        if inner:
            self.inner = inner

    def eval(self, context):
        for _ in range(self.counter.eval(context)):
            super().eval(context)


class WhileNode(BlockNode):
    counter: VarNode
    inner = []

    def __init__(self, counter: VarNode, inner: list = None):
        self.counter = counter
        if inner:
            self.inner = inner

    def eval(self, context):
        while self.counter.eval(context) != 0:
            super().eval(context)
