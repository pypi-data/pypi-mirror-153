from colorama import Fore, Style

def get_kwarg(key_name, default_val=False, value_type=None, **kwargs):
    kwargs = keys_to_lower(kwargs)
    if isinstance(key_name, list) is False:
        key_name = [key_name]

    for name in key_name:
        # generate basic variations of the name
        varis = _gen_variations(name)
        for v_name in varis:
            if v_name in kwargs:
                if value_type is not None:
                    if isinstance(kwargs[v_name], value_type) is True:
                        return kwargs[v_name]
                else:
                    return kwargs[v_name]
    return default_val


def _gen_variations(string):
    string = str(string)
    varis = []
    lower = string.lower()
    upper = string.upper()
    snake_case = lower.replace(" ", "_")
    screaming_snake_case = upper.replace(" ", "_")
    varis.append(lower)
    varis.append(upper)
    varis.append(snake_case)
    varis.append(screaming_snake_case)
    return varis


def keys_to_lower(dictionary):
    '''
        Converts all keys in a dictionary to lowercase.
    '''
    return {k.lower(): v for k, v in dictionary.items()}

# pylint: disable=too-many-locals
# pylint: disable=too-many-branches


def get_unique_keys(obj, **kwargs):
    '''
        Gets all unique keys in the object provided.

        @param {dict|list} obj - The object or list to search for keys within.
        @param {boolean} [**sort_list=True] - Sort the list alphabetically.
        @param {boolean} [**case_sensitive=True] - If True the case of the key is ignored.
        @param {boolean} [**force_lowercase=True] - Convert all keys to lowercase.
        @param {boolean} [**recursive=True] - Recurse into nested objects to find keys.
        @param {int} [**max_depth=500] - The maximum recursions it is allowed to make.
        @return {list} A list of unique keys from the object, if none are found the list is empty.
        @function get_unique_keys
    '''

    __current_depth = get_kwarg(['__current_depth'], 0, int, **kwargs)
    sort_list = get_kwarg(['sort_list'], False, bool, **kwargs)
    case_sensitive = get_kwarg(['case_sensitive'], True, bool, **kwargs)
    force_lowercase = get_kwarg(['force_lowercase'], True, bool, **kwargs)
    recursive = get_kwarg(['recursive'], True, bool, **kwargs)
    max_depth = get_kwarg(['max_depth'], 500, int, **kwargs)
    kwargs['__current_depth'] = __current_depth + 1

    keys = []

    if recursive is True and __current_depth < max_depth:
        if isinstance(obj, (list, tuple, set)):
            for element in obj:
                if isinstance(element, (list, dict)):
                    keys = keys + get_unique_keys(element, **kwargs)

    if isinstance(obj, dict):
        keys = list(obj.keys())

        if recursive is True and __current_depth < max_depth:
            # pylint: disable=unused-variable
            for k, value in obj.items():
                # find nested objects
                if isinstance(value, (list, dict, tuple, set)):
                    keys = keys + get_unique_keys(value, **kwargs)

    if case_sensitive is True:
        output = []
        lkkeys = []
        for key in keys:
            low_key = key.lower()
            if low_key not in lkkeys:
                output.append(key)
                lkkeys.append(low_key)
        keys = output

    if force_lowercase is True:
        keys = [x.lower() for x in keys]

    keys = list(set(keys))

    if sort_list is True:
        keys = sorted(keys, key=lambda x: int("".join([i for i in x if i.isdigit()])))
    return keys

def find_list_diff(list_one, list_two):
    '''
        find elements in list_one that do not exist in list_two.
        @param {list} list_one the primary list for comparison
        @param {list} list_two
        @function findListDiff
    '''
    return [x for x in list_one if x not in list_two]

def set_defaults(default_vals, obj):
    '''
        Sets default values on the dict provided, if they do not already exist.

        ----------

        Arguments
        -------------------------
        `default_vals` {dict}
            The default values to set on the obj.
        `obj` {dict}
            The object to assign default values to.

        Keyword Arguments
        -------------------------
        `arg_name` {type}
                arg_description

        Return {dict}
        ----------------------
        The obj with default values applied

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:04:03
        `memberOf`: object_utils
        `version`: 1.0
        `method_name`: set_defaults
    '''
    for k, v in default_vals.items():
        if k not in obj:
            obj[k] = v
        # print(f"k: {k} - v: {v}")
    return obj

def get_arg(args,key_name,default_val=False, value_type=None):
    '''
        Get a key's value from a dictionary.

        ----------

        Arguments
        -------------------------
        `args` {dict}
            The dictionary to search within.

        `key_name` {str|list}
            The key or list of keys to search for.

        [`default_val`=False] {any}
            The value to return if the key is not found.

        [`value_type`=None] {any}
            The type the value should have. This can be a tuple of types.

        Return {any}
        ----------------------
        The key's value if it is found and matches the value_type (if provided.)
        The default value otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-02-2022 07:43:12
        `memberOf`: object_utils
        `version`: 1.0
        `method_name`: get_arg
        * @xxx [06-02-2022 07:46:35]: documentation for get_arg
    '''


    if isinstance(args,(dict)) is False:
        return default_val
    if len(args.keys()) == 0:
        return default_val

    args = keys_to_lower(args)
    # if defaults is not None:
    #     defaults = keys_to_lower(defaults)
    #     args = set_defaults(defaults,args)

    if isinstance(key_name, list) is False:
        key_name = [key_name]

    for name in key_name:
        # generate basic variations of the name
        varis = _gen_variations(name)
        for v_name in varis:
            if v_name in args:
                if value_type is not None:
                    if isinstance(args[v_name], value_type) is True:
                        return args[v_name]
                else:
                    return args[v_name]
    return default_val


def strip_list_nulls(value):
    '''
        Remove all None values from a list.

        ----------

        Arguments
        -------------------------
        `value` {list}
            The list to remove nulls from.

        Return {list}
        ----------------------
        The list with null values removed.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-02-2022 07:47:09
        `memberOf`: object_utils
        `version`: 1.0
        `method_name`: strip_list_nulls
        * @xxx [06-02-2022 07:47:51]: documentation for strip_list_nulls
    '''

    if isinstance(value,(list)) is False:
        return value
    return [x for x in value if x is not None]


def append(base=None,value=None,**kwargs):
    '''
        Append an item to the base list.
        This is a lazy way of merging lists or appending a single item.

        ----------

        Arguments
        -------------------------
        `base` {list}
            The list to append an item to.
        `value` {any}
            The value to append to the base.

        Keyword Arguments
        -------------------------
        [`skip_null`=True] {bool}
            if True and the value is None, it will not append it.

        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 08:45:33
        `memberOf`: objectUtils
        `version`: 1.0
        `method_name`: append
        # @TODO []: documentation for append
    '''

    if base is None:
        base = []

    skip_null = get_kwarg(["skip_null"],True,(bool),**kwargs)
    if skip_null is True:
        if value is None:
            return base

    if isinstance(value,(list)):
        base = base + value
    else:
        base.append(value)
    return base

def force_list(value):
    if isinstance(value,(list)) is False:
        return [value]
    return value

def has_required_keys(data,keys,**kwargs):
    message_template = get_kwarg(['message_template'], None, (str), **kwargs)
    missing_keys = []
    keys = force_list(keys)
    for k in keys:
        if k not in data:
            if message_template is not None:
                msg = message_template.replace("__KEY__",k)
                print(Fore.RED + msg + Style.RESET_ALL)
            missing_keys.append(k)
    if len(missing_keys) > 0:
        return False
    return True
