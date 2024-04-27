onerror {quit -code 1}
source "C:/Users/axelo/OneDrive/Skrivbord/Exjobb/GIT/Examensarbete/VHDL/vunit_out/test_output/lib.tb_save_to_file.auto_3a25e16ce962d6cadb7ae49b736d71982009cf88/modelsim/common.do"
set failed [vunit_load]
if {$failed} {quit -code 1}
set failed [vunit_run]
if {$failed} {quit -code 1}
quit -code 0
