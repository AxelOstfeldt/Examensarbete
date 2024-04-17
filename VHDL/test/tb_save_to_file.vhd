library IEEE;
use IEEE.STD_LOGIC_1164.all;
use ieee.numeric_std.all;
use std.textio.all;

library vunit_lib;
context vunit_lib.vunit_context;

use work.MATRIX_TYPE.all;

entity tb_save_to_file is--Testbench file name here
   generic (
      runner_cfg : string
   );

end tb_save_to_file;

architecture save_to_file_arch of tb_save_to_file is--Testbench file name here
   --General signals
   constant C_SCK_CYKLE : time      := 8 ns; -- 125 MHz
   signal clk_tb        : std_logic := '0';
   signal reset_tb      : std_logic := '1';
   signal StateDelay_tb : std_logic_vector(1 downto 0);

   --Entity signals
   signal AssembleDoneIn_tb    : std_logic;
   signal AllCodeWordsIn_tb    : std_logic_vector(8191 downto 0);
   signal AllCodeWordsLenIn_tb : std_logic_vector(12 downto 0);

   signal BitToWrite_tb   : std_logic;
   signal WriteBit_tb     : std_logic;
   signal DataSavedOut_tb : std_logic;

begin
   clk_tb <= not(clk_tb) after C_SCK_CYKLE/2;--testbench clock

   reset_tb <= '1', '0' after 35 ns;

   TestSaveToFile : entity work.SaveToFile
      port map(
         --ports in entity to the left => signals in testbench to the right
         clk               => clk_tb,
         reset             => reset_tb,
         AssembleDoneIn    => AssembleDoneIn_tb,
         AllCodeWordsIn    => AllCodeWordsIn_tb,
         AllCodeWordsLenIn => AllCodeWordsLenIn_tb,

         BitToWrite   => BitToWrite_tb,
         WriteBit     => WriteBit_tb,
         DataSavedOut => DataSavedOut_tb
      );
   ws_process_1234 : process (clk_tb)
   
   

   begin
      --test code
      if falling_edge(clk_tb) then

         if StateDelay_tb = "01" then

            if DataSavedOut_tb = '1' then
               StateDelay_tb <= "10";
            end if;

         elsif StateDelay_tb = "10" then
            --Set first 8 input bits
            AllCodeWordsIn_tb(8191) <= '1';
            AllCodeWordsIn_tb(8190) <= '1';
            AllCodeWordsIn_tb(8189) <= '0';
            AllCodeWordsIn_tb(8188) <= '0';
            AllCodeWordsIn_tb(8187) <= '1';
            AllCodeWordsIn_tb(8186) <= '1';
            AllCodeWordsIn_tb(8185) <= '0';
            AllCodeWordsIn_tb(8184) <= '0';
            AllCodeWordsIn_tb(8183) <= '1';

            AssembleDoneIn_tb <= '1';

            StateDelay_tb <= "11";

         elsif StateDelay_tb = "11" then
            AssembleDoneIn_tb <= '0';

            StateDelay_tb <= "01";

         end if;
         if reset_tb = '1' then
            StateDelay_tb <= "01";

            AssembleDoneIn_tb    <= '0';
            AllCodeWordsIn_tb    <= (others => '0');
            AllCodeWordsLenIn_tb <= "0000000001010";--should be 10?

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