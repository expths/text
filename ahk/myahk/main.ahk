SetCapsLockState, AlwaysOff
CapsLock::Return

; 光标运动键
$<^k::Send {Down}
$*<^i::Send {Up}
$*<^j::Send {Left}
$*<^l::Send {Right}

$<^+k::Send +{Down}
$<^+i::Send +{Up}
$<^+j::Send +{Left}
$<^+l::Send +{Right}

$<^!k::Send !{Down}
$<^!i::Send !{Up}
$<^!j::Send !{Left}
$<^!l::Send !{Right}

; CapsLock+系列键
; 光标移动
CapsLock & k::
	if GetKeyState("Shift"){
		MouseMove, 0, 50, 0, R
	}else{
		MouseMove, 0, 300, 0, R
	}
Return
CapsLock & i::
	if GetKeyState("Shift"){
		MouseMove, 0, -50, 0, R
	}else{
		MouseMove, 0, -300, 0, R
	}
Return
CapsLock & j::
	if GetKeyState("Shift"){
		MouseMove, -50, 0, 0, R
	}else{
		MouseMove, -300, 0, 0, R
	}
Return
CapsLock & l::
	if GetKeyState("Shift"){
		MouseMove, 50, 0, 0, R
	}else{
		MouseMove, 300, 0, 0, R
	}
Return
;加速光标
CapsLock & u::
	if GetKeyState("Shift"){
		MouseMove, -500, 0, 0, R
	}else{
		MouseMove, -150, 0, 0, R
	}
Return
CapsLock & o::
	if GetKeyState("Shift"){
		MouseMove, 500, 0, 0, R
	}else{
		MouseMove, 150, 0, 0, R
	}
Return

CapsLock & Space::
	Send {LButton}
Return

CapsLock & f::Send {AppsKey}
AppsKey::Send {PgDn}

