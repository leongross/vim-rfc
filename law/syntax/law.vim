" Vim syntax file
" Language: German Law
" Maintainer: github.com/leongross
" Latest Revision: 0.1.0

" https://vim.fandom.com/wiki/Creating_your_own_syntax_files
" https://neovim.io/doc/user/syntax.html#syntax-loading
"

"if exists("b:current_syntax")
"  finish
"endif

syntax clear
syntax case match


" Matches
syn match lawTitle              /Einkommensteuergesetz/
syn match lawCategory           '(\w*StG)'
syn match lawSectionHeader      '(\d)'
syn match lawSectionEnum        '\d\.'
syn match lawParagraphReference /§ \d*/
syn match lawSectionNumber      'Absatz \d*' 
syn match dbg                   '(\d)'

" Keyword
syn keyword lawKeywords Fußnote vgl

" highlights
hi link lawTitle                Title
hi link lawSectionHeader        Title
hi link lawParagraphReference   Title
hi link lawSectionEnum          Number
hi link lawCategory             Keyword
hi link lawKeywords             Keyword
hi link lawSectionNumber        Keyword

"hi link dbg                     Title

let b:current_syntax = "law"
