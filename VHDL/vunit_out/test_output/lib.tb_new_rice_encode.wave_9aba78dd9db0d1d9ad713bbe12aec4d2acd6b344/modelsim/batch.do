onerror {quit -code 1}
source "C:/Users/axelo/OneDrive/Skrivbord/Exjobb/GIT/Examensarbete/VHDL/vunit_out/test_output/lib.tb_new_rice_encode.wave_9aba78dd9db0d1d9ad713bbe12aec4d2acd6b344/modelsim/common.do"
set failed [vunit_load]
if {$failed} {quit -code 1}
set failed [vunit_run]
if {$failed} {quit -code 1}
quit -code 0
