class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        all_props = []
        if isinstance(self.props, str):
            return self.props
        for key in self.props:
            string = f' {key}="{self.props[key]}"'
            all_props.append(string)

        all_props_str = "".join(all_props)

        return all_props_str
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: no value")
        if self.tag == None:
            return str(self.value)
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        htmlprops = super().props_to_html()
        return f"<{self.tag}{htmlprops}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Invalid HTML: no tag")
        if self.children == None:
            raise ValueError("Invalid HTML: no children")
        if self.props != None:
            htmlprops = super().props_to_html()
        else:
            htmlprops = ""    
        return f"<{self.tag}{htmlprops}>{self.children_list()}</{self.tag}>"

       
    def children_list(self):
        if not isinstance(self.children, (list, LeafNode, ParentNode)):
            raise ValueError("Invalid HTML: child is not LeafNode(s)")
        if isinstance(self.children, (LeafNode, ParentNode)):
            return self.children.to_html()
        child_list = ""
        for child in self.children:
            child_list += child.to_html()
        return child_list
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
