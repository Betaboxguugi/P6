import ast

Wanted_List = {'ConnectionWrapper', 'SQLSource'}

x = 0

def get_id():
    global x
    s = 'test_' + str(x)
    x += 1
    return s


class DepthFirstVisitor(ast.NodeVisitor):
    """
    """

    def depth_first(func):
        """
        """
        def wrapper(self, node):
            func(self, node)
            for child in ast.iter_child_nodes(node):
                self.visit(child)
        return wrapper

    @depth_first
    def visit_Call(self, node):
        name = None
        if hasattr(node.func, 'id'):
            name = node.func.id
            print(name)
        else:
            if hasattr(node.func, 'attr'):
                name = node.func.attr
                print(name)
        if name in Wanted_List:
            self.__replace_connection(node)

            
    def __replace_connection(self, node):
        id = get_id()
        if id is not None:
            newode = ast.Name(id=id, ctx=ast.Load())
            if len(node.args) != 0:
                print('Before:', node.args[0].id)
                node.args[0] = newode
                print('After:', node.args[0].id)  
            else:
                for keyword in node.keywords:
                    if keyword.arg == 'connection':
                        print('Before:', keyword.value.id)
                        keyword.value = newode
                        print('After:', keyword.value.id)           
        


def main():
    with open('./sample_program.py', 'r') as f:
        program = f.read()

    dfv = DepthFirstVisitor()
    tree = ast.parse(program)
    print(ast.dump(tree))
    dfv.visit(tree)


if __name__ == '__main__':
    main()


