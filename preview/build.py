"""Build style previews: game.html + each theme CSS -> preview/<name>.html"""
import os

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, '..', 'game.html'), encoding='utf-8') as f:
    base = f.read()

for name in ['a', 'b', 'c']:
    with open(os.path.join(here, 'theme-%s.css' % name), encoding='utf-8') as f:
        css = f.read()
    out = base.replace('</head>', '<style>\n' + css + '\n</style>\n</head>', 1)
    with open(os.path.join(here, 'style-%s.html' % name), 'w', encoding='utf-8') as f:
        f.write(out)
    print('built style-%s.html' % name)
