onerror {quit -code 1}
source "C:/Users/axelo/OneDrive/Skrivbord/Exjobb/GIT/Examensarbete/vunit_out/test_output/lib.tb_new_code_word_assembler.auto_40b197e82b9286b6c0881b64c6604d24d6adc6bb/modelsim/common.do"
set failed [vunit_load]
if {$failed} {quit -code 1}
set failed [vunit_run]
if {$failed} {quit -code 1}
quit -code 0
