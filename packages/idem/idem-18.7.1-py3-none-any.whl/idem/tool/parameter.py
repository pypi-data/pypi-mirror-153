"""
These classes are used to extract paramaters used inside
SLS files during validation. The code works by simulating
get() function of Python Dictionary object. As we get any
request to access parameter foo using {{ params.get('foo') }}
in SLS file we capture that request sending back a dummy
value, and identifying the parameter name in the process.

To give specific example, a SLS file like this:

    Assure Resource Group Present {{ params.get('rg_name').get('your_rg') }}:
    azure.resource_management.resource_groups.present:
        - resource_group_name: {{ params.get('rg_name').get('your_rg') }}
        - parameters:
            - location{{ params['locations'][4].name }}

    Assure Resource Group Present {{ params.get('rg_name').get('my_rg', 'rg') }}:
    azure.resource_management.resource_groups.present:
        - resource_group_name: {{ params.get('rg_name').get('my_rg', 'rg') }}
        - parameters:
            - location{{ params['locations'][0].name }}

will produce parameter section like the following in
validate sub command output:

    "parameters": {
        "rg_name": {
            "your_rg": "",
            "my_rg": "rg"
        },
        "locations": [
            {
                "name": ""
            }
        ]
    }

TODO: Implement rest of Python dict functionality in Parameters

"""


class BaseParam:
    def __init__(
        self, parent, name, display, is_indexing_operator, internal, default
    ) -> None:
        self._parent = parent
        self._name = str(name)
        self._display = BaseParam._get_display(
            name, display, is_indexing_operator, default
        )
        self._internal = internal
        self._default = "" if default is None else default
        self._params = {}
        self._is_leaf = False
        self._attributes = set()

    @staticmethod
    def _get_display(name, parent_display, is_indexing_operator, default):
        if parent_display is None:
            return ""
        ret = "params" if len(parent_display) == 0 else f"{parent_display}"
        if isinstance(name, int):
            return f"{ret}[{name}]"
        elif is_indexing_operator:
            return f"{ret}['{name}']"
        else:
            return (
                f"{ret}.get('{name}')"
                if default is None
                else f"{ret}.get('{name}', '{default}')"
            )

    def params(self):
        if not self._params:
            return self._default

        ret = None
        for key, value in self._params.items():
            if isinstance(key, int):
                if ret is None:
                    ret = []
                for i in range(len(ret), key + 1):
                    ret.append(None)
                ret[key] = value.params()
            else:
                if ret is None:
                    ret = {}
                ret[key] = value.params()

        return ret

    def _create_child(self, param, is_indexing_operator, default=None):
        if self._is_leaf:
            raise TypeError(
                f"Terminal leaf can not have atrributes: {self._display} can not have attribute {param}."
            )

        if isinstance(param, int):
            internal = f"{self._internal}[{param}]"
            child = ParamArray(
                self, param, self._display, is_indexing_operator, internal, default
            )
        else:
            internal = (
                f"^^{param}^^"
                if self._internal == "" or self._internal is None
                else f"{self._internal}.~~{param}"
            )
            child = ParamObject(
                self, param, self._display, is_indexing_operator, internal, default
            )

        self._params[param] = child
        return child

    def _get_value(self, param):
        if param in self._params:
            return self._params[param]

    def _set_display(self, display):
        self._display = display

    def __getitem__(self, param):
        return self.get(param)

    def __str__(self) -> str:
        return f"?? {self._display} ?? {self._internal} ??"

    def items(self):
        return ResponseObject(self, 2)

    def __getattr__(self, name):
        if name not in self._attributes:
            self._attributes.add(name)
        raise AttributeError(
            f"Function {self._name} is not supported on {self._parent._display}"
        )

    def __call__(self, *args, **kwargs):
        return self


class ResponseObject:
    def __init__(self, item, pack_count=0):
        self._item = item
        self._next_index = 0
        self._index = 0
        self._pack_count = pack_count

    def __len__(self):
        return self._pack_count

    def __getitem__(self, index):
        if self._index == 0:
            self._index += 1
            if self._pack_count == 0:
                return self._item

            t = []
            for i in range(self._pack_count):
                t.append(str(self._item))
            return tuple(t)

        self._index = 0
        raise StopIteration

    def __call__(self, *args, **kwargs):
        return self

    def __next__(self):
        if self._next_index == 0:
            self._next_index += 1
            return self
        self._next_index = 0
        raise StopIteration

    def __str__(self):
        return str(self._item)


class ParamObject(BaseParam):
    def __init__(
        self, parent, name, display, is_indexing_operator, internal, default
    ) -> None:
        super().__init__(parent, name, display, is_indexing_operator, internal, default)

    def _get_common(self, param, is_indexing_operator, default):
        child = super()._get_value(param)
        if child is not None:
            return child

        if param in self._attributes:
            return ResponseObject(self)

        return super()._create_child(param, is_indexing_operator, default)

    def get(self, param, default=None):
        return self._get_common(param, False, default)

    def __getitem__(self, param):
        return self._get_common(param, True, None)

    def __iter__(self):
        return ResponseObject(self)


class ParamArray(ParamObject):
    def __init__(
        self, parent, name, display, is_indexing_operator, internal, default
    ) -> None:
        super().__init__(parent, name, display, is_indexing_operator, internal, default)

    def __str__(self) -> str:
        self._is_leaf = True
        return super().__str__()


class Parameters(ParamArray):
    def __init__(self) -> None:
        super().__init__(None, None, None, False, None, None)


def get_validate_params(hub):
    return Parameters()
