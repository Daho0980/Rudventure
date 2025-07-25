import re


_ansiCompile = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
escapeAnsi   = lambda l: _ansiCompile.sub('',l)

def anchor(stdscr                     ,
           string     :str            ,
           y          :int      =0    ,
           x          :int      =0    ,
           addOnyx    :list[int]=[0,0],
           returnEndyx:bool     =False,
           returnStr  :bool     =False ) -> str: # type: ignore
    lines:list[int] = list(map(lambda l:len(escapeAnsi(l)),string.split("\n")))
    y, x = (y,x)if y+x else map(
        lambda c:c[0]-int([len(lines)/2,max(lines)/2][c[1]]),
        list(zip(map(lambda n:int(n/2),stdscr.getmaxyx()),[0,1]))
    )
    y, x = y+addOnyx[0], x+addOnyx[1]+1

    output:str = ''.join(
        [
            ec for line in zip(
                [f"\033[{x};{_}H" for _ in range(y-1, y+(len(lines)))],
                string.split("\n")
                ) for ec in line
            ]
        )
    if not returnStr: stdscr.addstr(output)

    if       returnEndyx and     returnStr: return output, y+len(string.split("\n")), x # type: ignore
    elif not returnEndyx and     returnStr: return output
    elif     returnEndyx and not returnStr: return y+len(string.split("\n")), x # type: ignore