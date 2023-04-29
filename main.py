from anytree import AnyNode, RenderTree

def main():
    root = AnyNode(id="root")
    s0 = AnyNode(id="sub0", parent=root)
    print(RenderTree(root).by_attr('id'))

if __name__ == '__main__':
    main()
