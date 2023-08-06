import matplotlib.pyplot as plt


text_config = {
    'ha': 'center',
    'fontsize': 'xx-small'
}

def plot_grammar(grammar, **kargs):
    plt.text(0, 0, grammar.root, **text_config)
    root_rule = grammar.get_rule(grammar.root)
    plot_children(root_rule.derivation, grammar, **kargs)
    plt.xlim(-15, 15)
    plt.ylim(-6, 0)
    plt.xticks([])
    plt.yticks([])
    plt.show()

def get_arrow_color(s):
    if isinstance(s, list):
        return 'green'
    elif isinstance(s, tuple):
        return 'blue'
    elif isinstance(s, str):
        return 'black'
    return 'red'

def plot_children(derivation, grammar, plotted_tokens=[], parent_pos=(0, 0), spacing=(10, 2)):
    parent_x, parent_y = parent_pos
    spacing_x, spacing_y = spacing
    if isinstance(derivation, str):
        plt.text(parent_x, parent_y - spacing_y, derivation, **text_config)
    for i, token in enumerate(derivation):
        spacing_x = 1 if parent_y == -3 else spacing_x
        spacing_x = 1 if parent_y == -4 else spacing_x
        x = (i - (len(derivation)-1)/2) * spacing_x + parent_x
        y = parent_y - spacing_y
        width = 0.002 * spacing_x
        text = token if token else '$\epsilon$'
        plt.text(x, y, text, **text_config)
        plt.arrow(parent_x, parent_y, x-parent_x, y-parent_y, width=width, color=get_arrow_color(derivation))
        plotted_tokens.append(token)
        if token.startswith('<') and plotted_tokens.index(token) == len(plotted_tokens)-1:
            next_rule = grammar.get_rule(token)
            new_spacing_x = spacing_x / len(next_rule.derivation)
            new_spacing_y = spacing_y * 0.6
            plot_children(next_rule.derivation, grammar, plotted_tokens, (x, y), (new_spacing_x, new_spacing_y))