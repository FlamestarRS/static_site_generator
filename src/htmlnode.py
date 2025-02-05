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
        for key in self.props:
            str = f' {key}="{self.props[key]}"'
            all_props.append(str)

        all_props_str = "".join(all_props)

        return all_props_str
    
    def __repr__ (self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"