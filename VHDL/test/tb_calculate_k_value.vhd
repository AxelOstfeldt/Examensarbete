library IEEE;
use IEEE.STD_LOGIC_1164.all;
use ieee.numeric_std.all;

library vunit_lib;
context vunit_lib.vunit_context;

use work.MATRIX_TYPE.all;

entity tb_calculate_k_value is
   generic (
      runner_cfg : string
   );

end tb_calculate_k_value;

architecture calculate_k_value_arch of tb_calculate_k_value is

   constant C_CLK_CYKLE   : time      := 8 ns; -- 125 MHz
   signal clk_tb          : std_logic := '0';
   signal reset_tb        : std_logic := '1';
   signal StateDelay_tb   : std_logic_vector(1 downto 0);
   signal SetInputBits_tb : integer range 0 to 23;

   signal OriginalValue_tb : std_logic_vector(23 downto 0);--value in to be encoded
   signal NewDataIn_tb     : std_logic;--New data available for input

   signal ReadyToRecive_tb : std_logic;
   signal NewKOut_tb       : std_logic;--New k-value to be sent
   signal ErrorOut_tb      : std_logic;--Send an error signal when error state is reached
   signal k_value_tb       : std_logic_vector(4 downto 0);

begin
   clk_tb <= not(clk_tb) after C_CLK_CYKLE/2;

   reset_tb <= '1', '0' after 35 ns;

   TestkCalculator : entity work.kCalculator
      port map(
         reset         => reset_tb,
         clk           => clk_tb,
         OriginalValue => OriginalValue_tb,
         NewDataIn     => NewDataIn_tb,

         ReadyToRecive => ReadyToRecive_tb,
         NewKOut       => NewKOut_tb,
         ErrorOut      => ErrorOut_tb,
         k_value       => k_value_tb

      );

   ws_process_123123124645631234 : process (clk_tb)
   begin

      if falling_edge(clk_tb) then

         if StateDelay_tb = "01" then
            --Set new original value so that k will be incremented by 1 to the next ouput
            OriginalValue_tb(SetInputBits_tb) <= '0';
            StateDelay_tb    <= "10";
            NewDataIn_tb <= '0';

         elsif StateDelay_tb = "10" then
            --set the codeword input

            NewDataIn_tb <= '0';
            StateDelay_tb    <= "11";

         elsif StateDelay_tb = "11" then
            NewDataIn_tb <= '1';

            StateDelay_tb <= "00";

         else

            if NewKOut_tb = '1' then
               if SetInputBits_tb < 22 then
                  SetInputBits_tb <= SetInputBits_tb + 1;
                  
               else
                  SetInputBits_tb <= 8;
                  OriginalValue_tb <= (others => '1');-- (others => '0');

               end if;
               StateDelay_tb <= "01";
               

            elsif ReadyToRecive_tb = '1' then
               StateDelay_tb <= "10";

            end if;

            NewDataIn_tb <= '0';

         end if;
         if reset_tb = '1' then
            StateDelay_tb <= "01";
            NewDataIn_tb     <= '0';
            OriginalValue_tb <= (others => '1');--"010010110010101010110010";--(others => '0');
            SetInputBits_tb <= 8;
         end if;

      end if;
   end process;

   main_1234 : process
   begin
      test_runner_setup(runner, runner_cfg);
      while test_suite loop
         if run("wave") then
            -- test 1 is so far only meant for gktwave

            wait for 99000 ns; -- duration of test 1

         elsif run("auto") then

            wait for 11 ns;

         end if;
      end loop;

      test_runner_cleanup(runner);
   end process;

   test_runner_watchdog(runner, 100 ms);
end architecture;