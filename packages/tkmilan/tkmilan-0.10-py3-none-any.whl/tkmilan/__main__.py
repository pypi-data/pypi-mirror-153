import logging

from pathlib import Path
from functools import wraps
from datetime import datetime
import random

import tkinter as tk
from . import MODULES_VERBOSE
from . import RootWindow, FrameUnlabelled, FrameLabelled, FrameStateful, FramePaned, Notebook, NotebookUniform, ScrolledWidget
from . import Button, Checkbox, Entry, Label, LabelStateful, Listbox, Combobox, ComboboxMap, EntryMultiline, Tree, ListboxControl
from . import var, spec, fn
from .model import CP, BindingGlobal, Timeout, TimeoutIdle, FileType, FileTypes


logger = logging.getLogger(__name__)


class LuftBaloons(FrameUnlabelled):
    layout = 'xE'

    def setup_widgets(self, howmany=16 - 3):
        widgets = {}
        for widx in range(howmany):
            idx = 'lb:%d' % widx
            widget = Checkbox(self, label='%02d' % widx)
            widget.trace(self.onClick_lb, idx=idx)
            widgets[idx] = widget
        return widgets

    def onClick_lb(self, vobj, etype, *, idx):
        pass
        # logger.debug('Clicked on "%s" @ %s:%s', idx, vobj, etype)
        # logger.debug('- State: %r', vobj.get())


class ListFrame_Inner(FrameStateful):
    wstate_single = 'e'

    def __init__(self, *args, label, **kwargs):
        super().__init__(*args, label=label, labelInner=label, **kwargs)

    def setup_widgets(self, labelInner):
        self.lbl = Label(self, label=f'Label: {labelInner}')
        self.e = Entry(self)  # label=f'Entry: {labelInner}'


class ListFrame_Outer(FrameStateful):
    label = 'Outer Frame'
    layout = 'R2,1'

    def setup_widgets(self, *, cbox1):
        self.left = ListFrame_Inner(self, label='Left',
                                    cvariableDefault=True)
        self.right = ListFrame_Inner(self, label='Right',
                                     cvariableDefault=False)
        self.bottom = ListFrame_Inner(self, label='Bottom',
                                      cvariable=cbox1)


class ListFrame_Lists(FramePaned):
    layout = tk.HORIZONTAL

    def setup_widgets(self, *, vLst):
        self.lstS = Listbox(self,
                            height=6,
                            variable=vLst,
                            selectable=True)  # Selectable
        self.lstRO = Listbox(self, label='Unselectable',
                             maxHeight=3, expand=True,  # Varying Height, Expanded  # N/A on FramePaned
                             variable=vLst,
                             selectable=False,
                             style=Listbox.Style(altbg=True),
                             )  # Not Selectable


class ListFrame(FrameLabelled):
    layout = 'R3,1,2,1'

    def setup_widgets(self, *, cbox1):
        i_choices: spec.StaticMap[int] = spec.StaticMapValues(lambda i: 'I%d' % i, range(10), defaultValue=7)

        self.bFill = Button(self, label='Fill Me!')
        self.lPanes = Label(self, label='↓ Drag Separator ↓')
        self.bCheck = Button(self, label='Check')

        vLst = self.var(var.StringList, name='lst')
        self.cLst = ListFrame_Lists(self, vLst=vLst)

        self.bChoice = Button(self, label='CB=2')
        self.i_choice = ComboboxMap(self, values=i_choices)  # label='CB(int)'

        self.rstateful = ListFrame_Outer(self, labelAnchor=CP.N,
                                         cbox1=cbox1)

    def setup_layout(self, layout):
        fn.configure(self, self.cLst, rows=True, weight=0)

    def setup_defaults(self):
        self.fill_lst()
        # Events
        self.bFill.onClick = self.fill_lst
        self.bCheck.onClick = self.check_lst
        self.bChoice.onClick = self.i_choice.eSetValue(2)

        self.i_choice.trace(self.onChosen, spec=self.i_choice.specValues)

        BindingGlobal(self.bChoice, '<F1>', self.globalHelp,
                      immediate=True, description='Nothing, just showing the event object')

    def setup_adefaults(self):
        # Why not verify some invariants?
        assert self.wroot_search() == self.wroot, 'Invalid Root calculation'

    def fill_lst(self):
        ctime = str(datetime.now())
        self.gvar('lst').set(['A', 'List', 'Of', 'Letters', '@', ctime])

    def check_lst(self):
        sel = self.cLst.lstS.wselection()
        logger.debug('S: %r', sel)

    def onChosen(self, variable, etype, *, spec):
        logger.debug('V: %r', variable)
        label = variable.get()
        logger.debug('   Label: %s[%r]', label, spec.value(label))

    def globalHelp(self, event=None):
        if event:
            logger.debug('Event: %r', event)


class UpstreamBool(FrameLabelled):
    layout = 'x1N'  # Bottom-Up
    # Comment the following line to change the state
    isNoneable = False  # Don't skip this widget, even when its state is `None`

    def setup_widgets(self, what_bool):
        self.bNoOp = Button(self, label='noop')
        self.u_bool = Checkbox(self, variable=what_bool, label='Upstream "bool"')
        self.bNoOp_Big = Button(self, label='No Operation')


class NB_Child_Simple(FrameUnlabelled):
    layout = 'Rx,1'
    wstate_single = 'e'

    def setup_widgets(self, label):
        w = {}
        for n in range(5):
            w[f'n{n}'] = Label(self, label=f'{n}: {label}')
        w['e'] = LabelStateful(self)  # label=f'LS #{n}'
        return w

    def setup_defaults(self):
        self.widgets['e'].onClick = self.onClick_E

    def setup_adefaults(self):
        self.widgets['e'].wstate = 'Clickable LabelStateful'

    def onClick_E(self, event=None):
        w = self.widgets['e']
        state = w.wstate
        if not state.endswith(' T'):
            state += ' T'
        else:
            state = state[:-2]
        w.wstate = state


class NB_Child_Complex(NotebookUniform):
    tabids = {f'TC{d}': f'Tab Complex {d}' for d in range(5)}

    def setup_tab(self, tid: str, tname: str):
        return NB_Child_Simple(self, label=tid)


class NB_Child_Timeout(FrameLabelled):
    label = 'Timeout'

    def __init__(self, *args, **kwargs):
        self.t = Timeout(self, self.onTimeout, 1000, immediate=False)
        super().__init__(*args, **kwargs)

    def setup_widgets(self):
        self.cScheduled = Checkbox(self, label='Scheduled?', readonly=True)
        self.cTriggered = Checkbox(self, label='Triggered?', readonly=True)
        self.bToggle = Button(self, label='Toggle\nasync')

        self.bToggle.onClick = self.onToggle

    def setup_defaults(self):
        self.update()

    def update(self):
        self.cScheduled.wstate = self.t.isScheduled()
        self.cTriggered.wstate = self.t.isTriggered()

    def onToggle(self):
        self.t.toggle()
        self.update()

    def onTimeout(self):
        logger.debug('Timeout!')
        self.update()


class NB_Child_Timeout_Delay(FrameLabelled):
    label = 'Timeout (Delayed)'

    def __init__(self, *args, **kwargs):
        self.t = Timeout(self, self.onTimeout, 1000, immediate=False)
        super().__init__(*args, **kwargs)

    def setup_widgets(self):
        self.cScheduled = Checkbox(self, label='Scheduled?', readonly=True)
        self.cTriggered = Checkbox(self, label='Triggered?', readonly=True)
        self.bToggle = Button(self, label='  Toggle\nasync-ish')

        self.bToggle.onClick = self.onToggle

    def setup_defaults(self):
        self.update()

    def update(self):
        self.cScheduled.wstate = self.t.isScheduled()
        self.cTriggered.wstate = self.t.isTriggered()

    def onToggle(self):
        self.t.toggle()
        self.update()

    def onTimeout(self):
        logger.debug('Timeout!')
        self.update()
        logger.debug('Delay ...')
        self.after(1000)
        logger.debug('... Done!')


class NB_Child_TimeoutIdle_Delay(FrameLabelled):
    label = 'TimeoutIdle (Delayed)'

    def __init__(self, *args, **kwargs):
        self.t = TimeoutIdle(self, self.onTimeout, immediate=False)
        self.tsleep = TimeoutIdle(self, lambda: self.after(1000), immediate=False)  # Pretend this is a long calculation
        super().__init__(*args, **kwargs)

    def setup_widgets(self):
        self.cScheduled = Checkbox(self, label='Scheduled?', readonly=True)
        self.cTriggered = Checkbox(self, label='Triggered?', readonly=True)
        self.bToggle = Button(self, label='Toggle\n sync')

        self.bToggle.onClick = self.onToggle

    def setup_defaults(self):
        self.update()

    def update(self):
        self.cScheduled.wstate = self.t.isScheduled()
        self.cTriggered.wstate = self.t.isTriggered()

    def onToggle(self):
        ts = [self.tsleep, self.t]
        # (un)schedule both timeouts in tandem
        if self.t.isScheduled():
            for t in ts:
                t.unschedule()
        else:
            for t in ts:
                t.schedule()
        self.update()

    def onTimeout(self):
        logger.debug('TimeoutIdle!')
        self.update()


class NB_Child_TimeoutIdle_Chain(FrameLabelled):
    label = 'TimeoutIdle (Chained)'

    def __init__(self, *args, **kwargs):
        self.tsleep = TimeoutIdle(self, self.onTimeoutSleep, immediate=False)
        self.t = TimeoutIdle(self, self.onTimeout, immediate=False)
        super().__init__(*args, **kwargs)

    def setup_widgets(self):
        self.cScheduled = Checkbox(self, label='Scheduled?', readonly=True)
        self.cTriggered = Checkbox(self, label='Triggered?', readonly=True)
        self.bToggle = Button(self, label='Toggle\n sync')

        self.bToggle.onClick = self.onToggle

    def setup_defaults(self):
        self.update()

    def update(self):
        self.cScheduled.wstate = self.t.isScheduled()
        self.cTriggered.wstate = self.t.isTriggered()

    def onToggle(self):
        ts = [self.tsleep, self.t]
        # (un)schedule both timeouts in tandem
        if self.t.isScheduled():
            for t in ts:
                t.unschedule()
        else:
            for t in ts:
                t.schedule()
        self.update()

    def onTimeoutSleep(self):
        logger.debug('Chain Delay ...')
        self.after(1000)
        logger.debug('... Done!')
        self.t.schedule()
        self.update()

    def onTimeout(self):
        logger.debug('TimeoutIdle!')
        self.update()


class NB_Child_Timeouts(FrameUnlabelled):
    # layout = tk.HORIZONTAL

    def setup_widgets(self):
        self.timeout = NB_Child_Timeout(self)
        self.timeout_d = NB_Child_Timeout_Delay(self)
        self.timeout_idle_d = NB_Child_TimeoutIdle_Delay(self)
        self.timeout_idle_c = NB_Child_TimeoutIdle_Chain(self)


class NB_Child_Dialog(FrameUnlabelled):
    layout = 'Rx,1'
    wstate_single = 'txt'

    def setup_widgets(self):
        self.ds = Button(self, label='D S')
        self.dl = Button(self, label='D L')
        self.fs = Button(self, label='F S')
        self.fl = Button(self, label='F L')
        self.flc = Button(self, label='F L(py)')
        self.fsc = Button(self, label='F S(py)')
        self.txt = LabelStateful(self)

        self.ds.onClick = self.click(fn.ask_directory_save, self, title='Directory @ .',
                                     initialDirectory=Path('.'))
        self.dl.onClick = self.click(fn.ask_directory_load, self, title='Directory @ Home',
                                     initialDirectory=Path('~').expanduser())
        self.fs.onClick = self.click(fn.ask_file_save, self, title='File @ ..',
                                     initialDirectory=Path('..'))
        self.fl.onClick = self.click(fn.ask_file_load, self, title='File @ /',
                                     initialDirectory=Path('/'))
        self.fsc.onClick = self.click(self.customFile, fn.ask_file_save)
        self.flc.onClick = self.click(self.customFile, fn.ask_file_load)

    def click(self, fn, *args, **kwargs):
        @wraps(fn)
        def wrapped():
            self.txt.wstate = ''
            ret = fn(*args, **kwargs)
            ret_loc = ret.resolve() if ret else ret
            ret_exists = str(ret.exists()) if ret else 'N/A'
            self.txt.wstate = f'{ret_loc}\nExists: {ret_exists}'
        return wrapped

    def customFile(self, function):
        return function(self, title='Custom Python Files @ .',
                        initialDirectory=Path('.'),
                        includeAll=False, filetypes=FileTypes({
                            'Python': FileType('py'),
                            'TOML': FileType('toml'),
                        }))


class NB_Child_Scrollbars(FrameUnlabelled):
    layout = 'R2,x'
    wstate_single = 'slst'

    def setup_widgets(self):
        self.randomize = Button(self, label='Randomize List Size')
        self.setscrolls = Button(self, label='Toggle Scrollbars')

        vSlist = self.var(var.StringList, name='slst')
        self.sbL = ScrolledWidget(self, Listbox,
                                  scrollHorizontal=None, scrollVertical=None,  # Auto (default)
                                  height=5, variable=vSlist)
        self.sbC = ScrolledWidget(self, Listbox,
                                  scrollHorizontal=False, scrollVertical=False,  # Manual, disabled
                                  height=5, variable=vSlist)
        self.sbR = ScrolledWidget(self, Listbox,
                                  scrollHorizontal=True, scrollVertical=True,  # Manual, enabled
                                  height=5, variable=vSlist)

        self.randomize.onClick = self.onRandom
        self.setscrolls.onClick = self.onShowAll

    def setup_adefaults(self):
        self.onRandom()

    def onRandom(self, event=None):
        randomsize = random.randint(5, 30)  # Allow an opportunity for no vertical scrollbar
        self.gvar('slst').set([f'Index {i:03}' for i in range(1, randomsize + 1)])

    def onShowAll(self, event=None):
        # sbL: Auto, Set True
        self.sbL.set_scroll_state(True, True)
        # sbC: Manual, Set True (no-op)
        self.sbC.set_scroll_state(True, True)
        # sbR: Manual, Set Reversed
        self.sbR.set_scroll_state(*(not b for b in self.sbR.get_scroll_state()))


class NB_Child_ListboxSet(FrameUnlabelled):
    layout = tk.HORIZONTAL

    def setup_widgets(self):
        ls_all = spec.StaticList((f'String {idx:02}' for idx in range(1, 20 + 1)), defaultIndex=0)

        ls_selected = random.sample(list(ls_all.all()), k=5)
        self.left = ListboxControl(self,
                                   selAll=ls_all)
        self.right = ListboxControl(self, layout='c1,x', label='Full Control',
                                    selAll=ls_all, selList=ls_selected,
                                    buttonOne=False, buttonAll=True, buttonOrder=True)

    def setup_defaults(self):
        self.left.onAddAll()


class NB(Notebook):
    def setup_tabs(self):
        logger.debug('» %r', self)
        # TODO: Test images, etc.

        return {
            'sb': Notebook.Tab('Scrollbars', NB_Child_Scrollbars(self)),
            'tt': Notebook.Tab('Timeouts', NB_Child_Timeouts(self),
                               image=self.wimage('info-s16'), labelPosition=CP.E),  # Default labelPosition
            'td': Notebook.Tab('Dialogues', NB_Child_Dialog(self),
                               image=self.wimage('info-msgbox-s16'), labelPosition=True),  # Only image
            'tc': Notebook.Tab('Tab Complex', NB_Child_Complex(self),
                               image=self.wimage('info-s16'), labelPosition=CP.W),  # "Reverse" labelPosition
            't1': Notebook.Tab('Tab 1', NB_Child_Simple(self, label='Tab 1')),
            't2': Notebook.Tab('Tab 2', NB_Child_Simple(self, label='Tab 2')),
            'c:lc': Notebook.Tab('Complex ListboxControl', NB_Child_ListboxSet(self)),
        }

    def setup_adefaults(self):
        self.wselect('c:lc')


class TextEditor(FrameStateful):
    label = 'LTML'
    layout = 'Rx,1'
    wstate_single = 'txt'

    def setup_widgets(self):
        self.bTxtClean = Button(self, label='Clean TXT')
        self.bTxtReset = Button(self, label='Reset TXT')
        self.bTxtSet = Button(self, label='Set TXT')
        self.txt = ScrolledWidget(self, EntryMultiline,
                                  setgrid=False)
        # Setup events
        self.bTxtClean.onClick = self.txt.style_reset
        self.bTxtReset.onClick = self.txt_reset
        self.bTxtSet.onClick = self.txt_set
        self.txt.onClickTag = self.txt_clicked

    def setup_layout(self, layout):
        self.txt.grid(sticky=tk.NS)

    def setup_defaults(self):
        self.rowconfigure(0, weight=0)  # Buttons

    def setup_adefaults(self):
        self.txt_set(cnt=20)

    def txt_reset(self, event=None):
        self.txt.wstate = ''

    def txt_set(self, event=None, *, cnt=None):
        texts = []
        if cnt is None:
            cnt = 20 + random.choice(range(-10, 5))
        for r in range(cnt):
            texts.append(f'<b>Line</b> <i>{"%02d" % r}</i>/{cnt} ')
            if r % 2 == 0:
                _txt = 'EVEN'
            else:
                _txt = '    '
            texts.append(f'<a>[{_txt}]</a>')
            texts.append('<br/>')
            if r % 5 == 0:
                texts.append('<br/>')
        self.txt.wstate = ''.join(texts)

    def txt_clicked(self, tag, tag_id, tags_other):
        logger.debug(f'Clicked on {tag} {tag_id} :: {tags_other}')


class TreeExample(Tree):
    pass


class ComboboxCB(Combobox):
    pass


class RW(RootWindow):
    def setup_widgets(self):
        choices = spec.StaticList(('Choice %d' % n for n in range(5)), defaultIndex=3)
        vc = self.var(var.Boolean, name='bool', value=True)

        self.b1 = Button(self, label='B1')
        self.c1 = Checkbox(self, label='Checkbox1')
        self.bE1 = Button(self, label='Set "example"')
        self.b2 = Button(self, label='Debug')
        self.c2ro = Checkbox(self, label='RO "bool"', readonly=True, variable=vc)
        self.c2rw = Checkbox(self, label='RW "bool"', readonly=False, variable=vc)
        self.e1 = Entry(self)  # label='Entry1'
        self.lbs = LuftBaloons(self)
        self.ubox = UpstreamBool(self, label='Upstream', labelAnchor=CP.S,
                                 what_bool=vc)
        self.choice = ComboboxCB(self, values=choices)  # label='CB'
        self.choice_reset = Button(self, label='CB: Set Last')
        self.lf = ListFrame(self, label='List Box', cbox1=self.c1.variable)

        self.txt = TextEditor(self)
        self.nb = NB(self)
        self.arbre = TreeExample(self, label='Label', columns={
            'number': 'Number',
        })

        # Setup events
        self.b1.onClick = self.c1.toggle
        self.bE1.onClick = self.ask_contents
        self.b2.onClick = self.debug
        self.choice_reset.onClick = self.choice.eSet(choices[-1])

    def setup_defaults(self):
        BindingGlobal(self, '<F4>', lambda e: self.debug(),
                      immediate=True, description='Debug')

    def setup_adefaults(self):
        logger.debug('Setup arbre state:')
        self.arbre.wstate = [
            Tree.Element('First', ['1'], image=self.wimage('warning-s16')),
            Tree.Element('Second', ['2'], image=self.wimage('warning-s16'), children=[
                Tree.Element('Second.One', ['21'], image=self.wimage('error-s16')),
            ]),
            Tree.Element('Third', ['3'], image=self.wimage('warning-s16'), children=[
                Tree.Element('Third.One', ['31']),
                Tree.Element('Third.Two', ['32'], image=self.wimage('error-s16'), children=[
                    Tree.Element('Third.Two.One', ['321']),
                    Tree.Element('Third.Two.Two', ['322'], image=self.wimage('warning-s16')),
                    Tree.Element('Third.Two.3', ['323'], image=self.wimage('error-s16')),
                ]),
                Tree.Element('Third.Tee', ['33']),
            ]),
            Tree.Element('Tenth', ['10'], image=self.wimage('warning-s16')),
        ]
        logger.debug('Global Bindings:')
        for bname, B in self._bindings_global.items():
            logger.debug('- %s: %s%s', bname, '' if B else '[Disabled] ', B.description)

    def ask_contents(self):
        string = tk.simpledialog.askstring('Set Contents', f'Set the "{self.e1.label}" contents')
        if string is not None:
            self.e1.wstate = string

    def debug(self):
        from pprint import pformat
        logging.info('=> State @ %s[%r]', self, self)
        for line in pformat(self.wstate_get()).splitlines():  # No `.wstate` for better tracebacks
            logging.info('%s', line)
        # logging.info('=> State @ ubox')
        # for line in pformat(self.ubox.wstate).splitlines():
        #     logging.info('%s', line)
        # logging.info('=> State @ lf.cLst')
        # for line in pformat(self.lf.cLst.wstate).splitlines():
        #     logging.info('%s', line)
        # logging.info('=> State @ nb[c:lc]')
        # for line in pformat(self.nb.wtab('c:lc').wstate).splitlines():
        #     logging.info('%s', line)
        logging.info('=> State Set')
        new = self.wstate
        for b in ('0', '12'):
            new['lbs'][f'lb:{b}'] = not new['lbs'][f'lb:{b}']
        self.wstate = new
        logging.info('=> GUI States')
        logging.info('   GUI State @ %s[%r]', self, self)
        for line in pformat(self.gstate).splitlines():
            pass  # logging.info('  %s', line)
        logging.info('   GUI State @ c2ro')
        for line in pformat(self.c2ro.gstate).splitlines():
            pass  # logging.info('  %s', line)
        logging.info('   GUI State @ c2rw')
        for line in pformat(self.c2rw.gstate).splitlines():
            pass  # logging.info('  %s', line)
        logging.info('   GUI State @ choice')
        for line in pformat(self.choice.gstate).splitlines():
            pass  # logging.info('  %s', line)
        logging.info('   GUI State @ e1')
        for line in pformat(self.e1.gstate).splitlines():
            pass  # logging.info('  %s', line)
        logging.info('   GUI State @ txt.txt')
        for line in pformat(self.txt.txt.gstate).splitlines():
            pass  # logging.info('  %s', line)
        # self.set_gui_state(enabled=True, valid=True)  # Invalid Target
        logging.info('=> NB')
        for tn, ti in self.nb.wtabs.items():
            logging.info(f'   | {tn}: {ti}')


def entrypoint():
    import argparse
    parser = argparse.ArgumentParser(description='Showcase for tkmilan module')

    # ./showcase-images
    default_images = Path(__file__).parent / 'showcase-images'

    # parser.add_argument('--version', action='version', version=PROJECT_VERSION)
    parser.add_argument('-v', '--verbose', dest='loglevel',
                        action='store_const', const=logging.DEBUG, default=logging.INFO,
                        help='Add more details to the standard error log')
    parser.add_argument('--debug', action='store_true',
                        help=argparse.SUPPRESS)
    parser.add_argument('--images', type=Path, default=default_images,
                        help='Image Folder to Load. Defaults to %(default)s')
    parser.add_argument('--no-images', action='store_const',
                        dest='images', const=None,
                        help='Do not load any images')
    args = parser.parse_args()

    # Logs
    logs_fmt = '%(levelname)-5.5s %(name)s@%(funcName)s| %(message)s'
    try:
        import coloredlogs  # type: ignore
        coloredlogs.install(level=args.loglevel, fmt=logs_fmt)
    except ImportError:
        logging.basicConfig(level=args.loglevel, format=logs_fmt)
    logging.captureWarnings(True)
    # # Silence spammy modules, even in verbose mode
    if not args.debug and args.loglevel == logging.DEBUG:
        for dmodule in MODULES_VERBOSE:
            logging.getLogger(f'{__package__}.{dmodule}').setLevel(logging.INFO)

    # Widget Tester / Showcase
    r = RW(imgfolder=args.images)
    logger.debug('Screen Size: %r', r.size_screen)
    logger.debug('         /2: %r', r.size_screen.reduce(2))
    r.mainloop()


if __name__ == '__main__':
    import sys
    sys.exit(entrypoint() or 0)
