#NoEnv
#SingleInstance, Force
SendMode, Input
SetBatchLines, -1
SetWorkingDir, %A_ScriptDir%

;适用于OneNote的快捷键
#IfWinActive ahk_exe ONENOTE.EXE
q::Send,!{1}
w::Send,!{2}
e::Send,!{3}
a::Send,!{d}{t} ;指针
s::Send,!{d}{l} ;套索
d::Send,{Delete}
z::Send,^{z}
x::Send,^{x}
c::Send,^{c}
v::Send,^{v}
CapsLock::Send,!{d}{x}