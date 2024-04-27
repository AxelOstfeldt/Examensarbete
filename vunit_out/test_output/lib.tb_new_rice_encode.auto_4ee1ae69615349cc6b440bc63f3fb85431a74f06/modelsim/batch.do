onerror {quit -code 1}
source "C:/Users/axelo/OneDrive/Skrivbord/Exjobb/GIT/Examensarbete/vunit_out/test_output/lib.tb_new_rice_encode.auto_4ee1ae69615349cc6b440bc63f3fb85431a74f06/modelsim/common.do"
set failed [vunit_load]
if {$failed} {quit -code 1}
set failed [vunit_run]
if {$failed} {quit -code 1}
quit -code 0
