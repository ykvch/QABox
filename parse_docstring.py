from textwrap import dedent


def parse_docstring(docstring):
    """Grab nicely formatted sections from test docstring

    Args:
        docstring (str): test docstring

    Returns:
        dict where keys are title (for test title, the 1st line of docstring),
        pre (for preconditions), step (for steps to execute),
        expect (for expected results) and values are dedented texts
        from corresponding docstring sections
    """

    isdash = lambda s: all('-' == i for i in s.strip())
    head, _, tail = docstring.partition('\n')
    head = head.strip()
    text = (line for line in dedent(tail).splitlines() if line and not isdash(line))
    sections = dict(title=head if head else text.next(), pre=[], step=[], expect=[])

    cur_section = sections['pre']
    for line in text:
        if line.endswith(':'):
            for k in sections:
                if line.lower().startswith(k):
                    cur_section = sections[k]
                    break
            else:
                cur_section.append(line)
        else:
            cur_section.append(line)
    return sections
