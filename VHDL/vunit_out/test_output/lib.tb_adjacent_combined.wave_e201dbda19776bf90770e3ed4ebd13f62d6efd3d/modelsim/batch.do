onerror {quit -code 1}
source "C:/Users/axelo/OneDrive/Skrivbord/Exjobb/GIT/Examensarbete/VHDL/vunit_out/test_output/lib.tb_adjacent_combined.wave_e201dbda19776bf90770e3ed4ebd13f62d6efd3d/modelsim/common.do"
set failed [vunit_load]
if {$failed} {quit -code 1}
set failed [vunit_run]
if {$failed} {quit -code 1}
quit -code 0
