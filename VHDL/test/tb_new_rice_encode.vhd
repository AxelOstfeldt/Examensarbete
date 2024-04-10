library IEEE;
use IEEE.STD_LOGIC_1164.all;
use ieee.numeric_std.all;

library vunit_lib;
context vunit_lib.vunit_context;

use work.MATRIX_TYPE.all;

entity tb_new_rice_encode is
   generic (
      runner_cfg : string
   );

end tb_new_rice_encode;

architecture new_rice_encode_arch of tb_new_rice_encode is

   constant C_CLK_CYKLE : time      := 8 ns; -- 125 MHz
   signal clk_tb        : std_logic := '0';
   signal reset_tb      : std_logic := '1';
   signal StateDelay    : std_logic;


   signal OriginalValue_tb  : std_logic_vector(23 downto 0);
   signal k_value_tb        : std_logic_vector(4 downto 0);
   signal NewDataIn_tb      : std_logic;--New data available for input
   signal NewDataOut_tb     : std_logic;--New CodeWord ready to be sent
   signal CodeWordLength_tb : std_logic_vector(4 downto 0);--Bits used in the codeword
   signal CodeWord_tb       : std_logic_vector(23 downto 0);--CodeWord out

begin
   clk_tb <= not(clk_tb) after C_CLK_CYKLE/2;

   reset_tb <= '1', '0' after 35 ns;

   RiceEncoderTest : entity work.NewRiceEncoder
      port map(
         reset          => reset_tb,
         clk            => clk_tb,
         OriginalValue  => OriginalValue_tb,
         k_value        => k_value_tb,
         NewDataIn      => NewDataIn_tb,
         NewDataOut     => NewDataOut_tb,
         CodeWordLength => CodeWordLength_tb,
         CodeWord       => CodeWord_tb
      );
   ws_process_1234 : process (clk_tb)
   begin

      if falling_edge(clk_tb) then
         if NewDataOut_tb = '1' then
            OriginalValue_tb <= std_logic_vector(signed(OriginalValue_tb) + 1);
            StateDelay       <= '1';
         end if;


         if StateDelay = '1' then
            NewDataIn_tb <= '1';

         else
            NewDataIn_tb <= '0';
         end if;
    

         if reset_tb = '1' then
            NewDataIn_tb     <= '0';
            StateDelay       <= '1';
            OriginalValue_tb <= (others => '0'); --"000000000000000000011001";
            k_value_tb       <= "00010";
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