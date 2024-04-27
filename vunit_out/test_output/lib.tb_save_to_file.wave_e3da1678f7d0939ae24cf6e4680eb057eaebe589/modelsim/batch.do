onerror {quit -code 1}
source "C:/Users/axelo/OneDrive/Skrivbord/Exjobb/GIT/Examensarbete/vunit_out/test_output/lib.tb_save_to_file.wave_e3da1678f7d0939ae24cf6e4680eb057eaebe589/modelsim/common.do"
set failed [vunit_load]
if {$failed} {quit -code 1}
set failed [vunit_run]
if {$failed} {quit -code 1}
quit -code 0
