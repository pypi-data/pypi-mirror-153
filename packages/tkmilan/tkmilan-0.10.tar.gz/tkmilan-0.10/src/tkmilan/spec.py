'''Specification for `MixinState` possibilities.

This is really initial validation handling.
'''
import typing
import collections
import collections.abc


smvT = typing.TypeVar('smvT')
'''Generic Type for `StaticMap`.

This is a `typing.TypeVar`, to be used only when typechecking. See `typing`.
'''


class Spec:
    '''Parent class for specification definitions.

    These are objects that define the specification for the possible states for
    some widgets.

    Note that this might specify a complex validation, not just a list of
    discrete values, nor a continous range, for example.

    See `SpecCountable`.

    .. automethod:: __contains__
    '''

    default: str
    '''The default label to be shown to the user.'''

    def __contains__(self, label: str) -> bool:
        '''Check if the ``label`` label satisfies the specification.

        Should be used as ``label in Spec``.
        '''
        if isinstance(self, collections.abc.Container):
            return label in self
        raise NotImplementedError


class SpecCountable(Spec):
    '''Parent class for static specification definitions.

    This a more narrow definition of `Spec`, for specifications that consist of
    discrete and countable choices between some values.

    .. automethod:: __len__
    '''

    def all(self) -> typing.Iterable[str]:
        '''Get all the possible labels this specification contains.'''
        if isinstance(self, typing.Iterable):
            # Default Implementation
            return (e for e in self)
        raise NotImplementedError

    def __len__(self) -> int:
        '''Count how many labels this specification contains.

        Should be used as ``len(SpecCountable)``.
        '''
        assert isinstance(self, collections.abc.Sized), f'{self.__class__.__name__} is not Sized'
        return len(self)


class StaticList(tuple, SpecCountable):
    '''Specifies a static list of labels, therefore a :py:class:`tuple` of `str`.

    The default must be explicitely given, either directly as ``default``, or
    indirectly as ``defaultIndex``. Either way is validated to verify the
    default is a valid label.

    Args:
        iterable: Values to construct the list.
        default: Default label. Optional
        defaultIndex: Index for the default label, in the ``iterable``. Optional.
    '''
    def __init__(self, iterable: typing.Iterable[str], *, default: typing.Optional[str] = None, defaultIndex: typing.Optional[int] = None):
        assert default is not None or defaultIndex is not None, f'{self.__class__.__name__}: Missing default label'
        super().__init__(*iterable)
        if default is None:
            assert defaultIndex is not None
            default = self[defaultIndex]
        if default not in self:
            raise ValueError(f'{default!r} not in list')
        # Set `Spec` parameters
        self.default = default


class StaticMap(SpecCountable, typing.Generic[smvT]):
    '''Specifies a static list of labels, and its corresponding values.

    The ``mapping`` parameter matches labels to values. This must be
    bi-injective, that is, there cannot be values corresponding to multiple
    labels.

    The default must be explicitely given.
    '''
    def __init__(self, mapping: typing.Mapping[str, smvT], *, defaultValue: typing.Optional[smvT] = None, defaultLabel: typing.Optional[str] = None):
        assert defaultValue is not None or defaultLabel is not None, f'{self.__class__.__name__}: Missing default'
        # Setup label -> value
        self.l2v: typing.Mapping[str, smvT] = mapping
        # Setup value -> label
        self.v2l: typing.Mapping[smvT, str] = {val: lbl for lbl, val in self.l2v.items()}
        if len(self.l2v) != len(self.v2l):
            raise ValueError('Mapping is not bi-injective')
        # Setup the "other" default
        if defaultValue is None:
            if defaultLabel not in self.l2v:
                raise ValueError(f'Label {defaultLabel!r} not in mapping')
            assert defaultLabel is not None
            defaultValue = self.l2v[defaultLabel]
        if defaultLabel is None:
            if defaultValue not in self.v2l:
                raise ValueError(f'Value {defaultValue!r} not in mapping')
            defaultLabel = self.v2l[defaultValue]
        assert defaultValue in self.v2l
        assert defaultLabel in self.l2v
        self.defaultLabel: str = defaultLabel
        self.defaultValue: smvT = defaultValue
        # Set `Spec` parameters
        self.default = defaultLabel

    def __contains__(self, label):
        return label in self.l2v

    def all(self):
        return self.l2v.keys()

    def __len__(self):
        return len(self.l2v)

    # Specific functions

    def value(self, label: str, default: smvT = None) -> smvT:
        '''Get the value corresponding to the given label.

        Wraps `dict.get`.
        '''
        if label in self.l2v:
            return self.l2v[label]
        else:
            assert default is not None, f'Invalid default value : {default!r}'
            return default

    def label(self, value: smvT, default: str = None) -> str:
        '''Get the label corresponding to the given value.

        Wraps `dict.get`.
        '''
        if value in self.v2l:
            return self.v2l[value]
        else:
            assert default is not None, f'Invalid default label: {default!r}'
            return default

    def hasValue(self, value: smvT) -> bool:
        '''Checks if the ``value`` statisfies the specification.

        This is the mirror image of `__contains__`, working on values.
        '''
        return value in self.v2l

    def allValues(self) -> typing.Iterable[smvT]:
        '''Get all possible values this specification contains.

        This is the mirror image of `all`, working on values.
        '''
        return self.v2l.keys()


def StaticMapLabels(fn: typing.Callable[[str], smvT], lst: typing.Sequence[str], *, defaultIndex: int = None, **kwargs) -> StaticMap:
    '''Turn a list of labels into a mapping, by applying a function to get the value.

    Wrapper for `StaticMap`.
    '''
    if defaultIndex is not None:
        kwargs['defaultLabel'] = lst[defaultIndex]
    return StaticMap({e: fn(e) for e in lst}, **kwargs)


def StaticMapValues(fn: typing.Callable[[smvT], str], lst: typing.Sequence[smvT], *, defaultIndex: int = None, **kwargs) -> StaticMap:
    '''Turn a list of values into a mapping, by applying a function to get the label.

    Wrapper for `StaticMap`.
    '''
    if defaultIndex is not None:
        kwargs['defaultValue'] = lst[defaultIndex]
    return StaticMap({fn(e): e for e in lst}, **kwargs)


# TODO: Include Range/Limit, for numbers
