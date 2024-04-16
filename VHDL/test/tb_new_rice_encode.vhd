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

   constant C_CLK_CYKLE       : time      := 8 ns; -- 125 MHz
   signal clk_tb              : std_logic := '0';
   signal reset_tb            : std_logic := '1';
   signal StateDelay_tb       : std_logic_vector(1 downto 0);
   signal CreateResiduals_tb  : std_logic_vector(24 downto 0);
   signal ResidualsCounter_tb : integer range 0 to 64;
   signal SetResidualsBit_tb  : integer range 0 to 1600;

   signal AllResidualsIn_tb          : std_logic_vector(1599 downto 0);
   signal kValueIn_tb                : std_logic_vector(4 downto 0);
   signal NewKIn_tb                  : std_logic;--New data available for input
   signal NewResidualsIn_tb          : std_logic;
   signal ReadytoReciveCodeWordIn_tb : std_logic;

   signal NewCodeWordReady_tb : std_logic;--New CodeWord ready to be sent
   signal CodeWordLen_tb      : std_logic_vector(9 downto 0);--Bits used in the codeword
   signal CodeWord_tb         : std_logic_vector(1023 downto 0);--CodeWord out
   signal ErrorOut_tb         : std_logic;
   signal ReadyToEncode_tb    : std_logic;
   signal k_valueOut_tb       : std_logic_vector(4 downto 0);

begin
   clk_tb <= not(clk_tb) after C_CLK_CYKLE/2;

   reset_tb <= '1', '0' after 35 ns;

   RiceEncoderTest : entity work.NewRiceEncoder
      port map(
         reset                   => reset_tb,
         clk                     => clk_tb,
         AllResidualsIn          => AllResidualsIn_tb,
         kValueIn                => kValueIn_tb,
         NewResidualsIn          => NewResidualsIn_tb,
         NewKIn                  => NewKIn_tb,
         ReadytoReciveCodeWordIn => ReadytoReciveCodeWordIn_tb,

         NewCodeWordReady => NewCodeWordReady_tb,
         CodeWordLen      => CodeWordLen_tb,
         CodeWord         => CodeWord_tb,
         ReadyToEncode    => ReadyToEncode_tb,
         k_valueOut => k_valueOut_tb,

         ErrorOut         => ErrorOut_tb
      );
   ws_process_1234 : process (clk_tb)
   begin

      if falling_edge(clk_tb) then

         if StateDelay_tb = "00" then
            ReadytoReciveCodeWordIn_tb <= '0';

            --Set all residual values for the test bench
            AllResidualsIn_tb(1599 - SetResidualsBit_tb) <= CreateResiduals_tb(24);
            AllResidualsIn_tb(1598 - SetResidualsBit_tb) <= CreateResiduals_tb(23);
            AllResidualsIn_tb(1597 - SetResidualsBit_tb) <= CreateResiduals_tb(22);
            AllResidualsIn_tb(1596 - SetResidualsBit_tb) <= CreateResiduals_tb(21);
            AllResidualsIn_tb(1595 - SetResidualsBit_tb) <= CreateResiduals_tb(20);
            AllResidualsIn_tb(1594 - SetResidualsBit_tb) <= CreateResiduals_tb(19);
            AllResidualsIn_tb(1593 - SetResidualsBit_tb) <= CreateResiduals_tb(18);
            AllResidualsIn_tb(1592 - SetResidualsBit_tb) <= CreateResiduals_tb(17);
            AllResidualsIn_tb(1591 - SetResidualsBit_tb) <= CreateResiduals_tb(16);
            AllResidualsIn_tb(1590 - SetResidualsBit_tb) <= CreateResiduals_tb(15);
            AllResidualsIn_tb(1589 - SetResidualsBit_tb) <= CreateResiduals_tb(14);
            AllResidualsIn_tb(1588 - SetResidualsBit_tb) <= CreateResiduals_tb(13);
            AllResidualsIn_tb(1587 - SetResidualsBit_tb) <= CreateResiduals_tb(12);
            AllResidualsIn_tb(1586 - SetResidualsBit_tb) <= CreateResiduals_tb(11);
            AllResidualsIn_tb(1585 - SetResidualsBit_tb) <= CreateResiduals_tb(10);
            AllResidualsIn_tb(1584 - SetResidualsBit_tb) <= CreateResiduals_tb(9);
            AllResidualsIn_tb(1583 - SetResidualsBit_tb) <= CreateResiduals_tb(8);
            AllResidualsIn_tb(1582 - SetResidualsBit_tb) <= CreateResiduals_tb(7);
            AllResidualsIn_tb(1581 - SetResidualsBit_tb) <= CreateResiduals_tb(6);
            AllResidualsIn_tb(1580 - SetResidualsBit_tb) <= CreateResiduals_tb(5);
            AllResidualsIn_tb(1579 - SetResidualsBit_tb) <= CreateResiduals_tb(4);
            AllResidualsIn_tb(1578 - SetResidualsBit_tb) <= CreateResiduals_tb(3);
            AllResidualsIn_tb(1577 - SetResidualsBit_tb) <= CreateResiduals_tb(2);
            AllResidualsIn_tb(1576 - SetResidualsBit_tb) <= CreateResiduals_tb(1);
            AllResidualsIn_tb(1575 - SetResidualsBit_tb) <= CreateResiduals_tb(0);
            --increment so that the next residual in AllResidualsIn can be set
            if ResidualsCounter_tb < 63 then
               ResidualsCounter_tb <= ResidualsCounter_tb + 1;
               CreateResiduals_tb  <= std_logic_vector(signed(CreateResiduals_tb) + 1);
               SetResidualsBit_tb  <= SetResidualsBit_tb + 25;
            -- when AllREsidualsIn bit are set go to next step
            elsif ResidualsCounter_tb = 63 then
               NewKIn_tb         <= '1';
               NewResidualsIn_tb <= '1';--indicates all residuals have been set
               if ReadyToEncode_tb = '1' then
                  ResidualsCounter_tb <= ResidualsCounter_tb + 1;
                  StateDelay_tb     <= "01";
               end if;

            end if;

         elsif StateDelay_tb <= "01" then
            --This state is just for signals to be stable, might not be needed
            ReadytoReciveCodeWordIn_tb <= '0';
            NewKIn_tb                  <= '0';
            StateDelay_tb              <= "11";

         elsif StateDelay_tb = "10" then
            --Once a codeword is ready to be sent this state is entered

            -- Indicates that the codeword is ready to be recived
            ReadytoReciveCodeWordIn_tb <= '1';

            if NewCodeWordReady_tb = '0' then
               --if ResidualCounter = 0 all residuals have been encoded, 
               --go to state "00" to set new residuals
               if ResidualsCounter_tb = 0 then
                  --Reset counters
                  SetResidualsBit_tb  <= 0;
                  ResidualsCounter_tb <= 0;
                  --set negative residuals by starting at -32
                  CreateResiduals_tb <= "1111111111111111111100000";

                  if kValueIn_tb = "10100" then
                     kValueIn_tb <= "01000";

                  else
                     kValueIn_tb <= std_logic_vector(unsigned(kValueIn_tb) + 1);

                  end if;

                  StateDelay_tb      <= "00";

                  --if all residuals have not been encoded keep creating codewords until all residuals have been encoded
               else
                  StateDelay_tb <= "01";

               end if;
            end if;

         else
            --if a new codeword is ready to be sent go to the next state
            if NewCodeWordReady_tb = '1' then
               StateDelay_tb <= "10";
               --this line is to see how many residuals have been set
               if ResidualsCounter_tb > 0 then
                  ResidualsCounter_tb <= ResidualsCounter_tb - 1;
               end if;
            end if;

         end if;
         if reset_tb = '1' then
            ReadytoReciveCodeWordIn_tb <= '0';
            StateDelay_tb              <= "00";
            --Start residuals at 1
            CreateResiduals_tb  <= "0000000000000000000000001";
            ResidualsCounter_tb <= 0;
            NewResidualsIn_tb   <= '0';
            NewKIn_tb           <= '0';
            AllResidualsIn_tb   <= (others => '0');
            SetResidualsBit_tb  <= 0;
            kValueIn_tb         <= "01000";--keep bit 3 as a '1', the lowest k-value that works is 8, highest is 22
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