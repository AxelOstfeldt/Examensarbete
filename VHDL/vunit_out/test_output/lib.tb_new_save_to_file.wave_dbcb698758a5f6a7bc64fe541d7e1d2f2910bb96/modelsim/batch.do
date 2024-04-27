onerror {quit -code 1}
source "C:/Users/axelo/OneDrive/Skrivbord/Exjobb/GIT/Examensarbete/VHDL/vunit_out/test_output/lib.tb_new_save_to_file.wave_dbcb698758a5f6a7bc64fe541d7e1d2f2910bb96/modelsim/common.do"
set failed [vunit_load]
if {$failed} {quit -code 1}
set failed [vunit_run]
if {$failed} {quit -code 1}
quit -code 0
