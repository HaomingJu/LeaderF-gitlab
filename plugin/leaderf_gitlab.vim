"Create by Haoming on 2022-04-14

let s:inited = 0
let g:Lf_Extensions = get(g:, 'Lf_Extensions', {})
let s:home = fnamemodify(resolve(expand('<sfile>:p')), ':h')

function! s:init_python()
    if s:inited != 0
        return 0
    endif

    if !exists("g:Lf_PythonVersion")
        if has("python3")
            let g:Lf_PythonVersion = 3
            let g:Lf_py = "py3 "
        elseif has("python")
            let g:Lf_PythonVersion = 2
            let g:Lf_py = "py "
        else
            echoe "Error: LeaderF requires vim compiled with +python or +python3"
            finish
        endif
    else
        if g:Lf_PythonVersion == 2
            if has("python")
                let g:Lf_py = "py "
            else
                echoe 'LeaderF Error: has("python") == 0'
                finish
            endif
        else
            if has("python3")
                let g:Lf_py = "py3 "
            else
                echoe 'LeaderF Error: has("python3") == 0'
                finish
            endif
        endif
    endif

    exec g:Lf_py 'import sys, vim'
    exec g:Lf_py '_pp = vim.eval("s:home")'
    exec g:Lf_py 'if _pp not in sys.path: sys.path.append(_pp)'
    exec g:Lf_py 'import leaderf_gitlab'
    if g:Lf_PythonVersion == 2
        exec 'py2' 'import imp'
        exec 'py2' 'imp.reload(leaderf_gitlab)'
    else
        exec 'py3' 'import importlib'
        exec 'py3' 'importlib.reload(leaderf_gitlab)'
    endif
    let s:inited = 1
    return 1
endfunc

function! s:lf_gitlab_ping()
    let l:ping = v:false
    if g:Lf_PythonVersion == 2
        let l:ping = pyeval('leaderf_gitlab.ping()')
    else
        let l:ping = py3eval('leaderf_gitlab.ping()')
    endif
    if l:ping == v:false
        echo "[LeaderF-gitlab]: Please check your token or address of gitlab"
        echo "[LeaderF-gitlab]: Please check your token or address of gitlab"
    endif
endfunc

function! s:lf_gitlab_source(...)
    let l:source = []
    if g:Lf_PythonVersion == 2
        let l:source = pyeval('leaderf_gitlab.mr()')
    else
        let l:source = py3eval('leaderf_gitlab.mr()')
    endif
    return l:source
endfunc

let g:Lf_Extensions.mr = {
            \ 'source': string(function('s:lf_gitlab_source'))[10:-3]}

call s:init_python()
call s:lf_gitlab_ping()
