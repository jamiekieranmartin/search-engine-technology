# Jamie Martin
# N10212361
import re


class XMLParser:
    """
    Parses an XML string to a dict
    """

    def __init__(self, xml):
        """
        Parser initialiser, takes xml string
        :param xml: string, the xml to parse
        """
        self.xml = self.strip(xml)
        self.xml = self.xml.replace("\n", "")

        self.declaration = self.get_declaration()
        self.root = self.tag()

    # --- Parsing Methods ---

    def get_declaration(self):
        """
        Gets the declaration from self.xml
        :return: dict, the node
        """
        m = self.match(r'(<\?xml\s*)')
        if not m:
            return

        node = {'attributes': {}}

        while not (self.eos() or self._is('?>')):
            attr = self.attribute()
            if not attr:
                return node
            node['attributes'][attr['name']] = attr['value']

        self.match(r'(\?>\s*)')

        return node

    def tag(self):
        """
        Gets the tag/s from self.xml
        :return: dict, the node
        """
        # attempt to match first section of xml i.e: <newsitem
        m = self.match(r'^(<)(\w+)(\s*)')
        if not m:
            return

        # initialises node with name from match, i.e newsitem
        node = {'name': m[1], 'attributes': {}, 'children': [], 'content': ''}

        # parses attribtues whilst looking for >, />, etc
        while not (self.eos() or self._is('>') or self._is('?>') or self._is('/>')):
            attr = self.attribute()
            if not attr:
                break
            # attaches attributes to node
            node['attributes'][attr['name']] = attr['value']
        
        # attempt to match node end without children, i.e />
        if self.match(r'^(\s*\/>)(\s*)'):
            # return if no children
            return node

        # attempt to match node with children, i.e >
        self.match(r'(\??)(>)(\s*)')

        # parse node content (string, not children)
        node['content'] = self.content()

        # attempt to parse children
        while True:
            child = self.tag()
            if child is None:
                break
            node['children'].append(child)

        # match closing tag, i.e </newsitem>
        self.match(r'^(<\/)(\w+)(>)(\s*)')

        return node

    def content(self):
        """
        Gets content of a node
        :return: string, node content
        """
        m = self.match(r'^([^<]*)')
        if m:
            return m[0]
        return ''

    def attribute(self):
        """
        Gets next attribute
        :return: dict, attribute 'name' and 'value'
        """
        # attempt to match attributes, i.e itemid="123"
        m = self.match(r'([\w:-]+)(\s*=\s*)(")([^"]*)("|\'[^\']*\'|\w+)(\s*)')
        if not m:
            return
        return {'name': m[0], 'value': self.strip(m[3])}

    def strip(self, value):
        """
        Strips unnecessary chars
        :param value: string, the value to strip
        :return: string, stripped value
        """
        return value.replace(r'^[\'"]|[\'"]$', '')

    def match(self, expression):
        """
        Tries to match expression, then remove that from the buffer
        :param expression: string, the expression to match and remove
        :return: dict, the regex match to extract values
        """
        m = re.match(expression, self.xml)
        if not m:
            return
        m = m.groups()
        self.xml = self.xml[sum(list([len(x) for x in m])):]
        return m

    def eos(self):
        """
        True if at the end of the buffer
        :return: boolean, buffer ended
        """
        return 0 is len(self.xml)

    def _is(self, prefix):
        """
        Whether the buffer starts with prefix
        :param prefix: string, the prefix to match
        :return: boolean, True if prefix matches start of buffer
        """
        return self.xml.startswith(prefix)

    # --- Document Methods ---

    def get_by_attribute(self, attr):
        """
        Gets nodes containing attribute name
        :param attr: string, the attribute name
        :return: []dict, the matched nodes
        """
        lam = lambda child: attr in child['attributes']
        if lam(self.root):
            return [self.root]
        return self.by([], self.root['children'], lam)

    def get_by_name(self, name):
        """
        Gets nodes by name 
        :param name: string, the node name
        :return: []dict, the matched nodes
        """
        lam = lambda child: child['name'] == name
        if lam(self.root):
            return [self.root]
        return self.by([], self.root['children'], lam)

    def by(self, res, children, lam):
        """
        Recursive search function, searches for nodes where lam returns True
        :param res: []dict, the nodes matched
        :param children: []dict, the children nodes to search through
        :param lam: lambda: child, filter criteria
        :return: []dict, the matched nodes
        """
        if children:
            for child in children:
                if lam(child):
                    res.append(child)

                if 'children' in child:
                    self.by(res, child['children'], lam)
        return res
