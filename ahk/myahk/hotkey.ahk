;参考资料： 映射双键https://www.zhihu.com/question/22656077

RWin up::return
^Esc::return
>#k::Send ^{k}
>#\::Send ^{Esc}
; \::SoundBeep ;发出蜂鸣声（可选频率和毫秒）

; 左控制(光标)
$<^k::Send {Down}
$<^i::Send {Up}
$<^j::Send {Left}
$<^l::Send {Right}

$<^+k::Send +{Down} ; 加shift
$<^+i::Send +{Up}
$<^+j::Send +{Left}
$<^+l::Send +{Right}

$<^!k::Send !{Down} ; 加alt
$<^!i::Send !{Up}
$<^!j::Send !{Left}
$<^!l::Send !{Right}

; 右控制(鼠标)
$>^Space::LButton
$>^k::MouseMove, 0, 300, 0, R
$>^i::MouseMove, 0, -300, 0, R
$>^j::MouseMove, -300, 0, 0, R
$>^l::MouseMove, 300, 0, 0, R

; cl控制区
>#a::Send {1}
>#s::Send {2}
>#d::Send {3}