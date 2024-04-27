onerror {quit -code 1}
source "C:/Users/axelo/OneDrive/Skrivbord/Exjobb/GIT/Examensarbete/vunit_out/test_output/lib.tb_calculate_k_value.wave_67f6c1f74e15611b708f67d06dcc26cd93f86017/modelsim/common.do"
set failed [vunit_load]
if {$failed} {quit -code 1}
set failed [vunit_run]
if {$failed} {quit -code 1}
quit -code 0
