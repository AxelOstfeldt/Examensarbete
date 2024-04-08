library IEEE;
use IEEE.STD_LOGIC_1164.all;
use ieee.numeric_std.all;

library vunit_lib;
context vunit_lib.vunit_context;

use work.MATRIX_TYPE.all;

entity tb_new_adjacent_recreate is
   generic (
      runner_cfg : string
   );

end tb_new_adjacent_recreate;

architecture new_adjacent_recreate_arch of tb_new_adjacent_recreate is
   constant C_CLK_CYKLE : time      := 8 ns; -- 125 MHz
   signal clk_tb        : std_logic := '0';
   signal reset_tb      : std_logic := '1';

   signal mic_tb                 : unsigned(5 downto 0)          := (others => '0');
   signal residual_tb            : std_logic_vector(23 downto 0) := (others => '0');
   signal recreated_value_tb     : std_logic_vector(23 downto 0) := (others => '0');
   signal modResult_tb           : integer range 0 to 10;

begin
   clk_tb <= not(clk_tb) after C_CLK_CYKLE/2;

   reset_tb <= '1', '0' after 35 ns;

   AdjacentRecreateTest : entity work.AdjacentRecreate
      port map(
         --ports in entity to the left => signals in testbench to the right
         clk                 => clk_tb,
         reset               => reset_tb,
         mic                 => mic_tb,
         recreated_value     => recreated_value_tb,
         residual            => residual_tb,
         modResult           => modResult_tb
      );

   ws_process_4321 : process (clk_tb)
   begin
      --test code
      if falling_edge(clk_tb) then

         mic_tb      <= unsigned(mic_tb + 1);
         residual_tb <= std_logic_vector(signed(residual_tb) + 1);



      end if;

      if reset_tb = '1' then
         mic_tb      <= (others => '0');
         residual_tb <= (others => '0');
      end if;

   end process;
   main : process
   begin
      test_runner_setup(runner, runner_cfg);

      wait until reset_tb = '0';
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