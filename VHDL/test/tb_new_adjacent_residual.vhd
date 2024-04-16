library IEEE;
use IEEE.STD_LOGIC_1164.all;
use ieee.numeric_std.all;

library vunit_lib;
context vunit_lib.vunit_context;

use work.MATRIX_TYPE.all;

entity tb_new_adjacent_residual is--Testbench file name here
   generic (
      runner_cfg : string
   );

end tb_new_adjacent_residual;

architecture new_adjacent_residual_arch of tb_new_adjacent_residual is--Testbench file name here
   constant C_SCK_CYKLE   : time      := 8 ns;                           -- 125 MHz
   signal clk_tb          : std_logic := '0';
   signal reset_tb        : std_logic := '1';
   signal StateDelay_tb   : std_logic_vector(1 downto 0);
   signal CreateInput_tb  : std_logic_vector(23 downto 0);
   signal InputCounter_tb : integer range 0 to 1535;

   signal DataBlockIn_tb      : std_logic_vector(1535 downto 0);
   signal ReadyToEncodeIn_tb  : std_logic;
   signal DataBlockReadyIn_tb : std_logic;
   signal ReadyToReciveIn_tb  : std_logic;

   signal ResidualsCalculatedOut_tb : std_logic;
   signal ResidualValueOut_tb       : std_logic_vector(24 downto 0);
   signal NewDataOut_tb             : std_logic;
   signal AllResidualsOut_tb        : std_logic_vector(1599 downto 0);
   signal NewResidualOut_tb         : std_logic;

   signal ErrorOut_tb : std_logic;

begin
   clk_tb <= not(clk_tb) after C_SCK_CYKLE/2;--testbench clock

   reset_tb <= '1', '0' after 35 ns;
   --the name on the left of : is the name seen for test bench signals in gtkwave
   -- entity work."entity name in the file you want to test"

   --adjacentResiduals entity
   AdjacentResidualsTest : entity work.AdjacentResiduals
      port map(
         --ports in entity to the left => signals in testbench to the right
         clk   => clk_tb,
         reset => reset_tb,

         DataBlockIn      => DataBlockIn_tb,
         ReadyToEncodeIn  => ReadyToEncodeIn_tb,
         DataBlockReadyIn => DataBlockReadyIn_tb,
         ReadyToReciveIn  => ReadyToReciveIn_tb,

         ResidualsCalculatedOut => ResidualsCalculatedOut_tb,
         ResidualValueOut       => ResidualValueOut_tb,
         NewDataOut             => NewDataOut_tb,
         AllResidualsOut        => AllResidualsOut_tb,
         NewResidualOut         => NewResidualOut_tb,

         ErrorOut => ErrorOut_tb
      );

   ws_process_1234 : process (clk_tb)
   begin
      --test code
      if falling_edge(clk_tb) then

         if StateDelay_tb = "01" then

            --set input values for testbench
            DataBlockIn_tb(1535 - InputCounter_tb) <= CreateInput_tb(23);
            DataBlockIn_tb(1534 - InputCounter_tb) <= CreateInput_tb(22);
            DataBlockIn_tb(1533 - InputCounter_tb) <= CreateInput_tb(21);
            DataBlockIn_tb(1532 - InputCounter_tb) <= CreateInput_tb(20);
            DataBlockIn_tb(1531 - InputCounter_tb) <= CreateInput_tb(19);
            DataBlockIn_tb(1530 - InputCounter_tb) <= CreateInput_tb(18);
            DataBlockIn_tb(1529 - InputCounter_tb) <= CreateInput_tb(17);
            DataBlockIn_tb(1528 - InputCounter_tb) <= CreateInput_tb(16);
            DataBlockIn_tb(1527 - InputCounter_tb) <= CreateInput_tb(15);
            DataBlockIn_tb(1526 - InputCounter_tb) <= CreateInput_tb(14);
            DataBlockIn_tb(1525 - InputCounter_tb) <= CreateInput_tb(13);
            DataBlockIn_tb(1524 - InputCounter_tb) <= CreateInput_tb(12);
            DataBlockIn_tb(1523 - InputCounter_tb) <= CreateInput_tb(11);
            DataBlockIn_tb(1522 - InputCounter_tb) <= CreateInput_tb(10);
            DataBlockIn_tb(1521 - InputCounter_tb) <= CreateInput_tb(9);
            DataBlockIn_tb(1520 - InputCounter_tb) <= CreateInput_tb(8);
            DataBlockIn_tb(1519 - InputCounter_tb) <= CreateInput_tb(7);
            DataBlockIn_tb(1518 - InputCounter_tb) <= CreateInput_tb(6);
            DataBlockIn_tb(1517 - InputCounter_tb) <= CreateInput_tb(5);
            DataBlockIn_tb(1516 - InputCounter_tb) <= CreateInput_tb(4);
            DataBlockIn_tb(1515 - InputCounter_tb) <= CreateInput_tb(3);
            DataBlockIn_tb(1514 - InputCounter_tb) <= CreateInput_tb(2);
            DataBlockIn_tb(1513 - InputCounter_tb) <= CreateInput_tb(1);
            DataBlockIn_tb(1512 - InputCounter_tb) <= CreateInput_tb(0);

            --Increament Create Input
            CreateInput_tb <= std_logic_vector(unsigned(CreateInput_tb) - 100);

            --24*62 = 1488, so when 1488 this state is in its second to last lap and adds 24 more to pass the if statement limit
            if InputCounter_tb > 1488 then

               --once this limit is reached all mic value have been set and the datablock input is done
               DataBlockReadyIn_tb <= '1';
               StateDelay_tb       <= "00";

            else
               --increment InputCounter_tb to set the nxt 24 values for the next mic
               InputCounter_tb     <= InputCounter_tb + 24;
               DataBlockReadyIn_tb <= '0';
               ReadyToEncodeIn_tb  <= '0';
               ReadyToReciveIn_tb  <= '0';

            end if;

         elsif StateDelay_tb = "10" then

            --This state indicates kCalculator is ready to recive a new residual
            ReadyToReciveIn_tb  <= '1';
            ReadyToEncodeIn_tb  <= '0';
            DataBlockReadyIn_tb <= '0';

            if NewDataOut_tb = '0' then
               StateDelay_tb <= "00";

            end if;

         elsif StateDelay_tb = "11" then

            --This state indicates RiceEncode is ready for a new block of residuals
            ReadyToEncodeIn_tb  <= '1';
            ReadyToReciveIn_tb  <= '0';
            DataBlockReadyIn_tb <= '0';

            if NewResidualOut_tb = '0' then
               StateDelay_tb <= "01";

            end if;

         else

            if NewDataOut_tb = '1' then
               StateDelay_tb <= "10";

            elsif NewResidualOut_tb = '1' then
               StateDelay_tb <= "11";

            end if;

            ReadyToEncodeIn_tb  <= '0';
            ReadyToReciveIn_tb  <= '0';
            DataBlockReadyIn_tb <= '0';

            InputCounter_tb <= 0;

         end if;
         if reset_tb = '1' then
            DataBlockIn_tb      <= (others => '0');
            ReadyToEncodeIn_tb  <= '0';
            DataBlockReadyIn_tb <= '0';
            ReadyToReciveIn_tb  <= '0';

            StateDelay_tb   <= "01";
            CreateInput_tb  <= (others => '0');
            InputCounter_tb <= 0;
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