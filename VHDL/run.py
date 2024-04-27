#install vunit useing: pip install vunit_hdl

#In order to run the following test enter test file and ensure the pathing of the files to read/write is correct:
#tb_adjacent_combined
#tb_load_data
#tb_new_sate_to_file
#tb_save_to_file



from pathlib import Path
from vunit import VUnit


# NOTE: Path to directory containing this file
ROOT = Path(__file__).parent

vu = VUnit.from_argv(compile_builtins=False)  # Stop using the builtins ahead of time.vu.add_vhdl_builtins() #new for version 5 VUnit
vu.add_vhdl_builtins() #new for version 5 VUnit

lib = vu.add_library("lib")
lib.add_source_files(ROOT.glob("test/**/*.vhd"))


lib.add_source_files(ROOT.glob("src/**/*.vhd"))


for l in lib.get_test_benches():
   wave = ROOT.joinpath("test", "wave", f"{l.name}.tcl")
   l.set_sim_option("ghdl.gtkwave_script.gui", str(wave) if wave.is_file() else str(ROOT / "gtkwave.tcl"))

vu.main()