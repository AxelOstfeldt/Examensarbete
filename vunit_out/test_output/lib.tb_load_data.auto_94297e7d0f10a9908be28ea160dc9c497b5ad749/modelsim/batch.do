onerror {quit -code 1}
source "C:/Users/axelo/OneDrive/Skrivbord/Exjobb/GIT/Examensarbete/vunit_out/test_output/lib.tb_load_data.auto_94297e7d0f10a9908be28ea160dc9c497b5ad749/modelsim/common.do"
set failed [vunit_load]
if {$failed} {quit -code 1}
set failed [vunit_run]
if {$failed} {quit -code 1}
quit -code 0
