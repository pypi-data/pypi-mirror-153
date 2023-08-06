" This file is part of mved, the bulk file renaming tool.
" License: GNU GPL version 3, see the file "AUTHORS" for details.
"
" File:        syntax/mved.vim
" Description: Vim syntax for mved, the bulk file renaming tool.

if exists("b:current_syntax")
    finish
endif

let s:cpo_save = &cpo
set cpo&vim

syn match mvedError +\\\%([^x]\|x.\{0,2\}\)+
syn match mvedEscape +\\[\\abfnrtv]+
syn match mvedEscape +\\x\x\x+

syn match mvedNumber /^\s*[0-9]\+/

syn match mvedError /^\s*\S*[^ 0-9]\S*\%(\s\|$\)/

syn match mvedComment +^\s*#.*$+

hi def link mvedNumber Number
hi def link mvedEscape Special
hi def link mvedComment Comment
hi def link mvedError Error

let b:current_syntax = "mved"

let &cpo = s:cpo_save
unlet s:cpo_save
