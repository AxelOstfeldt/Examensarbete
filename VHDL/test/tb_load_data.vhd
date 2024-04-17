library IEEE;
use IEEE.STD_LOGIC_1164.all;
use ieee.numeric_std.all;
use std.textio.all;

library vunit_lib;
context vunit_lib.vunit_context;

use work.MATRIX_TYPE.all;

entity tb_load_data is--Testbench file name here
   generic (
      runner_cfg : string
   );

end tb_load_data;

architecture load_data_arch of tb_load_data is--Testbench file name here


   --General signals
   constant C_SCK_CYKLE   : time      := 8 ns; -- 125 MHz
   signal clk_tb          : std_logic := '0';
   signal reset_tb        : std_logic := '1';

   signal CurrentValue_tb : std_logic_vector(23 downto 0);
   signal StateDelay_tb : std_logic_vector(1 downto 0);
   signal SampleCounter_tb : integer range 0 to 65535;
   signal MicCounter_tb : integer range 0 to 65535;

   



   signal LastMicReached_tb : std_logic;
   signal EndOfFileReached_tb : std_logic;




   


begin
   clk_tb <= not(clk_tb) after C_SCK_CYKLE/2;--testbench clock

   reset_tb <= '1', '0' after 35 ns;


   ws_process_1234 : process (clk_tb)
      variable text_line      : line;
      variable i1 : std_logic_vector(23 downto 0);


      --Make sure this directiory is correct!
      file my_file: text open read_mode is "/home/toad/Projects/FPGA-sampling2/pl/test/first_sample_binary.txt";


   begin
      --test code
      if falling_edge(clk_tb) then

         if StateDelay_tb = "01" then

            --check that it is not end of file
            if not endfile(my_file) then
               --point to the next line
               readline(my_file, text_line);
               --read the current lint
               read(text_line, i1);
               
               StateDelay_tb <= "10";

            else
               StateDelay_tb <= "00";
               EndOfFileReached_tb <= '1';

            end if;

         elsif StateDelay_tb = "10" then
            --assign CurrentValue_tb with the read value from text file
            CurrentValue_tb <= i1;

            --increment mic
            if MicCounter_tb < 63 then
               --if all 63 mics have not been set grab the next mic value
               MicCounter_tb <= MicCounter_tb + 1;
               StateDelay_tb <= "01";

            else
               StateDelay_tb <= "00";

            end if;

         else
            if MicCounter_tb = 63 then
               SampleCounter_tb <= SampleCounter_tb + 1;

               LastMicReached_tb <= '1';
               MicCounter_tb <= 0;

            else
               StateDelay_tb <= "01";

            end if;

         end if;







         if reset_tb = '1' then
            CurrentValue_tb <= (others => '0');
            StateDelay_tb <= "00";
            MicCounter_tb <= 0;
            SampleCounter_tb <= 0;

            EndOfFileReached_tb <= '0';
            LastMicReached_tb <= '0';


         end if;


      end if;
      
   end process;

   main_1234 : process
   begin
      test_runner_setup(runner, runner_cfg);
      while test_suite loop
         if run("wave") then
            -- test 1 is so far only meant for gktwave

            wait for 50000 ns; -- duration of test 1

         elsif run("auto") then

            wait for 11 ns;

         end if;
      end loop;

      test_runner_cleanup(runner);
   end process;

   test_runner_watchdog(runner, 100 ms);
end architecture;