def enhanced_dir(arg, categorize=True, show_types=False, checks=False, collections_abc_list=False):
    from collections import defaultdict
    if not categorize:
        return_list = []
    passed = defaultdict(lambda: defaultdict(set))
    failed = defaultdict(set)
    passed_ = defaultdict(lambda: defaultdict(set))
    failed_ = defaultdict(lambda: defaultdict(set))
    x = arg

    for method in (set(dir(arg)) | (set(dir(type(x))) - set(dir(x)))):
        try:
            type_ = type(eval(f'x.{method}'))
        except:
            failed[f'{arg}'].add(method)
            continue
        try:
            qualname = eval(f'x.{method}.__qualname__')
            qualname = qualname.split('.')
            passed[f'{arg}'][qualname[0]].add(qualname[1])
            passed_[f'{arg}'][type_].add(qualname[1])
        except:
            failed[f'{arg}'].add(method)
            failed_[f'{arg}'][type_].add(method)
    if categorize:
        return_list = [{'passed': passed}, {'failed': failed}]
    if show_types:
        return_list.extend(({'passed_types': passed_}, {'failed_types': failed_}))
    if collections_abc_list:
        import collections.abc
        collections_abc = {*()}
        for i in dir(collections.abc):
            try:
                if isinstance(arg, eval(f'collections.abc.{i}')):
                    collections_abc.add(i)
            except:
                pass
        return_list.append([collections_abc])
    if checks:
        checks_ = {}
        try:
            class A(x):
                pass

            checks_['inheritable'] = True
        except:
            checks_['inheritable'] = False

        try:
            a = defaultdict(arg)
            checks_['defaultdict_arg'] = True
        except:
            checks_['defaultdict_arg'] = False

        try:
            d = {arg: 1}
            checks_['dict_key'] = True
        except:
            checks_['dict_key'] = False

        try:
            for i in arg:
                pass
            checks_['iterable'] = True
        except:
            checks_['iterable'] = False
        return_list.append([checks_])

    return return_list


def two_way(operation, opposite=False, iterators=False):
    import warnings
    warnings.filterwarnings("ignore")
    import re, keyword
    from collections import defaultdict, Counter, OrderedDict, namedtuple
    from decimal import Decimal
    from fractions import Fraction
    failed = defaultdict(set)
    succeeded = defaultdict(set)
    invalid = 'StopIteration|StopAsyncIteration|Error|Warning|Exception|Exit|Interrupt|__|ipython|display|execfile' \
              '|dreload|help|license|open|get_ipython|credits|runfile|copyright|breakpoint|input|print'
    bytes_iterator = "(iter(b''))"
    bytearray_iterator = "(iter(bytearray()))"
    dict_keyiterator = "(iter({}.keys()))"
    dict_valueiterator = "(iter({}.values()))"
    dict_itemiterator = "(iter({}.items()))"
    list_iterator = "(iter([]))"
    list_reverseiterator = "(iter(reversed([])))"
    range_iterator = "(iter(range(0)))"
    set_iterator = "(iter(set()))"
    str_iterator = "(iter(''))"
    tuple_iterator = "(iter(()))"
    zip_iterator = "(iter(zip()))"
    line_iterator = "(lambda x: 1).__code__.co_lines"
    positions_iterator = "(lambda x: 1).__code__.co_positions"
    mappingproxy = '(type.__dict__)'
    generator = '((lambda: (yield))())'
    ## views ##
    dict_keys = 'dict().keys'
    dict_values = 'dict().values'
    dict_items = 'dict().items'
    counter = 'Counter'
    ordered_dict = 'OrderedDict'
    default_dict = 'defaultdict'
    named_tuple = 'namedtuple'
    decim = 'Decimal'
    fract = 'Fraction'
    y = [(dict_keys, 13), (dict_values, 14), (dict_items, 15), (mappingproxy, 16),
         (generator, 17), (counter, 18), (ordered_dict, 19), (default_dict, 20), (named_tuple, 21), (decim, 22),
         (fract, 23)]
    if iterators:
        y += [(bytes_iterator, 0), (bytearray_iterator, 1), (dict_keyiterator, 2),
              (dict_valueiterator, 3), (dict_itemiterator, 4), (list_iterator, 5),
              (list_reverseiterator, 6), (range_iterator, 7),
              (set_iterator, 9), (str_iterator, 10), (tuple_iterator, 11), (zip_iterator, 12)]

    for a, i in list(keyword.__builtins__.items()) + y:
        if not re.search(invalid, str(a)):
            for b, j in list(keyword.__builtins__.items()) + y:
                if not re.search(invalid, b):
                    try:
                        x = eval(f'{a}() {operation} {b}()')
                        if opposite:
                            succeeded[f'{b}()'].add(f'{a}()')
                        else:
                            succeeded[f'{a}()'].add(f'{b}()')
                    except:
                        failed[a].add(b)
                    try:
                        x = eval(f'{a}() {operation} {b}')
                        if opposite:
                            succeeded[b].add(f'{a}()')
                        else:
                            succeeded[f'{a}()'].add(b)
                    except:
                        failed[a].add(b)
                    try:
                        x = eval(f'{a} {operation} {b}()')
                        if opposite:
                            succeeded[f'{b}()'].add(a)
                        else:
                            succeeded[a].add(f'{b}()')
                    except:
                        failed[a].add(b)
                    try:
                        x = eval(f'{a} {operation} {b}')
                        if opposite:
                            succeeded[b].add(a)
                        else:
                            succeeded[a].add(b)
                    except:
                        failed[a].add(b)
    return [{'succeeded': succeeded}]


def operator_check(left_argument, right_argument, show_failed=False):
    import warnings
    warnings.filterwarnings("ignore")
    failed = set()
    succeeded = set()
    operators = [':', ',', ';', '+', '-', '*', '/', '|', '&', '<', '>', '=',
                 '.', '%', '==', '!=', '<=', '>=', '~', '^', '<<',
                 '>>', '**', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=',
                 '<<=', '>>=', '**=', '//', '//=', '@', '@=', '->', '...',
                 ':=', 'and', 'or', 'in', 'is']

    for operator in operators:
        try:
            x = eval(f'left_argument {operator} right_argument')
            succeeded.add(operator)
        except:
            failed.add(operator)
    returned_dictionary = {'succeeded': succeeded}
    if show_failed:
        returned_dictionary['failed'] = failed
    return returned_dictionary
