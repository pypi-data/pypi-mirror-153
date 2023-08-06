import xml.etree.ElementTree as ET


def _format_tag(tag: str) -> str:

    return tag.replace("{http://www.perkinelmer.com/PEHH/HarmonyV5}", "")


def _isfloat(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def _isint(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def _format_text(text: str):

    if text is None:
        return ""

    if text[0] == "[":
        temp = text.replace("[", "").replace("]", "")
        return [_format_text(t) for t in temp.split(",")]

    if _isint(text):
        return int(text)

    if _isfloat(text):
        return float(text)

    return text


def parse_tree_branch(branch) -> dict:

    if not list(branch):
        return {_format_tag(branch.tag): _format_text(branch.text)}

    dict_out = {}

    for this_branch in list(branch):
        temp = parse_tree_branch(this_branch)

        for this_key in list(temp.keys()):
            if this_key in dict_out:
                if isinstance(dict_out[this_key], list):
                    dict_out[this_key].append(temp[this_key])
                else:
                    dict_out[this_key] = [dict_out[this_key]]
                    dict_out[this_key].append(temp[this_key])
            else:
                dict_out[this_key] = temp[this_key]

    return {_format_tag(branch.tag): dict_out}
