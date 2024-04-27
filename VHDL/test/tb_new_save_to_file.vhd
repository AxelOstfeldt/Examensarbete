library IEEE;
use IEEE.STD_LOGIC_1164.all;
use ieee.numeric_std.all;
use std.textio.all;

library vunit_lib;
context vunit_lib.vunit_context;

use work.MATRIX_TYPE.all;

entity tb_new_save_to_file is--Testbench file name here
   generic (
      runner_cfg : string
   );

end tb_new_save_to_file;

architecture new_save_to_file_arch of tb_new_save_to_file is--Testbench file name here
    --General signals
    constant C_SCK_CYKLE : time      := 8 ns; -- 125 MHz
    signal clk_tb        : std_logic := '0';
    signal reset_tb      : std_logic := '1';
    signal StateDelay_tb : std_logic_vector(1 downto 0);
    signal NewRow_tb : std_logic;
    signal BottomLimit_tb : integer range 0 to 8191;
    signal RowCounter_tb : integer range 0 to 65535;
    signal AllDone : std_logic;

 
    --Signals from CodeWordAssembler
    signal AssembleDoneOut_tb    : std_logic;
    signal AllCodeWordsOut_tb    : std_logic_vector(8191 downto 0);
    signal AllCodeWordsLenOut_tb : std_logic_vector(12 downto 0);

    --Signals to CodeWordAssembler
    signal DataSavedIn_tb : std_logic;




begin
   clk_tb <= not(clk_tb) after C_SCK_CYKLE/2;--testbench clock

   reset_tb <= '1', '0' after 35 ns;



   ws_process_1234 : process (clk_tb)
      --Variables to write to txt file
      --Importent to check path /My/Path/MyFileName.txt
      --file file_handler     : text open write_mode is "/home/toad/Projects/FPGA-sampling2/pl/test/testtext.txt";
      
      file file_handler     : text open write_mode is "C:\\Users\\axelo\\OneDrive\\Skrivbord\\Exjobb\\GIT\\SoundData\\VHDL\\new_save.txt";
      
      variable row          : line;
--      variable v_data_write : std_logic;

      --remove after test
      variable v_data_write : std_logic_vector(8191 downto 0);

   begin
      --test code
      if falling_edge(clk_tb) then


         if StateDelay_tb = "01" then
            --wait for a new codeword to be done
            DataSavedIn_tb <= '1';
            if AssembleDoneOut_tb = '1' then

               v_data_write := AllCodeWordsOut_tb;
               BottomLimit_tb <= to_integer(unsigned(AllCodeWordsLenOut_tb));

               --when a codeword is available go to next state
               StateDelay_tb <= "10";


            end if;

         elsif StateDelay_tb = "10" then
            
            DataSavedIn_tb <= '0';

            if NewRow_tb = '0' then
               write(row, v_data_write(8191 downto 8191-BottomLimit_tb));
               NewRow_tb <= '1';
               RowCounter_tb <= RowCounter_tb + 1;

            else
               writeline(file_handler ,row);
               NewRow_tb <= '0';

               StateDelay_tb <= "11";

            end if;

         elsif StateDelay_tb = "11" then
            --set new values
            AllCodeWordsOut_tb(8191) <= not(AllCodeWordsOut_tb(8191));
            AllCodeWordsOut_tb(8190) <= not(AllCodeWordsOut_tb(8190));
            AllCodeWordsOut_tb(8189) <= not(AllCodeWordsOut_tb(8189));
            AllCodeWordsOut_tb(8188) <= not(AllCodeWordsOut_tb(8188));
            AllCodeWordsOut_tb(8187) <= not(AllCodeWordsOut_tb(8187));
            AllCodeWordsOut_tb(8186) <= not(AllCodeWordsOut_tb(8186));
            AllCodeWordsOut_tb(8185) <= not(AllCodeWordsOut_tb(8185));
            AllCodeWordsOut_tb(8184) <= not(AllCodeWordsOut_tb(8184));
            AllCodeWordsOut_tb(8183) <= not(AllCodeWordsOut_tb(8183));
            AllCodeWordsOut_tb(8182) <= not(AllCodeWordsOut_tb(8182));


            --Check if all 256 samples have been written
            if RowCounter_tb < 256 then
               StateDelay_tb <= "01";

            else
               StateDelay_tb <= "00";

            end if;

         elsif StateDelay_tb = "00" then
            file_close(file_handler);

            AllDone <= '1';



         end if;










         if reset_tb = '1' then
            StateDelay_tb <= "01";
            NewRow_tb <= '0';
            AllDone <= '0';
            RowCounter_tb <= 0;
            BottomLimit_tb <= 0;
            DataSavedIn_tb <= '0';
            

            AssembleDoneOut_tb    <= '1';
            AllCodeWordsOut_tb    <= (others => '0');
            AllCodeWordsLenOut_tb <= "0000000001010";--should be 10?

            AllCodeWordsOut_tb(8191) <= '1';
            AllCodeWordsOut_tb(8190) <= '1';
            AllCodeWordsOut_tb(8189) <= '0';
            AllCodeWordsOut_tb(8188) <= '0';
            AllCodeWordsOut_tb(8187) <= '1';
            AllCodeWordsOut_tb(8186) <= '1';
            AllCodeWordsOut_tb(8185) <= '0';
            AllCodeWordsOut_tb(8184) <= '0';
            AllCodeWordsOut_tb(8183) <= '1';
            AllCodeWordsOut_tb(8182) <= '0';


            



         end if;
      end if;

   end process;

   main_1234 : process
   begin
      test_runner_setup(runner, runner_cfg);
      while test_suite loop
         if run("wave") then
            -- test 1 is so far only meant for gktwave

            wait for 300000 ns; -- duration of test 1

         elsif run("auto") then

            wait for 11 ns;

         end if;
      end loop;

      test_runner_cleanup(runner);
   end process;

   test_runner_watchdog(runner, 100 ms);
end architecture;