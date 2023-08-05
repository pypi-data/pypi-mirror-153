'''Parsers for custom formats.

Reuse existing parsers as much as possible, don't reinvent wheels.
'''
import typing
from dataclasses import dataclass, field as dataclass_field
from collections import Counter
from html.parser import HTMLParser

from . import model


@dataclass
class LTML_Attributes:
    '''`LTML` attributes (see the main documentation).'''
    # Common
    data: typing.Mapping[str, str] = dataclass_field(default_factory=dict)
    # A
    href: typing.Optional[str] = None


class LTML(HTMLParser):
    '''Lite Text Markup Language parser.

    This is a small subset of HTML, to mark spans of text with metadata.

    The HTML subset is a very small piece of the whole HTML specification. See
    `TAGS_FULL` and `TAGS_SE` for the list of allowed tags. All text ouside the
    tags is included as untagged spans.

    The API is analogous to `HTMLParser <html.parser.HTMLParser>`, but supports
    only the LTML subset. After creating the parser object, feed it data using
    the `feed` function, and reuse the parser with new data by calling the
    `reset` function.

    .. note::

        Chunked `feed` usage is not supported (not even detected), please send
        the entire text at once, or at least break it at the tags.

    The output command list is available in `cmdlist`, it's a list of
    `model.TextElement`. The text element main tag is the LTML tag name (i.e
    for ``<span>TXT</span>``, the text element main tag is ``span``).

    Most attributes are ignored, but other have a special meaning and restrictions:

    - Tag ``a``, Attribute ``href``:
        A simple string, **NOT** a URL as in HTML.

        ``"a:href"`` is sent as ``a-$href`` text element tag. The value must
        not have any ``::`` anywhere.

    - Attributes ``data-*``:
        All the data attributes are collected in a dictionary, removing the
        ``data-`` prefix from the attribute name to get the key, and using the
        value as-is.

    For the tags in `TAGS_SIMPLE`, if there are no attributes, the tag is
    "simplified" by turning it into a regular text span. This is controlled by
    the "tag_simplify" argument.

    In addition to these tags, each tag type includes the so-called Automatic
    Counter tags (ACT). These are markers for each instance of each target
    type, including it's index position (starting at 0). The format is
    ``$tag::$index``. This is controlled by "tag_act" argument.

    .. note::

        As an example of the Automatic Counter tags, consider the following LTML::

            <span>1</span><span>2</span>

        This results in two elements with the following tags:

        - 1: ``span`` (Main Tag) ``span::0`` (ACT)
        - 2: ``span`` (Main Tag) ``span::1`` (ACT)

    Args:
        tag_simplify: Simplify some tags (`TAGS_SIMPLE`).
        tag_act: See the description for automatic counter tags
        documentation. Defaults to `True`.

    .. automethod:: feed

        Inherited from `HTMLParser.feed <html.parser.HTMLParser.feed>`
    '''
    TAGS_FULL = {
        'a',  # anchor
        'span',  # inline text
        'b', 'i',  # inline text: bold, italic
    }
    '''Full Tags.

    Like this: ``<tag>...</tag>``.
    '''
    TAGS_SIMPLE = {
        'span',
    }
    '''Simple Tags, that is, Full Tags that can be simplified.

    See the ``tag_simplify`` option.
    '''
    TAGS_SE = {
        'br',
    }
    '''Start/End Tags.

    Like this: ``<tag />``
    '''

    TAGS_MODEL = {
        'a': model.TextElementInline,
        'span': model.TextElementInline,
        'b': model.TextElementInline,
        'i': model.TextElementInline,
        'br': model.TextElement_br,
    }
    '''Mapping tag names to its corresponding model class.'''

    cmdlist: typing.List[model.TextElement]
    '''Output command list.'''

    def __init__(self, tag_act: bool = True, tag_simplify: bool = True):
        # Flags
        self._stags = tag_simplify
        self._act = tag_act
        # Asserts
        assert all(ts in self.TAGS_FULL for ts in self.TAGS_SIMPLE), 'All Simple Tags must be Full Tags'
        assert all(t in self.TAGS_MODEL for t in [*self.TAGS_FULL, *self.TAGS_SE]), 'All Tags must have a model'
        # Parent initialization
        # - Should call `self.reset()` automatically
        super().__init__()

    def reset(self):
        '''
        Reset the instance. Loses all unprocessed data.

        This is called when instancing the parser.

        ---

        Extended from `HTMLParser.reset <html.parser.HTMLParser.reset>`
        '''
        super().reset()
        # Automatic Counter Tags
        self._tctag: Counter = Counter()
        # Current Tag tracker
        # TODO: Make this a tag stack ???
        self._ctag: typing.Optional[str] = None
        self._ctag_attrs: typing.Optional[LTML_Attributes] = None
        # Output
        self.cmdlist = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.TAGS_FULL:
            raise ValueError(f'Invalid LTML: full tag {tag}')
        elif self._ctag is not None:
            raise ValueError(f'Nested tags are unsupported: {self._ctag} in {tag}')
        else:
            # Correct
            self._ctag = tag
            data = {}
            for aname, avalue in attrs:
                data_prefix = 'data-'
                if aname.startswith(data_prefix):
                    # Python 3.9: `str.removeprefix`
                    data[aname[len(data_prefix):]] = avalue
            attributes = {}
            if tag == 'a':
                href = None
                for aname, avalue in attrs:
                    if aname == 'href':
                        assert href is None, 'Repeated "a:href" attribute'
                        href = avalue
                        assert '::' not in href, f'Invalid "a:href": {href}'
                attributes['href'] = href
            self._ctag_attrs = LTML_Attributes(data=data, **attributes)
            self._tctag[tag] += 1  # ACT

    def handle_startendtag(self, tag, attrs):
        if tag not in self.TAGS_SE:
            raise ValueError(f'Invalid LTML: tag se {tag}')
        else:
            what = self.TAGS_MODEL[tag]()
            assert what is not None
            self.cmdlist.append(what)

    def handle_endtag(self, tag):
        if self._ctag == tag:
            self._ctag = None
            self._ctag_attrs = None
        else:
            raise ValueError(f'Unbalanced start/end tags: {self._ctag}/{tag}')

    def handle_data(self, string: str):
        # TODO: Support chunked `feed`, do this on `handle_endtag`
        main_tag = self._ctag
        tags = []
        data: typing.Mapping[str, str] = {}
        if main_tag:
            assert self._ctag_attrs is not None
            data = self._ctag_attrs.data
            if self._ctag_attrs.href:
                tags.append(f'{self._ctag}-{self._ctag_attrs.href}')
            if self._act:  # ACT
                tags.append('%s::%d' % (main_tag, self._tctag[self._ctag] - 1))  # Start counting at 0
            tag_model = self.TAGS_MODEL[main_tag]
        else:
            tag_model = model.TextElementInline
        if self._stags and main_tag in self.TAGS_SIMPLE and len(tags) == 0 and len(data) == 0:
            # Simplify simple tags
            main_tag = None
        tag_obj = tag_model(string,
                            tag=main_tag,
                            tags=tags if len(tags) > 0 else None,
                            data=data)
        self.cmdlist.append(tag_obj)

    def parse(self, ltml: str) -> typing.Sequence[model.TextElement]:
        '''Helper function to parse a standalone string.

        - `reset` the parser
        - `feed` "ltml" to the parser
        - Return the output `cmdlist`
        '''
        self.reset()
        self.feed(ltml)
        return self.cmdlist


def parse_LTML(ltml: str, __parser: LTML = LTML()) -> typing.Sequence[model.TextElement]:
    '''Parse Lite Text Markup Language using the default settings.

    This always reuses the same parser, so it should be fast.

    Args:
        ltml: The string to parse.

    See Also:
        See `LTML` for further advanced usage. In particular, see `LTML.parse`.
    '''
    return __parser.parse(ltml)
