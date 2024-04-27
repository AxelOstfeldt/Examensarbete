onerror {quit -code 1}
source "C:/Users/axelo/OneDrive/Skrivbord/Exjobb/GIT/Examensarbete/VHDL/vunit_out/test_output/lib.tb_new_save_to_file.auto_abe544397fa7549e33639e73b9695af0813c6f1a/modelsim/common.do"
set failed [vunit_load]
if {$failed} {quit -code 1}
set failed [vunit_run]
if {$failed} {quit -code 1}
quit -code 0
